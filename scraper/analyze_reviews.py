from turtle import up
import pandas as pd
import numpy as np
from transformers import pipeline
import spacy # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load the input data
input_file = 'data/bank_reviews.csv'
logger.info(f"Loading data from {input_file}")
df = pd.read_csv(input_file)

# Add a review_id column
df['review_id'] = range(1, len(df) + 1)

# Rename for consistency
df = df.rename(columns={'review': 'review_text'})

# Ensure required columns are present
required_columns = ['review_id', 'review_text', 'rating', 'date', 'bank', 'source']
df = df[required_columns]


# Initialize sentiment analysis pipeline
logger.info("Initializing sentiment analysis pipeline...")
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Perform sentiment analysis with corrected scoring
def get_sentiment(text):
    try:
        # Truncate text to 512 tokens (max for DistilBERT)
        text = " ".join(text.split()[:512])
        result = sentiment_pipeline(text)[0]
        label = result['label'].lower()
        score = result['score']
        # Map sentiment score: positive -> 0 to 1, negative -> -1 to 0
        if label == 'positive':
            sentiment_score = score  # 0 to 1
            sentiment_label = 'positive' if score >= 0.6 else 'neutral'
        else:  # negative
            sentiment_score = -score  # -1 to 0
            sentiment_label = 'negative' if score >= 0.6 else 'neutral'
        return sentiment_label, sentiment_score
    except Exception as e:
        logger.warning(f"Sentiment analysis failed for text: {text[:50]}... Error: {str(e)}")
        return 'neutral', 0.0

logger.info("Computing sentiment scores...")
sentiment_results = df['review_text'].apply(get_sentiment)
df['sentiment_label'] = [result[0] for result in sentiment_results]
df['sentiment_score'] = [result[1] for result in sentiment_results]

# Aggregate sentiment by bank and rating
sentiment_summary = df.groupby(['bank', 'rating'])['sentiment_score'].mean().reset_index()
logger.info("Sentiment summary by bank and rating:")
logger.info(sentiment_summary)

# Check KPI: Sentiment scores for 90%+ reviews
sentiment_coverage = (df['sentiment_score'] != 0).mean()
logger.info(f"Sentiment scores computed for {sentiment_coverage:.2%} of reviews")
if sentiment_coverage < 0.9:
    logger.warning("Sentiment scores computed for less than 90% of reviews")

# Text preprocessing for thematic analysis
logger.info("Loading spaCy model for preprocessing...")
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(tokens)

logger.info("Preprocessing review texts...")
df['processed_text'] = df['review_text'].apply(preprocess_text)

# Thematic Analysis: Extract keywords using TF-IDF
logger.info("Extracting keywords with TF-IDF...")
vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_df=0.8)
tfidf_matrix = vectorizer.fit_transform(df['processed_text'])
feature_names = vectorizer.get_feature_names_out()

# Function to get top keywords per bank
def get_top_keywords(bank_name, top_n=20):
    bank_reviews = df[df['bank'] == bank_name]['processed_text']
    if len(bank_reviews) < 5:
        return []
    bank_tfidf = vectorizer.transform(bank_reviews)
    avg_tfidf = bank_tfidf.mean(axis=0).A1
    top_indices = avg_tfidf.argsort()[-top_n:][::-1]
    return [feature_names[i] for i in top_indices]

# Extract keywords for each bank
banks = df['bank'].unique()
bank_keywords = {bank: get_top_keywords(bank) for bank in banks}
logger.info("Top keywords per bank:")
for bank, keywords in bank_keywords.items():
    logger.info(f"{bank}: {keywords}")

# Updated themes_dict with more keywords based on TF-IDF results
themes_dict = {
    'Commercial Bank of Ethiopia': {
        'Account Access Issues': ['login', 'password', 'access', 'sign', 'account', 'error'],
        'Transaction Performance': ['transfer', 'slow', 'speed', 'transaction', 'delay', 'fast'],
        'User Interface & Experience': ['ui', 'interface', 'design', 'navigate', 'easy', 'use', 'application', 'well', 'great', 'nice', 'excellent'],
        'Customer Support': ['support', 'service', 'help', 'response', 'customer', 'thank'],
        'Feature Requests': ['feature', 'update', 'add', 'option', 'fingerprint', 'screenshot']
    },
    'Bank of Abyssinia': {
        'Account Access Issues': ['login', 'error', 'access', 'account', 'sign'],
        'Transaction Performance': ['slow', 'transfer', 'payment', 'speed', 'fail', 'crash', 'time'],
        'User Interface & Experience': ['ui', 'design', 'navigation', 'look', 'use', 'mobile', 'banking', 'well', 'nice', 'good'],
        'Customer Support': ['support', 'help', 'service', 'contact', 'respond', 'fix'],
        'Feature Requests': ['feature', 'new', 'add', 'option', 'security', 'update']
    },
    'Dashen Bank': {
        'Account Access Issues': ['login', 'access', 'account', 'sign', 'error'],
        'Transaction Performance': ['transfer', 'slow', 'fast', 'payment', 'delay', 'step'],
        'User Interface & Experience': ['ui', 'design', 'navigate', 'user', 'friendly', 'easy', 'super', 'amazing', 'good', 'nice', 'wow', 'application'],
        'Customer Support': ['support', 'help', 'service', 'customer', 'response'],
        'Feature Requests': ['feature', 'update', 'add', 'option', 'login']
    }
}

# Grouping logic:
# - 'Account Access Issues': Keywords related to login problems, account access, or authentication.
# - 'Transaction Performance': Keywords about transaction speed, delays, or failures.
# - 'User Interface & Experience': Expanded to include general usability terms (e.g., 'good', 'nice', 'easy').
# - 'Customer Support': Keywords mentioning support, help, or customer service.
# - 'Feature Requests': Keywords indicating desired features or improvements.

# Assign themes to reviews
def assign_themes(review_text, bank_name):
    if not isinstance(review_text, str) or not review_text.strip():
        return []
    processed = preprocess_text(review_text)
    themes = []
    for theme, keywords in themes_dict[bank_name].items():
        if any(keyword in processed for keyword in keywords):
            themes.append(theme)
    return themes if themes else ['Other']

df['identified_themes'] = df.apply(lambda row: assign_themes(row['review_text'], row['bank']), axis=1)

# Check KPI: 3+ themes per bank
for bank in banks:
    bank_themes = set(themes_dict[bank].keys())
    logger.info(f"{bank} identified themes: {bank_themes}")
    if len(bank_themes) < 3:
        logger.warning(f"{bank} has fewer than 3 themes identified")

# Prepare final output
output_df = df[['review_id', 'review_text', 'sentiment_label', 'sentiment_score', 'identified_themes', 'bank', 'date']]
output_file = 'data/analyzed_reviews.csv'
os.makedirs('data', exist_ok=True)
output_df.to_csv(output_file, index=False, encoding='utf-8')
logger.info(f"Analysis results saved to {output_file}")

# Log final stats
total_reviews = len(df)
logger.info(f"Total reviews processed: {total_reviews}")
for bank in banks:
    bank_reviews = df[df['bank'] == bank]
    theme_counts = bank_reviews['identified_themes'].explode().value_counts()
    logger.info(f"\nTheme distribution for {bank}:")
    logger.info(theme_counts)