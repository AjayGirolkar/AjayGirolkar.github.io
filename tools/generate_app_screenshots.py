"""
generate_app_screenshots.py
----------------------------
Uses OpenAI DALL-E 3 to generate realistic iOS app UI screenshots
for 5 app categories. Saves images to assets/app-screenshots/{app-slug}/.

Usage:
    python3 tools/generate_app_screenshots.py

Requirements:
    pip install openai python-dotenv

Output:
    assets/app-screenshots/
        wealthkit/screen-1.png ... screen-6.png
        socialflow/screen-1.png ... screen-6.png
        appmarket/screen-1.png  ... screen-6.png
        payswift/screen-1.png   ... screen-6.png
        shopeasy/screen-1.png   ... screen-6.png
"""

import os
import sys
import time
import urllib.request
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ── Load .env from project root ────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
OUTPUT_ROOT = ROOT / "assets" / "app-screenshots"

# ── App configurations ─────────────────────────────────────────────────────────
APPS = {
    "wealthkit": {
        "display_name": "WealthKit",
        "category": "Finance & Investment",
        "color": "deep blue and emerald green gradient, dark mode",
        "screens": [
            ("dashboard",     "investment portfolio overview with circular donut chart showing allocation, total portfolio balance prominently displayed at top, percentage gains in green"),
            ("portfolio",     "list of stock holdings with small sparkline charts, company logos, current price and P&L in green and red"),
            ("mutualfunds",   "mutual fund categories grid with return percentage badges, fund type labels, star ratings, invest button"),
            ("transactions",  "chronological transaction history list with credit debit amounts, merchant icons, date stamps, balance"),
            ("goals",         "financial goals tracker screen with circular progress rings, goal name labels, target amount progress bars"),
            ("profile",       "user account profile with KYC verification badges, linked bank account cards, security settings icons"),
        ],
    },
    "socialflow": {
        "display_name": "SocialFlow",
        "category": "Social Media",
        "color": "clean white background with vibrant purple-pink gradient accents",
        "screens": [
            ("feed",      "social media scrollable photo feed with square image posts, heart like button, comment icon, user avatar and username above each post"),
            ("stories",   "horizontal row of circular story bubbles with user profile photos and gradient ring borders, story progress bars at top"),
            ("reels",     "fullscreen vertical video reel interface with like heart counter on right side, creator username, caption text overlay at bottom"),
            ("explore",   "grid discovery page with varied size image tiles in masonry layout, trending hashtag chips at top"),
            ("post",      "single post detail view with large image, comment thread below, reply input field, like count"),
            ("profile",   "user profile page with avatar photo header, follower following post counts, bio text, 3 column photo grid below"),
        ],
    },
    "appmarket": {
        "display_name": "AppMarket",
        "category": "App Discovery",
        "color": "clean white with blue accent colors, Apple-style minimal",
        "screens": [
            ("featured",    "app store today tab with large hero featured app card spanning full width, daily highlights section, editorial story cards"),
            ("categories",  "app categories grid with colorful icon tiles, Games Productivity Lifestyle Finance Education Health labels"),
            ("search",      "search results list view with app icons on left, app name and subtitle, star rating, price or free badge on right"),
            ("detail",      "single app detail page with large app icon, title, developer name, screenshot carousel thumbnails, install button, description"),
            ("ratings",     "app ratings detail page with overall score large number, star distribution bar chart, written review cards"),
            ("updates",     "pending app updates list with app icons, update size, changelog text preview, update all button at top"),
        ],
    },
    "payswift": {
        "display_name": "PaySwift",
        "category": "Payments & Wallet",
        "color": "deep navy blue with gold and white accents",
        "screens": [
            ("wallet",      "digital wallet home with large balance display at top, quick action buttons send receive pay, recent transaction mini cards"),
            ("sendmoney",   "send money screen with contact list showing profile photos and names, numeric keypad for amount entry, send button"),
            ("qrscan",      "QR code scanner camera viewfinder with rounded scanning frame corners, merchant name and amount displayed below"),
            ("history",     "payment transaction history with merchant logos, transaction names, debit credit amounts, timestamps, categories"),
            ("offers",      "cashback and rewards offers grid with percentage discount badge overlays, brand logos, validity dates"),
            ("profile",     "user financial profile with avatar, wallet balance card, linked bank accounts list, UPI IDs, security settings"),
        ],
    },
    "shopeasy": {
        "display_name": "ShopEase",
        "category": "E-Commerce",
        "color": "vibrant orange and white with accent teal, energetic retail style",
        "screens": [
            ("home",       "e-commerce home screen with promotional banner carousel at top, horizontal category icon row, product recommendation cards grid"),
            ("listing",    "product listing grid with product photo cards, product name, price, star rating, discount badge overlay"),
            ("detail",     "product detail page with large product image gallery, title, price with strikethrough original price, add to cart button"),
            ("cart",       "shopping cart with product thumbnail list, quantity stepper, item prices, subtotal order summary, checkout button"),
            ("checkout",   "checkout screen with delivery address section, payment method selector cards, order total breakdown, place order button"),
            ("tracking",   "order tracking screen with vertical timeline steps, courier icon, estimated delivery date, package status labels"),
        ],
    },
}

PROMPT_TEMPLATE = (
    "iOS mobile app UI screenshot, {app_name} app ({category}), "
    "{screen_description}. "
    "Color scheme: {color}. "
    "Ultra clean modern iOS design, no real text readable, minimal, professional, "
    "pixel-perfect UI components, realistic mobile interface, "
    "soft shadows, rounded corners, status bar at top, bottom navigation bar. "
    "Portrait orientation phone screen only, no device frame, pure app content. "
    "High quality, sharp edges, award-winning app design."
)


def download_image(url: str, dest: Path) -> None:
    """Download image from URL to dest path."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
        f.write(resp.read())


def generate_screenshots() -> None:
    total = sum(len(cfg["screens"]) for cfg in APPS.values())
    done = 0

    for slug, cfg in APPS.items():
        app_dir = OUTPUT_ROOT / slug
        app_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'─'*60}")
        print(f"  {cfg['display_name']}  ({cfg['category']})")
        print(f"{'─'*60}")

        for i, (screen_name, description) in enumerate(cfg["screens"], start=1):
            dest = app_dir / f"screen-{i}.png"

            if dest.exists():
                print(f"  [{i}/6] {screen_name} — already exists, skipping")
                done += 1
                continue

            prompt = PROMPT_TEMPLATE.format(
                app_name=cfg["display_name"],
                category=cfg["category"],
                screen_description=description,
                color=cfg["color"],
            )

            print(f"  [{i}/6] Generating: {screen_name}...", end=" ", flush=True)
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1792",
                    quality="standard",
                    n=1,
                )
                image_url = response.data[0].url
                download_image(image_url, dest)
                done += 1
                print(f"✓  ({done}/{total} total)")
            except Exception as e:
                print(f"✗  ERROR: {e}")
                # Continue on error — don't abort entire batch
                continue

            # Brief pause to avoid rate limits
            if i < len(cfg["screens"]):
                time.sleep(1)

    print(f"\n{'='*60}")
    print(f"  Done! {done}/{total} screenshots saved to:")
    print(f"  {OUTPUT_ROOT}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print("\n iOS App Screenshot Generator (DALL-E 3)")
    print(" ─────────────────────────────────────────")
    print(f"  Generating {sum(len(c['screens']) for c in APPS.values())} screenshots across {len(APPS)} apps\n")

    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment.")
        print("Make sure .env file exists at project root with OPENAI_API_KEY=sk-...")
        sys.exit(1)

    generate_screenshots()
