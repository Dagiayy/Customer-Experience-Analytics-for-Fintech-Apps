
# Customer-Experience-Analytics-for-Fintech-Apps

## 📌 Overview

This project collects, cleans, and analyzes user reviews from the Google Play Store for three major Ethiopian mobile banking apps:

- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

The goal is to gather and preprocess **at least 600 reviews per bank** (1,800 total) to create a high-quality dataset for sentiment analysis, thematic analysis, and UX insights, as part of the Week 2 Challenge for Omega Consultancy. The challenge requires a minimum of 400 reviews per bank (1,200 total), but we aim for 600 to ensure robustness after preprocessing.

---

## 🛠 Tools & Technologies

| Tool / Library        | Purpose                                        |
|-----------------------|-----------------------------------------------|
| `google-play-scraper` | Extract app reviews from the Google Play Store |
| `pandas`              | Data cleaning and manipulation                 |
| `python-dateutil`     | Parsing and normalizing review dates           |
| `pytz`                | Timezone handling for date consistency         |
| `logging`             | Logging scraping progress and errors           |
| `os`, `time`          | File I/O and delays to avoid rate limiting     |

---

## 📂 File Structure

```
.
├── scraper/
│   └── main.py               # Main script for scraping and cleaning data
├── data/
│   └── bank_reviews.csv      # Output cleaned CSV file
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore file for excluding unnecessary files
└── README.md                 # Project documentation
```

---

## 🚀 How It Works

### 1. **Review Scraping**

- **App Identifiers**:
  - CBE: `com.combanketh.mobilebanking`
  - BOA: `com.boa.boaMobileBanking`
  - Dashen Bank: `com.dashen.dashensuperapp`
- **Scraping Process**:
  - Uses `google-play-scraper` to fetch reviews with:
    - Country: 🇪🇹 Ethiopia (`country='et'`)
    - Language: English (`lang='en'`)
    - Sorting: Newest first (`Sort.NEWEST`)
  - Targets **600 reviews per app** (1,800 total) to account for potential data loss during preprocessing.
  - Employs pagination with continuation tokens and retry logic (up to 3 retries with exponential backoff) to handle rate limits or errors.
- **Error Handling**:
  - Logs errors and retries failed requests to maximize review collection.
  - Warns if fewer than 600 reviews are collected per bank.

### 2. **Preprocessing**

- **Steps**:
  - Normalizes review timestamps to `YYYY-MM-DD` format using `python-dateutil`.
  - Removes:
    - Duplicate reviews (based on `review` text and `date`).
    - Reviews with missing or empty `review`, `rating`, or `date` fields.
  - Ensures `rating` is an integer (1–5 stars).
  - Adds metadata:
    - `bank`: Name of the bank (e.g., "Commercial Bank of Ethiopia").
    - `source`: Set to `Google Play`.
- **Output**:
  - Saves cleaned data to `data/bank_reviews.csv` with columns:
    - `review`: Review text
    - `rating`: Star rating (1–5)
    - `date`: Normalized date (YYYY-MM-DD)
    - `bank`: Bank name
    - `source`: Google Play

### 3. **Data Validation**

- Ensures:
  - **<5% missing or invalid data** after preprocessing.
  - **Minimum 400 reviews per bank** (challenge requirement), with a target of 600 for robustness.
- Logs:
  - Total reviews collected.
  - Number of reviews per bank.
  - Warnings for banks with fewer than 600 reviews (or 400 if not met).

---

## ⚠️ Challenges

- **Rate Limiting**: Google Play Store may restrict the number of reviews fetched, resulting in fewer than 600 reviews per bank (e.g., previous run collected 386–397 reviews per bank).
  - **Mitigation**: Smaller batch sizes (200 reviews), retry logic, and sleep delays (2–15 seconds) to avoid rate limits.
- **Limited Review Availability**: Some apps may have fewer than 600 reviews available in English from Ethiopia.
  - **Mitigation**: Log warnings and document in reports. The challenge allows pivoting to a fallback dataset if scraping fails.
- **Date Parsing**: Variations in date formats handled using `python-dateutil`’s robust parser.
- **Duplicates and Empty Reviews**: Filtered during preprocessing to ensure data quality.

---

## 📡 Git Workflow

- **Repository Setup**:
  - Created a GitHub repository with a `.gitignore` file excluding `.csv` files, virtual environments, and cache files.
  - Included `requirements.txt` with dependencies.
- **Branching**:
  - Work performed on the `task-1` branch.
  - Committed logical chunks (e.g., scraper script, CSV output) with meaningful messages.
- **Commits**:
  - Example: `Add review scraper with retry logic for 600 reviews per bank`.
  - Example: `Update bank_reviews.csv with preprocessed data`.
- **Pull Request**:
  - Merge `task-1` into `main` via a pull request for the interim submission (due 8:00 PM UTC, June 08, 2024).

---

## ▶️ Getting Started

### ✅ Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

**requirements.txt**:
```
google-play-scraper
pandas
python-dateutil
pytz
```

### ▶️ Run the Script

```bash
python -m scraper.main
```

- **Output**: Cleaned reviews saved to `data/bank_reviews.csv`.
- **Logs**: Display total reviews, reviews per bank, missing data, and warnings for shortfalls.

### 📂 Verify Output

- Check `data/bank_reviews.csv` for:
  - Columns: `review`, `rating`, `date`, `bank`, `source`.
  - At least 400 reviews per bank (target 600).
  - <5% missing data.

---

## 📝 Notes

- **Ethical Considerations**: Scraping is performed for educational purposes, adhering to Google Play’s terms of service.
- **Fallback Plan**: If 600 reviews per bank cannot be collected due to rate limits or limited review availability, the challenge allows using a backup dataset. This will be documented in the interim report.
