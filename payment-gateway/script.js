/* ═══════════════════════════════════════════════════════════════
   Payment Gateway — Script
   Razorpay integration with UPI, Credit Card, Debit Card, Apple Pay
   Self-contained module. Configure CONFIG object with your keys.
   ═══════════════════════════════════════════════════════════════ */

/* ── 1. Theme sync (runs before DOMContentLoaded to prevent flash) ── */
(function syncTheme() {
  const saved = localStorage.getItem('theme-preference');
  if (saved === 'dark') document.body.dataset.theme = 'dark';
})();

/* ═══════════════════════════════════════════════════════════════
   2. CONFIGURATION — Edit this block with your Razorpay keys
   ═══════════════════════════════════════════════════════════════ */
const CONFIG = {
  razorpay: {
    keyId:       'rzp_test_YOUR_KEY_ID',   // ← replace with your Razorpay Key ID
    name:        'Ajay Girolkar',
    description: 'iOS Engineering Services',
    image:       '../assets/ajay-profile.jpg',
    currency:    'INR',
    prefill: {
      name:    '',
      email:   '',
      contact: '',
    },
    theme: {
      color: '#1e6cff',
    },
  },
  upi: {
    vpa:         'ajay@okaxis',            // ← replace with your UPI VPA
    qrExpiryMs:  600000,                   // 10 minutes
  },
  applePay: {
    merchantId:      'merchant.com.ajaygirolkar',
    countryCode:     'IN',
    currencyCode:    'INR',
    supportedNetworks:     ['visa', 'masterCard', 'amex'],
    merchantCapabilities:  ['supports3DS'],
  },
  order: {
    productName: 'iOS Consulting Session',
    productSub:  'Expert iOS engineering guidance',
    baseAmount:  12500,   // in paise (₹125.00). Overridden by URL params.
    platformFee: 0.02,    // 2%
    gstRate:     0.18,    // 18%
  },
  /* Backend endpoints for order creation & verification.
     If you don't have a backend yet, set mock: true to use
     Razorpay's standard checkout flow directly. */
  backend: {
    mock:      true,                              // ← set false when backend is ready
    createUrl: '/api/payments/create-order',
    verifyUrl: '/api/payments/verify',
  },
};

/* ═══════════════════════════════════════════════════════════════
   3. INLINE SVG LOGOS (card network detection)
   ═══════════════════════════════════════════════════════════════ */
const LOGOS = {
  visa: `<svg class="visa-logo" viewBox="0 0 80 26" fill="none" xmlns="http://www.w3.org/2000/svg">
    <text x="0" y="22" font-size="26" font-weight="900" font-family="Arial,sans-serif"
          fill="white" letter-spacing="-1">VISA</text>
  </svg>`,

  mastercard: `<svg class="mc-logo" viewBox="0 0 38 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="14" cy="12" r="12" fill="#EB001B"/>
    <circle cx="24" cy="12" r="12" fill="#F79E1B"/>
    <path d="M19 5.4a12 12 0 010 13.2A12 12 0 0119 5.4z" fill="#FF5F00"/>
  </svg>`,

  amex: `<svg class="amex-logo" viewBox="0 0 60 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <text x="0" y="16" font-size="13" font-weight="900" font-family="Arial,sans-serif"
          fill="white" letter-spacing="1">AMEX</text>
  </svg>`,

  rupay: `<svg class="rupay-logo" viewBox="0 0 60 22" fill="none" xmlns="http://www.w3.org/2000/svg">
    <text x="0" y="17" font-size="14" font-weight="900" font-family="Arial,sans-serif"
          fill="white" letter-spacing="0.5">RuPay</text>
  </svg>`,
};

/* ═══════════════════════════════════════════════════════════════
   4. STATE
   ═══════════════════════════════════════════════════════════════ */
const STATE = {
  step:           1,
  method:         'upi',
  orderId:        null,
  razorpayOrderId: null,
  upiTimerId:     null,
  upiSecondsLeft: 600,
  amounts: {
    base:     0,
    platform: 0,
    tax:      0,
    total:    0,
  },
};

/* ═══════════════════════════════════════════════════════════════
   5. RAZORPAY CLIENT
   ═══════════════════════════════════════════════════════════════ */
class RazorpayClient {
  constructor(cfg) {
    this.cfg = cfg;
  }

  /**
   * Creates an order via your backend or uses mock flow.
   * Returns { orderId, razorpayOrderId, amount }
   */
  async createOrder(amount, currency, receipt) {
    if (this.cfg.backend.mock) {
      // Mock: generate a local order ID and skip backend call.
      // Razorpay's checkout.js will handle the payment directly.
      return {
        orderId:         `ORD-${Date.now()}`,
        razorpayOrderId: null,   // No order ID in mock mode — checkout.js generates one
        amount,
        currency,
      };
    }

    const res = await fetch(this.cfg.backend.createUrl, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ amount, currency, receipt }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new PaymentError(err.message || `Order creation failed (HTTP ${res.status})`, 'ORDER_FAILED');
    }

    return res.json();
  }

  /**
   * Opens Razorpay's hosted checkout modal.
   * Returns a Promise that resolves with payment response or rejects on failure/dismiss.
   */
  openCheckout({ orderId, razorpayOrderId, amount, method, prefill }) {
    return new Promise((resolve, reject) => {
      const isDark = document.body.dataset.theme === 'dark';

      const options = {
        key:         this.cfg.razorpay.keyId,
        amount,                          // in paise
        currency:    this.cfg.razorpay.currency,
        name:        this.cfg.razorpay.name,
        description: this.cfg.razorpay.description,
        image:       this.cfg.razorpay.image,
        order_id:    razorpayOrderId,    // undefined/null in mock mode — that's fine
        prefill:     prefill || this.cfg.razorpay.prefill,
        theme:       {
          color: isDark ? '#6d90ff' : '#1e6cff',
        },
        modal: {
          ondismiss: () => reject(new PaymentError('Payment cancelled by user', 'CANCELLED')),
          escape:    true,
          animation: true,
        },
        handler: (response) => resolve(response),
      };

      // Pre-select payment method if possible
      if (method === 'upi') {
        options.method = { upi: true };
      } else if (method === 'credit' || method === 'debit') {
        options.method = { card: true };
      }

      const rzp = new Razorpay(options);
      rzp.on('payment.failed', (resp) => {
        reject(new PaymentError(
          resp.error?.description || 'Payment failed',
          resp.error?.code        || 'PAYMENT_FAILED'
        ));
      });
      rzp.open();
    });
  }

  /**
   * Verifies payment signature via backend.
   * Call after checkout.js callback to confirm authenticity.
   */
  async verifyPayment({ razorpay_payment_id, razorpay_order_id, razorpay_signature }) {
    if (this.cfg.backend.mock) {
      // In mock mode: skip server-side verification. Not safe for production.
      return { verified: true, transactionId: razorpay_payment_id };
    }

    const res = await fetch(this.cfg.backend.verifyUrl, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ razorpay_payment_id, razorpay_order_id, razorpay_signature }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new PaymentError(err.message || 'Payment verification failed', 'VERIFY_FAILED');
    }

    return res.json();
  }
}

class PaymentError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'PaymentError';
    this.code = code;
  }
}

const rzpClient = new RazorpayClient(CONFIG);

/* ═══════════════════════════════════════════════════════════════
   6. AMOUNT CALCULATOR
   ═══════════════════════════════════════════════════════════════ */
function calculateAmounts(baseAmountPaise) {
  const platform = Math.round(baseAmountPaise * CONFIG.order.platformFee);
  const subtotal = baseAmountPaise + platform;
  const tax      = Math.round(subtotal * CONFIG.order.gstRate);
  const total    = subtotal + tax;

  return { base: baseAmountPaise, platform, tax, total };
}

function formatINR(paise) {
  const rupees = paise / 100;
  return new Intl.NumberFormat('en-IN', {
    maximumFractionDigits: 0,
    minimumFractionDigits: 0,
  }).format(rupees);
}

function updateAmountUI(amounts) {
  STATE.amounts = amounts;

  const set = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.textContent = '₹' + formatINR(val);
  };

  set('pg-fee',      amounts.base);
  set('pg-platform', amounts.platform);
  set('pg-tax',      amounts.tax);
  set('pg-total',    amounts.total);
  set('pg-txn-amount', amounts.total);

  // Update all pay-amount spans
  document.querySelectorAll('.pg-pay-amount').forEach(el => {
    el.textContent = formatINR(amounts.total);
  });
}

/* ═══════════════════════════════════════════════════════════════
   7. URL PARAM READER — lets pricing cards pass product & amount
   ═══════════════════════════════════════════════════════════════ */
function readURLParams() {
  const params = new URLSearchParams(location.search);

  if (params.get('amount')) {
    const parsed = parseInt(params.get('amount'), 10);
    if (!isNaN(parsed) && parsed > 0) CONFIG.order.baseAmount = parsed * 100; // cents → paise
  }

  if (params.get('product')) {
    CONFIG.order.productName = decodeURIComponent(params.get('product'));
  }

  if (params.get('sub')) {
    CONFIG.order.productSub = decodeURIComponent(params.get('sub'));
  }

  // Update product name in DOM
  const nameEl = document.getElementById('pg-product-name');
  const subEl  = document.getElementById('pg-product-sub');
  if (nameEl) nameEl.textContent = CONFIG.order.productName;
  if (subEl)  subEl.textContent  = CONFIG.order.productSub;
}

/* ═══════════════════════════════════════════════════════════════
   8. VIEW & STEP MANAGEMENT
   ═══════════════════════════════════════════════════════════════ */
function showView(id) {
  document.querySelectorAll('.pg-view').forEach(v => v.classList.remove('active'));
  const target = document.getElementById(id);
  if (target) {
    target.classList.add('active');
    target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function setStep(n) {
  STATE.step = n;
  document.querySelectorAll('.pg-step').forEach((el, i) => {
    el.classList.toggle('active', i + 1 === n);
    el.classList.toggle('done',   i + 1 < n);
  });
  document.querySelectorAll('.pg-connector').forEach((el, i) => {
    el.classList.toggle('done', i + 1 < n);
  });
}

/* ═══════════════════════════════════════════════════════════════
   9. METHOD TABS (mirrors portfolio initAppTabs pattern)
   ═══════════════════════════════════════════════════════════════ */
function initMethodTabs() {
  const tabs  = document.querySelectorAll('.pg-tab');
  const panes = document.querySelectorAll('.pg-pane');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const method = tab.dataset.method;
      STATE.method = method;

      tabs.forEach(t => {
        t.classList.toggle('active', t === tab);
        t.setAttribute('aria-selected', String(t === tab));
      });

      panes.forEach(p => {
        p.classList.toggle('active', p.id === `pane-${method}`);
      });
    });
  });
}

/* ═══════════════════════════════════════════════════════════════
   10. UPI QR CODE GENERATION
   ═══════════════════════════════════════════════════════════════ */
function buildUPIString(orderId) {
  const params = new URLSearchParams({
    pa: CONFIG.upi.vpa,
    pn: CONFIG.razorpay.name,
    am: (STATE.amounts.total / 100).toFixed(2),
    cu: 'INR',
    tn: `Order-${orderId}`,
  });
  return `upi://pay?${params.toString()}`;
}

function generateUPIQR(upiString) {
  const container = document.getElementById('upi-qr-canvas');
  const shimmer   = document.getElementById('upi-qr-shimmer');

  if (!container || typeof QRCode === 'undefined') return;

  try {
    container.innerHTML = '';
    new QRCode(container, {
      text:         upiString,
      width:        168,
      height:       168,
      colorDark:    '#10131a',
      colorLight:   '#ffffff',
      correctLevel: QRCode.CorrectLevel.H,
    });
    if (shimmer) shimmer.classList.add('loaded');
  } catch (e) {
    console.warn('[PG] QR generation failed:', e.message);
  }
}

/* ═══════════════════════════════════════════════════════════════
   11. UPI COUNTDOWN TIMER
   ═══════════════════════════════════════════════════════════════ */
function startUPITimer() {
  clearInterval(STATE.upiTimerId);
  STATE.upiSecondsLeft = CONFIG.upi.qrExpiryMs / 1000;

  const display = document.getElementById('upi-countdown');
  const wrapper = document.getElementById('upi-timer');
  if (!display || !wrapper) return;

  STATE.upiTimerId = setInterval(() => {
    STATE.upiSecondsLeft--;

    const m = Math.floor(STATE.upiSecondsLeft / 60).toString().padStart(2, '0');
    const s = (STATE.upiSecondsLeft % 60).toString().padStart(2, '0');
    display.textContent = `${m}:${s}`;

    const isExpiring = STATE.upiSecondsLeft < 60;
    wrapper.classList.toggle('expiring', isExpiring);

    if (STATE.upiSecondsLeft <= 0) {
      clearInterval(STATE.upiTimerId);
      if (STATE.step === 1 && STATE.method === 'upi') {
        showFailure('QR code expired. Please refresh the page to generate a new one.');
      }
    }
  }, 1000);
}

/* ═══════════════════════════════════════════════════════════════
   12. LIVE CARD PREVIEW
   ═══════════════════════════════════════════════════════════════ */
function detectNetwork(pan) {
  const clean = pan.replace(/\s/g, '');
  if (/^4/.test(clean))             return 'visa';
  if (/^5[1-5]|^2[2-7]/.test(clean)) return 'mastercard';
  if (/^3[47]/.test(clean))         return 'amex';
  if (/^6[0-9]/.test(clean))        return 'rupay';
  return null;
}

function formatCardNumber(raw) {
  const digits = raw.replace(/\D/g, '').slice(0, 16);
  return digits.replace(/(.{4})/g, '$1 ').trim();
}

function maskCardDisplay(raw) {
  const digits = raw.replace(/\D/g, '').padEnd(16, '•');
  return digits.replace(/(.{4})/g, '$1 ').trim();
}

function initCardPreview(prefix) {
  const numInput    = document.getElementById(`${prefix}-number`);
  const nameInput   = document.getElementById(`${prefix}-name`);
  const expiryInput = document.getElementById(`${prefix}-expiry`);
  const cvvInput    = document.getElementById(`${prefix}-cvv`);
  const flipper     = document.getElementById(`${prefix}-flipper`);
  const numDisplay  = document.getElementById(`${prefix}-num-display`);
  const nameDisplay = document.getElementById(`${prefix}-name-display`);
  const expiryDisp  = document.getElementById(`${prefix}-expiry-display`);
  const cvvDisp     = document.getElementById(`${prefix}-cvv-display`);
  const networkDisp = document.getElementById(`${prefix}-network-display`);
  const logoSlot    = document.getElementById(`${prefix}-logo-slot`);

  if (!numInput) return;

  // ── Card number ──
  numInput.addEventListener('input', e => {
    const raw       = e.target.value.replace(/\D/g, '').slice(0, 16);
    e.target.value  = formatCardNumber(raw);
    if (numDisplay) numDisplay.textContent = maskCardDisplay(raw);

    const network = detectNetwork(raw);
    if (networkDisp) networkDisp.innerHTML = network ? (LOGOS[network] || '') : '';
    if (logoSlot)    logoSlot.innerHTML    = network ? (LOGOS[network] || '') : '';

    // Animate card glow when number is being entered
    if (flipper) flipper.classList.toggle('active-input', raw.length > 0 && raw.length < 16);
  });

  // ── Name ──
  nameInput.addEventListener('input', e => {
    if (nameDisplay) nameDisplay.textContent = e.target.value.toUpperCase() || 'FULL NAME';
  });

  // ── Expiry: auto-format MM/YY ──
  expiryInput.addEventListener('input', e => {
    let v = e.target.value.replace(/\D/g, '').slice(0, 4);
    if (v.length > 2) v = v.slice(0, 2) + '/' + v.slice(2);
    e.target.value = v;
    if (expiryDisp) expiryDisp.textContent = v || 'MM/YY';
  });

  // ── CVV: flip card ──
  cvvInput.addEventListener('focus', () => {
    if (flipper) flipper.classList.add('flipped');
  });
  cvvInput.addEventListener('blur', () => {
    if (flipper) flipper.classList.remove('flipped');
  });
  cvvInput.addEventListener('input', e => {
    const val = e.target.value.replace(/\D/g, '').slice(0, 4);
    e.target.value = val;
    if (cvvDisp) cvvDisp.textContent = val ? val.replace(/./g, '•') : '•••';
  });
}

/* ═══════════════════════════════════════════════════════════════
   13. APPLE PAY
   ═══════════════════════════════════════════════════════════════ */
function initApplePay() {
  const container = document.getElementById('apple-pay-btn-container');
  const fallback  = document.getElementById('apple-fallback');
  if (!container) return;

  // Check Web Payments API availability (Safari 16.4+ or Chrome with flag)
  if (window.PaymentRequest) {
    const methodData = [{
      supportedMethods: 'https://apple.com/apple-pay',
      data: {
        version:              3,
        merchantIdentifier:   CONFIG.applePay.merchantId,
        merchantCapabilities: CONFIG.applePay.merchantCapabilities,
        supportedNetworks:    CONFIG.applePay.supportedNetworks,
        countryCode:          CONFIG.applePay.countryCode,
      },
    }];

    const paymentDetails = {
      total: {
        label:  CONFIG.razorpay.name,
        amount: {
          currency: CONFIG.applePay.currencyCode,
          value:    (STATE.amounts.total / 100).toFixed(2),
        },
      },
    };

    // Try to create a PaymentRequest to check support
    try {
      const request = new PaymentRequest(methodData, paymentDetails);

      request.canMakePayment().then(canPay => {
        if (canPay) {
          // Render native <apple-pay-button> web component
          const btn = document.createElement('apple-pay-button');
          btn.setAttribute('buttonstyle', 'black');
          btn.setAttribute('type', 'pay');
          btn.setAttribute('locale', 'en-IN');
          container.appendChild(btn);

          btn.addEventListener('click', () => handleApplePayClick(methodData, paymentDetails));
        } else {
          showAppleFallback(container, fallback);
        }
      }).catch(() => showAppleFallback(container, fallback));

    } catch {
      showAppleFallback(container, fallback);
    }

  } else {
    showAppleFallback(container, fallback);
  }
}

function showAppleFallback(container, fallback) {
  if (container) {
    // Render a styled black pill button that degrades gracefully
    const btn = document.createElement('button');
    btn.className = 'pg-apple-btn-styled';
    btn.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
        <path d="M16.4 10.8c0-2.8 2.3-4.2 2.4-4.2-1.3-2-3.4-2.2-4.2-2.2-1.8-.2-3.5 1-4.4 1-.9 0-2.3-.9-3.8-.9C4 4.5 1.5 6.2 1.5 10c0 2.3.9 4.8 2.1 6.4 1.1 1.5 2.3 3.1 4 3.1 1.6 0 2.2-1 4.1-1 1.9 0 2.4 1 4.1 1 1.7 0 2.8-1.5 3.9-3 .7-1 1.2-2 1.2-2s-3.5-1.3-3.5-5.3z"/>
        <path d="M13.3 3c.9-1.1 1.5-2.6 1.5-4.1-1.4.1-3 .9-4 2-.9.9-1.5 2.3-1.5 3.7 1.3 0 2.8-.7 4-1.6z"/>
      </svg>
      Pay with Apple Pay
    `;
    btn.addEventListener('click', () => handleApplePayClick(null, null));
    container.appendChild(btn);
  }
  // Show fallback message only if the button also fails
}

async function handleApplePayClick(methodData, paymentDetails) {
  if (!methodData) {
    // Browser doesn't support Web Payments — show informational fallback
    const container = document.getElementById('apple-pay-btn-container');
    const fallback  = document.getElementById('apple-fallback');
    if (container) container.style.display = 'none';
    if (fallback)  fallback.hidden = false;
    return;
  }

  try {
    const request  = new PaymentRequest(methodData, paymentDetails);
    const response = await request.show();

    // Process the Apple Pay token through Razorpay
    setStep(2);
    showView('view-processing');
    updateProcessingStep(1);

    const { orderId } = await rzpClient.createOrder(
      STATE.amounts.total,
      CONFIG.razorpay.currency,
      `ORD-AP-${Date.now()}`
    );
    STATE.orderId = orderId;

    updateProcessingStep(2);

    // In a real integration, send response.details (Apple Pay token) to
    // your backend which processes it via Razorpay's Apple Pay API
    await response.complete('success');

    updateProcessingStep(3);
    showSuccess(orderId);

  } catch (e) {
    if (e.name !== 'AbortError') {
      showFailure(e.message || 'Apple Pay failed. Please try another method.');
    }
  }
}

/* ═══════════════════════════════════════════════════════════════
   14. FORM VALIDATION
   ═══════════════════════════════════════════════════════════════ */
function validateUPIId(id) {
  return /^[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}$/.test(id.trim());
}

function validateCardForm(prefix) {
  let valid = true;

  const validators = {
    [`${prefix}-number`]:  v => v.replace(/\s/g, '').length === 16,
    [`${prefix}-name`]:    v => v.trim().length >= 2,
    [`${prefix}-expiry`]:  v => /^\d{2}\/\d{2}$/.test(v) && isValidExpiry(v),
    [`${prefix}-cvv`]:     v => /^\d{3,4}$/.test(v),
  };

  for (const [id, validator] of Object.entries(validators)) {
    const input = document.getElementById(id);
    if (!input) continue;
    const ok = validator(input.value);
    input.classList.toggle('error', !ok);
    if (!ok) valid = false;
  }

  return valid;
}

function isValidExpiry(mmyy) {
  const [mm, yy] = mmyy.split('/');
  const now = new Date();
  const m   = parseInt(mm, 10);
  const y   = 2000 + parseInt(yy, 10);
  if (m < 1 || m > 12) return false;
  const expiry = new Date(y, m, 1);
  return expiry > now;
}

function clearErrors(prefix) {
  document.querySelectorAll(`#${prefix}-form .pg-input`).forEach(i => {
    i.classList.remove('error');
  });
}

/* ═══════════════════════════════════════════════════════════════
   15. PROCESSING STEPS UI
   ═══════════════════════════════════════════════════════════════ */
function updateProcessingStep(n) {
  const msgs = [
    'Initiating secure connection…',
    'Verifying payment details…',
    'Confirming transaction…',
  ];

  const sub = document.getElementById('pg-processing-msg');
  if (sub && msgs[n - 1]) sub.textContent = msgs[n - 1];

  document.querySelectorAll('.pg-proc-step').forEach((el, i) => {
    el.classList.toggle('active', i + 1 === n);
    el.classList.toggle('done',   i + 1 < n);
  });
}

/* ═══════════════════════════════════════════════════════════════
   16. PAYMENT SUBMISSION FLOWS
   ═══════════════════════════════════════════════════════════════ */
async function submitPayment() {
  setStep(2);
  showView('view-processing');
  updateProcessingStep(1);
  clearInterval(STATE.upiTimerId);

  try {
    // Step 1: Create order
    const { orderId, razorpayOrderId } = await rzpClient.createOrder(
      STATE.amounts.total,
      CONFIG.razorpay.currency,
      `ORD-${Date.now()}`
    );

    STATE.orderId         = orderId;
    STATE.razorpayOrderId = razorpayOrderId;

    updateProcessingStep(2);

    // Step 2: Open Razorpay checkout (handles all methods natively)
    const prefill = {};
    if (STATE.method === 'credit' || STATE.method === 'debit') {
      prefill.name = document.getElementById(`${STATE.method}-name`)?.value || '';
    }

    let paymentResponse;
    try {
      paymentResponse = await rzpClient.openCheckout({
        orderId,
        razorpayOrderId,
        amount:  STATE.amounts.total,
        method:  STATE.method,
        prefill,
      });
    } catch (e) {
      if (e.code === 'CANCELLED') {
        // User dismissed — go back to method selection
        setStep(1);
        showView('view-method');
        startUPITimer();
        return;
      }
      throw e;
    }

    updateProcessingStep(3);

    // Step 3: Verify payment
    const verification = await rzpClient.verifyPayment(paymentResponse);

    if (verification.verified) {
      showSuccess(paymentResponse.razorpay_payment_id || orderId);
    } else {
      showFailure('Payment verification failed. Please contact support.');
    }

  } catch (e) {
    const msg = e instanceof PaymentError
      ? e.message
      : 'An unexpected error occurred. Please try again.';
    showFailure(msg);
  }
}

/* ── UPI-specific: handle QR scan vs manual VPA ── */
async function submitUPI() {
  const upiInput = document.getElementById('upi-id-input');
  const upiId    = upiInput ? upiInput.value.trim() : '';

  // If UPI ID entered, validate it first
  if (upiId) {
    if (!validateUPIId(upiId)) {
      upiInput.classList.add('error');
      upiInput.focus();
      return;
    }
    upiInput.classList.remove('error');
    // Pre-fill the VPA in Razorpay options
    CONFIG.razorpay.prefill.vpa = upiId;
  }

  await submitPayment();
}

/* ════════════════════════════════════════════════════
   17. SUCCESS / FAILURE HANDLERS
   ════════════════════════════════════════════════════ */
function showSuccess(txnId) {
  setStep(3);
  clearInterval(STATE.upiTimerId);

  const txnEl = document.getElementById('pg-txn-id');
  if (txnEl) txnEl.textContent = txnId || '—';

  showView('view-success');
}

function showFailure(message) {
  setStep(3);
  clearInterval(STATE.upiTimerId);

  const msgEl = document.getElementById('pg-error-msg');
  if (msgEl) msgEl.textContent = message || 'Something went wrong. Please try again.';

  showView('view-failure');
}

/* ════════════════════════════════════════════════════
   18. BOOT
   ════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {

  // 18a. Read URL params (must run first)
  readURLParams();

  // 18b. Calculate and display amounts
  const amounts = calculateAmounts(CONFIG.order.baseAmount);
  updateAmountUI(amounts);

  // 18c. Init tabs
  initMethodTabs();

  // 18d. Generate UPI QR
  const dummyOrderId = `ORD-${Date.now()}`;
  STATE.orderId = dummyOrderId;
  generateUPIQR(buildUPIString(dummyOrderId));
  startUPITimer();

  // 18e. Init card previews
  initCardPreview('credit');
  initCardPreview('debit');

  // 18f. Init Apple Pay
  initApplePay();

  // 18g. Wire UPI submit
  const upiSubmit = document.getElementById('upi-submit');
  if (upiSubmit) {
    upiSubmit.addEventListener('click', submitUPI);
  }

  // 18h. Wire card submit buttons
  ['credit', 'debit'].forEach(prefix => {
    const btn = document.getElementById(`${prefix}-submit`);
    if (!btn) return;

    btn.addEventListener('click', () => {
      clearErrors(prefix);
      if (validateCardForm(prefix)) {
        submitPayment();
      } else {
        // Shake the button to indicate error
        btn.style.animation = 'none';
        btn.offsetHeight; // reflow
        btn.style.animation = 'pgShake 300ms ease';
        setTimeout(() => btn.style.animation = '', 300);
      }
    });
  });

  // 18i. Retry button
  const retryBtn = document.getElementById('pg-retry-btn');
  if (retryBtn) {
    retryBtn.addEventListener('click', () => {
      setStep(1);
      showView('view-method');
      // Restart UPI timer if UPI tab is active
      if (STATE.method === 'upi') startUPITimer();
    });
  }

  // 18j. Keyboard accessibility: Enter on UPI input submits
  const upiInput = document.getElementById('upi-id-input');
  if (upiInput) {
    upiInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') submitUPI();
    });
  }

  // 18k. Clear error on re-input
  document.querySelectorAll('.pg-input').forEach(input => {
    input.addEventListener('input', () => input.classList.remove('error'));
  });
});

/* ════════════════════════════════════════════════════
   19. KEYFRAME for shake animation (injected via JS
   so styles.css stays free of one-off animations)
   ════════════════════════════════════════════════════ */
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
  @keyframes pgShake {
    0%,100% { transform: translateX(0); }
    20%     { transform: translateX(-6px); }
    40%     { transform: translateX(6px); }
    60%     { transform: translateX(-4px); }
    80%     { transform: translateX(4px); }
  }
`;
document.head.appendChild(shakeStyle);
