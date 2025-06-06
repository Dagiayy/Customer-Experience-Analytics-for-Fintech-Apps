from google_play_scraper import reviews, Sort
from .utils import normalize_date
import time

def scrape_bank_reviews(bank_name, app_id, target_count):
    print(f"🔍 Scraping {target_count} reviews for {bank_name}...")
    all_reviews = []
    continuation_token = None
    max_attempts = 6
    attempt = 0

    try:
        while len(all_reviews) < target_count and attempt < max_attempts:
            remaining = min(200, target_count - len(all_reviews))
            result, continuation_token = reviews(
                app_id,
                lang='en',
                country='et',
                sort=Sort.NEWEST,
                count=remaining,
                continuation_token=continuation_token
            )

            fetched = len(result)
            if fetched == 0:
                attempt += 1
                print(f"⚠️ No new reviews fetched (attempt {attempt}/{max_attempts})")
            else:
                for review in result:
                    all_reviews.append({
                        'review': review['content'],
                        'rating': review['score'],
                        'date': normalize_date(review['at']),
                        'bank': bank_name,
                        'source': 'Google Play'
                    })
                print(f"  ➕ {fetched} reviews fetched (Total: {len(all_reviews)})")
                attempt = 0  # Reset attempt if we got data

            if not continuation_token:
                print("⛔ No continuation token — ending early.")
                break

            time.sleep(1)

        print(f"✅ Done: Collected {len(all_reviews)} reviews for {bank_name}")
        return all_reviews

    except Exception as e:
        print(f"❌ Error scraping {bank_name}: {str(e)}")
        return all_reviews
