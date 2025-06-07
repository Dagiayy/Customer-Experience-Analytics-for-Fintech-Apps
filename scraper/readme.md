
# 📊 Task 2: Sentiment & Thematic Analysis of Bank App Reviews

This task involves processing and analyzing customer reviews from fintech mobile apps to gain insights into customer sentiment and identify recurring themes across multiple banks. The results help stakeholders understand user satisfaction, common issues, and feature requests for better product decisions.

---

## 🚀 Features

* **Sentiment Analysis** using HuggingFace `transformers` (`distilbert-base-uncased-finetuned-sst-2-english`)
* **Theme Extraction** based on custom keyword rules per bank
* **TF-IDF-based Keyword Discovery** to guide thematic categorization
* **Support for multiple banks** (Commercial Bank of Ethiopia, Dashen Bank, Bank of Abyssinia)
* **KPI Tracking** (sentiment score coverage and theme variety)
* **Exportable Output** in CSV format (`analyzed_reviews.csv`)

---

## 📁 Directory Structure

```
Customer-Experience-Analytics-for-Fintech-Apps/
│
├── data/
│   ├── bank_reviews.csv         # Input file: raw reviews
│   └── analyzed_reviews.csv     # Output file: analyzed results
│
├── scraper/
│   └── analyze_reviews.py       # Main script for sentiment + theme analysis
│
├── README.md                    # This file
└── requirements.txt             # Python dependencies (recommended)
```

---

## 🧪 Requirements

Ensure you are in a Python virtual environment and run:

```bash
pip install -r requirements.txt
```

Recommended packages:

* `pandas`
* `numpy`
* `transformers`
* `spacy`
* `scikit-learn`
* `torch`
* `tqdm`

Also, download the spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

---

## 🛠️ How to Run

From the project root:

```bash
python scraper/analyze_reviews.py
```

---

## 📥 Input Format

The script expects a CSV file located at `data/bank_reviews.csv` with the following columns:

| Column Name | Description                             |
| ----------- | --------------------------------------- |
| `review`    | Raw review text                         |
| `rating`    | Star rating (1–5)                       |
| `date`      | Review date                             |
| `bank`      | Name of the bank (e.g., "Dashen Bank")  |
| `source`    | Source of the review (e.g., Play Store) |

---

## 📤 Output

The processed output is saved to `data/analyzed_reviews.csv` with the following columns:

| Column              | Description                                     |
| ------------------- | ----------------------------------------------- |
| `review_id`         | Unique ID assigned to each review               |
| `review_text`       | Original review text                            |
| `sentiment_label`   | `positive`, `neutral`, or `negative` sentiment  |
| `sentiment_score`   | Sentiment score ranging from -1 to 1            |
| `identified_themes` | List of thematic categories matched by keywords |

---

## 📌 Thematic Categories (per Bank)

Themes are assigned based on keyword matches. Each bank has its own dictionary of keywords for categories like:

* Account Access Issues
* Transaction Performance
* User Interface & Experience
* Customer Support
* Feature Requests

TF-IDF is used to identify the most common and relevant keywords in customer reviews.

---

## ✅ KPIs Checked

* Sentiment score computed for **≥90%** of reviews
* At least **3 themes per bank** are defined and assigned

---

## 📈 Sample Output (Log Summary)

```bash
INFO - Sentiment scores computed for 100.00% of reviews
INFO - Top keywords per bank:
INFO - Dashen Bank: ['good', 'app', 'transfer', ...]
INFO - Sentiment summary by rating:
  1 ★ → Strongly Negative
  5 ★ → Strongly Positive
INFO - Theme distribution for Dashen Bank:
Account Access Issues: 124
Transaction Performance: 89
...
```

---

## 🧠 Insights

This analysis enables:

* Data-driven understanding of customer pain points
* Prioritization of features and bug fixes
* Benchmarking banks against each other

---

## 🧾 License

This project is internal to **Kifiya**. Do not distribute externally without permission.

---

