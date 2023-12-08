import pandas as pd
from classes import *
import datetime
import re

def extract_name_rank(text: str):
    """
    Extracts team name and rank from text.
    """
    pattern = re.compile(r'([^()]+)(?: \((\d+)\))?')
    match = pattern.findall(text)
    name = match[0][0].rstrip()
    try:
        ranking = match[1][0]
    except:
        ranking = None
    return name, ranking

def parse_game(df: pd.DataFrame, date: datetime):
    """
    Takes a game dataframe and returns a Game object.
    """
    home, home_rank = extract_name_rank(df.iloc[1,1])
    away, away_rank = extract_name_rank(df.iloc[0,1])
    gender = df.iloc[2,1].split("'")[0]
    home_score = df.iloc[1,2]
    away_score = df.iloc[0,2]
    return Game(Team.search_team(home, gender), 
                Team.search_team(away, gender),
                home_score,
                away_score,
                gender,
                date)

def log_games_on_date(date: datetime):
    """
    Creates Game objects for all games on a given day.
    """
    url = f'https://www.sports-reference.com/cbb/boxscores/index.cgi?month={date.month}&day={date.day}&year={date.year}'  # Replace with the actual URL
    result = scrape_tables_from_url(url)
    games = []
    for df in result:
        games.append(parse_game(df, date))
    return games

def scrape_tables_from_url(url):
    """
    Given a URL, returns a list of tables on the webpage.
    """
    try:
        dataframes_list = pd.read_html(url, flavor='bs4')
        return dataframes_list
    except Exception as e:
        print(f"An error occurred: {e}\nURL: {url}")
        return []

def fetch_team_stats(season: int = 2024, gender: str = "men", refresh_override: bool = False):
    """
    Fetch and return team stats tables.
    """
    pages = ["school-stats","opponent-stats","advanced-school-stats","advanced-opponent-stats","ratings"]
    tables = {}
    for page in pages:
        url = f"https://www.sports-reference.com/cbb/seasons/{gender.lower()}/{season}-{page}.html"
        for i,table in enumerate(scrape_tables_from_url(url)):
            j = ""
            if i > 0:
                j = f"-{i}"
            tables[f"{page}{j}"] = table
    for key, value in tables.items():
        pass
    return tables
