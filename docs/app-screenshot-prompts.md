# iOS App Screenshot Prompts — Leonardo.AI (Flux Dev Model)

## Setup: Leonardo.AI (Free, 150 images/day)

1. Go to **app.leonardo.ai** → Sign up free (Google account works)
2. Click **"Image Generation"** in the left sidebar
3. **Settings to use every time:**
   - Model: **Flux Dev** (best for UI/app design)
   - Aspect Ratio: **9:19** (portrait phone)
   - Number of images: **4** (pick best one)
   - Negative Prompt: `text, words, readable labels, watermark, blurry, low quality, distorted, ugly UI`
4. Paste prompt → **Generate** → hover image → **Download PNG**
5. **Save with exact filename shown** into the matching folder under `assets/app-screenshots/`

---

## Pro Tips for Flux Dev
- Flux is far superior to Gemini for UI/app design — much more realistic
- If output has too much text: add `typography, text overlay, letters` to negative prompt
- Try the prompt once, if result is off regenerate — Flux gives varied outputs
- **Don't** overthink it — pick the one that looks most like a real iOS app screen

---

## App 1 — WealthKit (INDMoney / Zerodha style Finance App)
**Folder:** `assets/app-screenshots/wealthkit/`
**Color theme:** Dark navy blue + emerald green, dark mode

| File | Save as | Prompt |
|------|---------|--------|
| Dashboard | `screen-1.png` | photorealistic iOS finance app dashboard, dark navy blue background, top section shows large white portfolio balance number with small green up arrow percentage, center features a smooth donut chart with colored segments showing portfolio allocation, bottom section has a horizontal scrollable row of investment category cards, dark glassmorphism card style, emerald green and blue accent colors, bottom tab bar with 5 icons, ultra realistic mobile UI screenshot, 8k quality |
| Portfolio | `screen-2.png` | photorealistic iOS stock portfolio list screen, dark navy theme, vertical scrollable list of stock holding rows, each row has a small colorful circle logo on left, a tiny sparkline chart in center trending up or down, green positive and red negative percentage on right, subtle separator lines between rows, floating action button bottom right, clean dark mobile UI, Zerodha Kite style, ultra realistic screenshot |
| Mutual Funds | `screen-3.png` | photorealistic iOS mutual funds screen, dark navy blue background, top section has horizontal filter tab pills (All Equity Debt Hybrid), below is a 2-column grid of fund cards with gradient colored top section and white return percentage badge, each card has a simple pie chart icon, subtle card shadows, clean dark fintech UI, emerald green accents, ultra realistic mobile screenshot |
| Transactions | `screen-4.png` | photorealistic iOS transaction history screen, dark navy background, vertical list of transaction rows, each row has a round colored icon on left, center shows merchant category and date, right side shows credit amount in green or debit in red, thin horizontal dividers, calendar filter button at top, monthly section headers, clean dark mobile banking UI, ultra realistic screenshot |
| Goals | `screen-5.png` | photorealistic iOS financial goals tracker screen, dark navy background, 3 vertical goal cards each with a large circular progress ring in different colors (green for emergency fund, gold for retirement, teal for vacation), percentage number inside ring, thin progress bar below each card, target amount and current amount shown, glassmorphism card style, ultra realistic dark mobile UI screenshot |
| Profile | `screen-6.png` | photorealistic iOS finance app profile screen, dark navy background, top has circular user avatar with green verified checkmark badge, below shows KYC status card in dark glass style, 3 linked bank account rows each with bank logo color icon, toggle switches for notifications and biometrics, settings rows at bottom, clean dark mobile profile UI, ultra realistic screenshot |

---

## App 2 — SocialFlow (Instagram-style Social Media App)
**Folder:** `assets/app-screenshots/socialflow/`
**Color theme:** White background, purple-pink gradient accents

| File | Save as | Prompt |
|------|---------|--------|
| Feed | `screen-1.png` | photorealistic iOS social media app feed screen, white background, top has app logo and icons, below is vertical feed of posts, each post has circular user avatar with username on top row, large square photo content area below, bottom of post has heart icon like button, comment bubble icon, paper plane share icon, bookmark icon, bold like count below, clean modern Instagram-style mobile UI, ultra realistic screenshot |
| Stories | `screen-2.png` | photorealistic iOS stories bar component, white background, horizontal row of 6 circular story bubbles at top of screen, each bubble has a profile photo inside with thick colorful gradient ring border (pink to orange to yellow), first bubble has a plus icon for adding story, rest show friend avatars, story names below each circle in tiny font, ultra realistic iOS mobile UI screenshot |
| Reels | `screen-3.png` | photorealistic iOS reels vertical video screen, full bleed dark background video placeholder, gradient overlay darkening bottom third, right side has vertical column of action icons (heart, comment, share, more), creator circular profile avatar at bottom right with plus subscribe button, caption and music note row at bottom left, like count next to heart icon, ultra realistic TikTok slash Instagram Reels style mobile screenshot |
| Explore | `screen-4.png` | photorealistic iOS explore discovery grid screen, white background, top has search bar with filter icon, below search are horizontal scrolling topic chip pills with category icons, main area is a masonry grid of varied-height photo tiles with travel food fashion lifestyle images, some tiles span full width, others are half, clean Pinterest-style grid layout, ultra realistic iOS mobile screenshot |
| Post Detail | `screen-5.png` | photorealistic iOS post detail screen, white background, top 55% is a large square high quality photo, below photo row has heart like button and count, comment bubble icon, share icon, bookmark, below that is a horizontal strip of 3-4 small commenter circular avatars with plus count, comment input field at very bottom with send arrow button, pull-up sheet style bottom, ultra realistic iOS mobile screenshot |
| Profile | `screen-6.png` | photorealistic iOS user profile page, white background, circular profile photo centered at top with edit profile and settings buttons, horizontal stat bar showing Posts Followers Following with numbers, short bio area below, content type filter tabs (grid reels tagged), 3-column grid of square photo thumbnails filling the rest of the screen, clean Instagram-style profile page, ultra realistic mobile screenshot |

---

## App 3 — AppMarket (Apple App Store style)
**Folder:** `assets/app-screenshots/appmarket/`
**Color theme:** White background, iOS blue accent, Apple minimal

| File | Save as | Prompt |
|------|---------|--------|
| Today/Featured | `screen-1.png` | photorealistic iOS app store today tab screen, pure white background, top has large date heading and avatar, main area shows a full-width hero app feature card with colorful gradient background and large app icon inset, below are 2 smaller editorial story cards side by side with rounded corners, Apple App Store style layout, iOS blue accent buttons, ultra realistic mobile UI screenshot |
| Categories | `screen-2.png` | photorealistic iOS app categories grid screen, white background, section heading row, below is a 3-column grid of category tile buttons, each tile has a rounded square with a colorful gradient background (blue for games, green for health, orange for finance, purple for education, red for photo) and a white SF-style symbol icon centered, bottom navigation bar, ultra realistic Apple App Store style mobile screenshot |
| Search Results | `screen-3.png` | photorealistic iOS search results list screen, white background, top has prominent search bar with cancel button, below is a scrollable list of app search results, each row has rounded square app icon on far left, app name below that subtitle text, star rating with 5 stars and review count, price or GET badge on far right, thin separator lines, clean iOS list view, ultra realistic mobile screenshot |
| App Detail | `screen-4.png` | photorealistic iOS app detail page, white background, top row has large rounded square app icon left-aligned, app name to right, developer name smaller below, large blue GET button top right, below is star rating row with review count, horizontal scrollable screenshot previews strip showing 3 phone screenshots, below that ratings summary row, description text area, ultra realistic Apple App Store app page mobile screenshot |
| Ratings | `screen-5.png` | photorealistic iOS ratings and reviews page, white background, top section has giant rating score number centered with 5 star graphic below, subtitle showing number of ratings, below is a horizontal bar chart with 5 rows for 5 4 3 2 1 stars with filled proportion bars in blue, below that are 2 review cards each with user avatar, star rating row, review title and body text, ultra realistic iOS mobile screenshot |
| Updates | `screen-6.png` | photorealistic iOS app updates list screen, white background, section heading with update count badge, top has Update All blue button, below is vertical list of apps waiting for update, each row has rounded square app icon, version number badge, update file size, individual update button, separator lines, clean iOS settings-style list, ultra realistic mobile screenshot |

---

## App 4 — PaySwift (Paytm / PhonePe style Payments)
**Folder:** `assets/app-screenshots/payswift/`
**Color theme:** Deep navy blue with gold accent, dark style

| File | Save as | Prompt |
|------|---------|--------|
| Wallet Home | `screen-1.png` | photorealistic iOS digital wallet home screen, deep navy blue background, top shows user name greeting and profile avatar, center has a large rounded card in dark glass with wallet balance number in gold, below card are 4 quick action circular icon buttons (send money, add money, pay, scan QR) with icon glyphs, below that is a recent transactions mini list with 3 rows, gold and white accent colors, ultra realistic dark mobile payment app screenshot |
| Send Money | `screen-2.png` | photorealistic iOS send money screen, deep navy blue background, top has back arrow and title, recipient search bar below, scrollable contact list with circular user avatars and phone numbers, frequently sent contacts row at top of list, bottom section has a numeric keypad and send button in gold, clean dark payment app UI, ultra realistic mobile screenshot |
| QR Scanner | `screen-3.png` | photorealistic iOS QR code scanner screen, very dark near-black background with camera viewfinder, centered square scanning frame with animated corner L-shaped brackets in gold, subtle grid overlay in viewfinder, merchant info card slides up from bottom of screen showing merchant logo circle, amount entry field, pay button in gold, flashlight toggle top corner, ultra realistic dark mobile payment screenshot |
| History | `screen-4.png` | photorealistic iOS payment transaction history list, deep navy background, date group headers (Today Yesterday), each transaction row has colored circular merchant logo icon left, transaction type label area center, credit amount in gold or debit in white right, small timestamp below, thin separator lines, filter chips at top, clean dark transaction history UI, ultra realistic mobile screenshot |
| Offers | `screen-5.png` | photorealistic iOS cashback and rewards offers screen, deep navy background, section heading with offers count, 2-column grid of offer cards, each card has dark glass background, brand logo icon centered, large gold percentage cashback badge overlay top right, validity date bar at bottom of card, subtle card border glow, ultra realistic dark promotional offers UI mobile screenshot |
| Profile | `screen-6.png` | photorealistic iOS wallet user profile screen, deep navy background, circular user photo avatar top center with gold verified badge, balance summary card below in dark glass with gold number, linked accounts section with bank logo pills, UPI IDs list with copy icons, biometric toggle row, security settings rows, clean dark financial profile mobile UI, ultra realistic screenshot |

---

## App 5 — ShopEase (Amazon / Meesho style E-Commerce)
**Folder:** `assets/app-screenshots/shopeasy/`
**Color theme:** Vibrant orange + white, energetic retail style

| File | Save as | Prompt |
|------|---------|--------|
| Home | `screen-1.png` | photorealistic iOS e-commerce app home screen, white background, top has search bar with camera and mic icons and cart icon, below is a bold orange promotional banner carousel with sale percentage badge, below banner is a horizontal category icon row (Electronics Fashion Food Beauty Sports), below that is a Today's Deals section with horizontal product card strip, clean modern retail app UI, ultra realistic mobile screenshot |
| Product Listing | `screen-2.png` | photorealistic iOS product listing grid screen, white background, top has active search query chip and filter sort buttons, main area is a 2-column grid of product cards, each card has product photo top 65%, product name below, bold orange price, lighter crossed-out original price, small star rating row, subtle card shadow, clean shopping grid UI, ultra realistic mobile screenshot |
| Product Detail | `screen-3.png` | photorealistic iOS product detail page, white background, top has large product image with image dot indicator and wishlist heart icon overlay, below is product name, star rating row with review count, bold orange discounted price with strikethrough original price, size or color variant selector row with rounded option buttons, quantity row, full-width orange Add to Cart button, ultra realistic mobile e-commerce screenshot |
| Cart | `screen-4.png` | photorealistic iOS shopping cart screen, white background, top heading with item count badge, vertical list of 3 cart items each with product thumbnail left, product name and variant center, quantity minus-number-plus stepper right, price, remove trash icon, below list is a promo code input row, order summary card with subtotal delivery discount total, large orange Proceed to Checkout button, ultra realistic mobile screenshot |
| Checkout | `screen-5.png` | photorealistic iOS checkout flow screen, white background, step progress indicator at top (3 steps: Address Payment Review), current step is Payment, shows saved delivery address card with edit button, payment method section with credit card debit card UPI wallet options as selectable rows with radio buttons, order total summary at bottom, large orange Place Order button, ultra realistic mobile checkout screenshot |
| Order Tracking | `screen-6.png` | photorealistic iOS order tracking screen, white background, top has order number and estimated delivery date card in light orange, below is a vertical step timeline with 4 steps: Order Placed (checked green) Processing (checked green) Shipped (current step in orange with pulsing dot) Delivered (upcoming gray), each step has icon and date, delivery partner info card at bottom, ultra realistic clean mobile tracking screenshot |

---

## File Naming — Drop images here after generating:

```
assets/app-screenshots/
├── wealthkit/
│   ├── screen-1.png   ← Dashboard
│   ├── screen-2.png   ← Portfolio
│   ├── screen-3.png   ← Mutual Funds
│   ├── screen-4.png   ← Transactions
│   ├── screen-5.png   ← Goals
│   └── screen-6.png   ← Profile
├── socialflow/
│   ├── screen-1.png   ← Feed
│   ├── screen-2.png   ← Stories
│   ├── screen-3.png   ← Reels
│   ├── screen-4.png   ← Explore
│   ├── screen-5.png   ← Post Detail
│   └── screen-6.png   ← Profile
├── appmarket/
│   ├── screen-1.png   ← Today/Featured
│   ├── screen-2.png   ← Categories
│   ├── screen-3.png   ← Search Results
│   ├── screen-4.png   ← App Detail
│   ├── screen-5.png   ← Ratings
│   └── screen-6.png   ← Updates
├── payswift/
│   ├── screen-1.png   ← Wallet Home
│   ├── screen-2.png   ← Send Money
│   ├── screen-3.png   ← QR Scanner
│   ├── screen-4.png   ← History
│   ├── screen-5.png   ← Offers
│   └── screen-6.png   ← Profile
└── shopeasy/
    ├── screen-1.png   ← Home
    ├── screen-2.png   ← Product Listing
    ├── screen-3.png   ← Product Detail
    ├── screen-4.png   ← Cart
    ├── screen-5.png   ← Checkout
    └── screen-6.png   ← Order Tracking
```

---

## After uploading all 30 images

Tell Claude: **"Screenshots are ready, proceed with Phase B"**
Claude will build preview.html + redesign the entire portfolio apps section immediately.
