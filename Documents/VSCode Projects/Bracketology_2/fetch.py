import pandas as pd

def scrape_tables_from_url(url):
    try:
        # Use pandas read_html to directly convert HTML tables to dataframes
        dataframes_list = pd.read_html(url, flavor='bs4')

        return dataframes_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
url = 'https://www.sports-reference.com/cbb/boxscores/index.cgi?month=11&day=30&year=2023'  # Replace with the actual URL
result = scrape_tables_from_url(url)

# Display the list of dataframes
if result:
    for i, df in enumerate(result):
        print(f"DataFrame {i + 1}:\n{df}\n{'='*50}")

result[0].to_csv("test_df.csv")