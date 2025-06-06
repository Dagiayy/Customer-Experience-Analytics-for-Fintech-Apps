# scraper/main.py

import os
import pandas as pd
from scraper.config import BANK_APPS, OUTPUT_FILE
from scraper.scraper import scrape_bank_reviews

def main():
    all_reviews = []

    for bank, (app_id, target_count) in BANK_APPS.items():
        bank_reviews = scrape_bank_reviews(bank, app_id, target_count)
        all_reviews.extend(bank_reviews)

    if not all_reviews:
        print("⚠️ No reviews collected. Exiting.")
        return

    df = pd.DataFrame(all_reviews)

    # Data cleaning
    df.drop_duplicates(subset=['review', 'date'], inplace=True)
    df.dropna(subset=['review', 'rating', 'date'], inplace=True)
    df['rating'] = df['rating'].astype(int)

    print(f"\n📊 Total cleaned reviews: {len(df)}")
    print("🧼 Missing values:\n", df.isnull().sum())

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"💾 Saved to {OUTPUT_FILE}")

    print("\n📈 Review count per bank:")
    print(df['bank'].value_counts())

    for bank, (_, target) in BANK_APPS.items():
        count = df[df['bank'] == bank].shape[0]
        if count < target:
            print(f"⚠️ {bank} has only {count} reviews (target: {target})")

if __name__ == '__main__':
    main()
