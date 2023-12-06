import pandas as pd
from classes import *
import datetime

def scrape_tables_from_url(url):
    """
    Given a URL, returns a list of tables on the webpage.
    """
    try:
        dataframes_list = pd.read_html(url, flavor='bs4')
        return dataframes_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
date = datetime.date(2023,11,7)
url = f'https://www.sports-reference.com/cbb/boxscores/index.cgi?month={date.month}&day={date.day}&year={date.year}'  # Replace with the actual URL

stats = ["school","opponent","advanced-school","advanced-opponent"]
stat = stats[0]
gender = "men"
season = 2024
url = f"https://www.sports-reference.com/cbb/seasons/{gender.lower()}/{season}-{stat}-stats.html"
result = scrape_tables_from_url(url)

# Display the list of dataframes
if result:
    for i, df in enumerate(result):
        print(f"DataFrame {i + 1}:\n{df}\n{'='*50}")