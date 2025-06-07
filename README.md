## Task 3: Store Cleaned Data in Oracle

### Methodology
- **Objective**: Store the cleaned and processed review data in an Oracle database.
- **Setup**:
  - Installed Oracle Database Express Edition (XE) 21c.
  - Created a user `bank_reviews` with schema `bank_reviews`.
- **Schema**:
  - `Banks` table: `bank_id` (primary key), `bank_name` (unique).
  - `Reviews` table: `review_id` (primary key), `bank_id` (foreign key), `review_text`, `rating`, `review_date`, `source`, `sentiment_label`, `sentiment_score`, `identified_themes`.
- **Data Insertion**:
  - Used `oracledb` Python driver to connect to Oracle XE.
  - Inserted 1,997 reviews from `data/analyzed_reviews.csv` into the `Reviews` table.
- **Output**:
  - Exported database schema and data as `data/bank_reviews_dump.sql` using Oracle SQL Developer.
- **Data Quality**:
  - Populated tables with 1,997 entries (exceeding the KPI of >1,000 entries).

### Files
- `scraper/load_to_oracle.py`: Script to create tables and insert data into Oracle.
- `bank_reviews_dump.sql`: SQL dump of the database.