# Customer-Experience-Analytics-for-Fintech-Apps

Here’s what you asked for:

---

## ✅ **Git Commit Message**

```bash
git add README.md .gitignore requirements.txt
git commit -m "Initialize project: add README, .gitignore, and requirements.txt"
```

---

## 📝 **General `README.md` for the Banking App Review Analysis Project**

```markdown
# Ethiopian Banking App Review Analysis

This project analyzes customer satisfaction with mobile banking apps in Ethiopia by collecting and processing user reviews from the Google Play Store. The goal is to provide data-driven insights and recommendations to improve app performance, user retention, and customer experience.

## 💼 Business Context

Omega Consultancy is assisting Ethiopian banks in identifying user pain points and satisfaction drivers in their mobile applications. As a Data Analyst, your responsibility is to collect, clean, analyze, and visualize review data for the following banks:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

## 🎯 Objectives

- Scrape Google Play Store app reviews.
- Preprocess the collected data for analysis.
- Perform sentiment and thematic analysis using NLP.
- Store cleaned data in an Oracle database.
- Visualize insights and recommend actionable improvements.

---

## 🛠️ Tech Stack

- Python 🐍
- `google-play-scraper` for web scraping
- Pandas & NumPy for data processing
- Git/GitHub for version control
- Oracle DB for storage (later stage)
- Jupyter Notebooks for exploratory analysis

---

## 📂 Project Structure

```

banking-app-reviews/
├── data/
│   ├── raw/                # Raw scraped reviews
│   └── cleaned/            # Cleaned & preprocessed reviews
├── scripts/
│   ├── scrape\_reviews.py   # Google Play scraping logic
│   └── preprocess\_reviews.py # Data cleaning script
├── .gitignore
├── README.md
├── requirements.txt
└── notebooks/

````

---

## 📦 Setup

### 1. Clone the repository

```bash
git clone https://github.com/Dagiayy/Customer-Experience-Analytics-for-Fintech-Apps.git
cd banking-app-reviews
````

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📌 Task 1: Data Collection & Preprocessing

### ✅ Subtasks

* [x] Create and set up GitHub repo
* [x] Scrape 400+ reviews per bank (CBE, BOA, Dashen)
* [x] Preprocess the reviews (remove duplicates, normalize dates)
* [x] Save final clean CSV for analysis

