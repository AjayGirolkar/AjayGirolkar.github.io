# How to Screenshot All 30 Screens from Xcode Canvas

## One-time Setup (5 minutes)

1. Open **Xcode** → File → New → Project
2. Choose: **iOS** → **App** → Next
3. Name: `PortfolioScreenshots`, Interface: **SwiftUI**, Language: **Swift**
4. Create the project anywhere on your Mac
5. In the Project Navigator (left panel), create a folder called `Screens`
6. **Drag all 6 Swift files** from this folder into Xcode:
   - `Shared.swift`
   - `WealthKit.swift`
   - `SocialFlow.swift`
   - `AppMarket.swift`
   - `PaySwift.swift`
   - `ShopEase.swift`
7. When asked "Copy items if needed" → check it → Add

---

## How to Screenshot Each Screen

### Step 1 — Open a Swift file
Click `WealthKit.swift` in the Navigator

### Step 2 — Open Canvas
Press **⌘ + Option + Return** (or Editor menu → Canvas)
The Canvas will appear on the right side showing all 6 previews

### Step 3 — Screenshot each preview
- Click on a preview in Canvas to select it
- Press **⌘ + Shift + 5** → screenshot
- Drag to capture just that one phone preview
- **OR**: Right-click the preview → Save As... (if available in your Xcode version)

### Alternative — Simulator screenshot
1. Click ▶ Run button (any simulator, iPhone 15 Pro recommended)
2. Simulator opens showing the app
3. Press **⌘ + S** in the Simulator to save screenshot to Desktop

---

## File Naming — Save screenshots here

```
PortfolioProject/assets/app-screenshots/
├── wealthkit/
│   ├── screen-1.png   ← WealthKit Dashboard    (#Preview "1 Dashboard")
│   ├── screen-2.png   ← Portfolio              (#Preview "2 Portfolio")
│   ├── screen-3.png   ← Mutual Funds           (#Preview "3 MutualFunds")
│   ├── screen-4.png   ← Transactions           (#Preview "4 Transactions")
│   ├── screen-5.png   ← Goals                  (#Preview "5 Goals")
│   └── screen-6.png   ← Profile                (#Preview "6 Profile")
├── socialflow/
│   ├── screen-1.png   ← Feed                   (#Preview "1 Feed")
│   ├── screen-2.png   ← Stories                (#Preview "2 Stories")
│   ├── screen-3.png   ← Reels                  (#Preview "3 Reels")
│   ├── screen-4.png   ← Explore                (#Preview "4 Explore")
│   ├── screen-5.png   ← Post Detail            (#Preview "5 Post Detail")
│   └── screen-6.png   ← Profile                (#Preview "6 Profile")
├── appmarket/
│   ├── screen-1.png   ← Today / Featured       (#Preview "1 Today")
│   ├── screen-2.png   ← Categories             (#Preview "2 Categories")
│   ├── screen-3.png   ← Search                 (#Preview "3 Search")
│   ├── screen-4.png   ← App Detail             (#Preview "4 App Detail")
│   ├── screen-5.png   ← Ratings & Reviews      (#Preview "5 Ratings")
│   └── screen-6.png   ← Updates                (#Preview "6 Updates")
├── payswift/
│   ├── screen-1.png   ← Wallet Home            (#Preview "1 Wallet")
│   ├── screen-2.png   ← Send Money             (#Preview "2 Send")
│   ├── screen-3.png   ← QR Scanner             (#Preview "3 QR Scan")
│   ├── screen-4.png   ← Transaction History    (#Preview "4 History")
│   ├── screen-5.png   ← Offers                 (#Preview "5 Offers")
│   └── screen-6.png   ← Profile                (#Preview "6 Profile")
└── shopeasy/
    ├── screen-1.png   ← Home                   (#Preview "1 Home")
    ├── screen-2.png   ← Product Listing         (#Preview "2 Listing")
    ├── screen-3.png   ← Product Detail          (#Preview "3 Detail")
    ├── screen-4.png   ← Cart                    (#Preview "4 Cart")
    ├── screen-5.png   ← Checkout                (#Preview "5 Checkout")
    └── screen-6.png   ← Order Tracking          (#Preview "6 Tracking")
```

---

## When done

Tell Claude: **"Screenshots are ready, proceed with Phase B"**

Claude will immediately:
1. Build `preview.html` to review all 30 screens
2. Redesign the portfolio `#apps` section with real screenshots
3. Add "View App Flow →" show-more feature
4. Wire GitHub CTA buttons for each app

---

## Tips

- **iPhone 15 Pro** simulator gives the best screenshot resolution (2556×1179px)
- Canvas previews render at device size — crop out the Canvas chrome if needed
- If Canvas says "Automatic preview updates paused", click **Resume** button
- If a file shows errors, make sure `Shared.swift` is added to the project first
