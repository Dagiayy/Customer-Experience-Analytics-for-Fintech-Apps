# scraper/utils.py

from dateutil import parser

def normalize_date(date_str):
    try:
        parsed_date = parser.parse(str(date_str))
        return parsed_date.strftime('%Y-%m-%d')
    except:
        return None
