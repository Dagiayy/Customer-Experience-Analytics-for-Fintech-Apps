import pandas as pd
import oracledb  # type: ignore
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Oracle credentials
username = "bank_reviews"
password = "BankReviews2025"
dsn = "localhost:1521/XEPDB1"

# Connect to Oracle
try:
    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    cursor = connection.cursor()
    logger.info("✅ Connected to Oracle database successfully")
except oracledb.Error as e:
    logger.error(f"❌ Failed to connect to Oracle DB: {e}")
    raise

# Function to create table if it does not exist
def create_table_if_not_exists(cursor, table_name, create_sql):
    try:
        # Check if table exists
        cursor.execute(f"SELECT COUNT(*) FROM user_tables WHERE table_name = '{table_name.upper()}'")
        result = cursor.fetchone()[0]
        if result == 0:
            cursor.execute(create_sql)
            logger.info(f"✅ {table_name} table created.")
        else:
            logger.info(f"⚠️ {table_name} table already exists. Skipping creation.")
    except oracledb.Error as e:
        logger.error(f"❌ Error during {table_name} table creation: {e}")
        raise

# Create Banks table if it doesn't exist
banks_create_sql = """
    CREATE TABLE Banks (
        bank_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        bank_name VARCHAR2(100) UNIQUE NOT NULL
    )
"""
create_table_if_not_exists(cursor, 'Banks', banks_create_sql)

# Create Reviews table if it doesn't exist
reviews_create_sql = """
    CREATE TABLE Reviews (
        review_id NUMBER PRIMARY KEY,
        bank_id NUMBER NOT NULL,
        review_text VARCHAR2(4000),
        rating NUMBER CHECK (rating BETWEEN 1 AND 5),
        review_date DATE,
        source VARCHAR2(50),
        sentiment_label VARCHAR2(20),
        sentiment_score NUMBER,
        identified_themes VARCHAR2(500),
        CONSTRAINT fk_bank FOREIGN KEY (bank_id) REFERENCES Banks(bank_id)
    )
"""
create_table_if_not_exists(cursor, 'Reviews', reviews_create_sql)

# Load CSV
input_file = 'data/analyzed_reviews.csv'
if not os.path.exists(input_file):
    logger.error(f"❌ File not found: {input_file}")
    raise FileNotFoundError(f"{input_file} not found")

df = pd.read_csv(input_file)
logger.info(f"✅ CSV loaded from {input_file}")

# Ensure necessary columns exist
required_columns = [
    'review_id', 'review_text', 'sentiment_label', 'sentiment_score',
    'identified_themes', 'bank', 'date'
]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    logger.error(f"❌ Missing columns in CSV: {missing_columns}")
    raise ValueError(f"Missing columns: {missing_columns}")

# Add default values
df['rating'] = 5
df['source'] = 'Google'

# Insert banks and build ID map
bank_id_map = {}
for bank_name in df['bank'].dropna().unique():
    cursor.execute("SELECT bank_id FROM Banks WHERE bank_name = :1", (bank_name,))
    existing = cursor.fetchone()
    if existing:
        bank_id_map[bank_name] = existing[0]
    else:
        bank_id_out = cursor.var(oracledb.NUMBER)
        cursor.execute("""
            INSERT INTO Banks (bank_name) VALUES (:bank_name)
            RETURNING bank_id INTO :bank_id_out
        """, {"bank_name": bank_name, "bank_id_out": bank_id_out})
        bank_id_map[bank_name] = int(bank_id_out.getvalue()[0])

connection.commit()
logger.info(f"✅ {len(bank_id_map)} banks processed and mapped")

# Map bank_id and clean data
df['bank_id'] = df['bank'].map(bank_id_map)
df['review_date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
df['identified_themes'] = df['identified_themes'].astype(str).str.slice(0, 500)

# Fetch existing review_ids to avoid duplicates
cursor.execute("SELECT review_id FROM Reviews")
existing_review_ids = set(row[0] for row in cursor.fetchall())
logger.info(f"🧠 {len(existing_review_ids)} existing review_ids loaded from DB")

# Prepare filtered review records
review_records = []
skipped_count = 0

for _, row in df.iterrows():
    if int(row['review_id']) in existing_review_ids:
        skipped_count += 1
        continue
    review_records.append((
        int(row['review_id']),
        int(row['bank_id']),
        row.get('review_text', ''),
        int(row.get('rating', 5)),
        row['review_date'],
        row.get('source', 'Google'),
        row.get('sentiment_label', ''),
        float(row.get('sentiment_score', 0)),
        row.get('identified_themes', '')
    ))

logger.info(f"✅ {len(review_records)} new reviews to insert, {skipped_count} skipped due to duplicates")

# Insert reviews
insert_review_sql = """
    INSERT INTO Reviews (review_id, bank_id, review_text, rating, review_date, source,
                         sentiment_label, sentiment_score, identified_themes)
    VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6, :7, :8, :9)
"""

try:
    if review_records:
        cursor.executemany(insert_review_sql, review_records)
        connection.commit()
        logger.info(f"✅ {len(review_records)} reviews inserted into the database")
    else:
        logger.info("ℹ️ No new reviews to insert")
except oracledb.Error as e:
    logger.error(f"❌ Failed to insert reviews: {e}")
    raise

# Count records
cursor.execute("SELECT COUNT(*) FROM Reviews")
total = cursor.fetchone()[0]
logger.info(f"📊 Total reviews in DB: {total}")

# Close connection
cursor.close()
connection.close()
logger.info("✅ Done. Oracle connection closed.")