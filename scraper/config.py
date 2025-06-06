# scraper/config.py

# Define app IDs for the three banks based on provided URLs
BANK_APPS = {
    'Commercial Bank of Ethiopia': ('com.combanketh.mobilebanking', 800),
    'Bank of Abyssinia': ('com.boa.boaMobileBanking', 800),
    'Dashen Bank': ('com.dashen.dashensuperapp', 800),
}



OUTPUT_FILE = 'data/bank_reviews.csv'
