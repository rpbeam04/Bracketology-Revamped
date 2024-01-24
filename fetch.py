import pandas as pd
from classes import *
import datetime
import re
import os
from pprint import *
from bs4 import BeautifulSoup
import requests
import time

def extract_name_rank(text: str):
    """
    Extracts team name and rank from text.
    """
    if not isinstance(text, str):
        print("Error (name_rank): Input is not string.")
        print(text)
        return text, None
    text = text.replace("\u00a0"," ")
    text = text.replace("\u2013","-")
    pattern = re.compile(r'\ \(\d+\)')
    match = pattern.findall(text)
    if len(match) == 1:
        name = text.removesuffix(match[0])
        ranking = int(match[0].replace("(","").replace(")",""))
    else:
        if len(match) > 1:
            print("Error (regex): multiple matches.")
        name = text
        ranking = None
    return name, ranking

def parse_game(df: pd.DataFrame, date: datetime.datetime):
    """
    Takes a game dataframe and returns a Game object.
    """
    if not isinstance(df.iloc[1,0], str) or not isinstance(df.iloc[0,0], str):
        return None
    home, home_rank = extract_name_rank(df.iloc[1,0])
    away, away_rank = extract_name_rank(df.iloc[0,0])
    try:
        gender = df.iloc[2,1].split("'")[0].lower()
    except:
        gender = "women"
        print("Error (game): No gender.")
    try:
        home_score = int(df.iloc[1,1])
    except:
        home_score = 0
    try:
        away_score = int(df.iloc[0,1])
    except:
        away_score = 0
    try:
        return Game(Team.search_team(home, gender), 
                    Team.search_team(away, gender),
                    home_score,
                    away_score,
                    gender,
                    date)
    except:
        return None

def fetch_games_on_date(date: datetime.datetime, refresh: bool = True):
    """
    Creates Game objects for all games on a given day.
    """
    url = fr'https://www.sports-reference.com/cbb/boxscores/index.cgi?month={date.month}&day={date.day}&year={date.year}'  # Replace with the actual URL
    filename = fr"Webpages/{date.year}_{date.month}_{date.day}_games.html"

    if refresh:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Games on {date.month}/{date.day}/{date.year} scraped.")
            with open(filename, 'w', encoding='utf-8') as html_file:
                html_file.write(response.text)
        else:
            print(f"Failed to fetch webpage. Status code: {response.status_code}")
            return None
    elif not refresh and not os.path.exists(filename):
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Games on {date.month}/{date.day}/{date.year} scraped.")
            with open(filename, 'w', encoding='utf-8') as html_file:
                html_file.write(response.text)
        else:
            print(f"Failed to fetch webpage. Status code: {response.status_code}")
            return None
    else:
        print(f"Games on {date.month}/{date.day}/{date.year} loaded locally.")

    result = scrape_tables_from_url(filename)
    games = []
    for df in result:
        games.append(parse_game(df, date))
    return [game for game in games if game]

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

    Parameters:
    season: season (year) to scrape
    gender: "men" or "women"
    refresh_override: if True, will scrape new stats regardless of cache

    Function will write stats .csv files to a directory AND also return tables if stats are scraped.
    
    Returns:
    tables: list of stats dataframes
    """
    if not refresh_override:
        try:
            with open(fr"Stats/{gender.lower()}/cache.txt","r") as f:
                cache = datetime.datetime.fromisoformat(f.read())
                now = datetime.datetime.today()
            if cache.day == now.day and ((cache.hour < 8 and now.hour < 8) or (cache.hour > 8 and now.hour > 8)):
                print("Loading stats on file.")
                tables = {}
                for file in [file for file in os.listdir("Stats") if file.endswith(".csv")]:
                    tables[file.removesuffix(".csv")] = pd.read_csv(f"Stats/{file}", index_col=0)
                return tables
        except:
            pass
    print("Scraping new stats from web.")
    pages = ["school-stats","opponent-stats","advanced-school-stats","advanced-opponent-stats","ratings"]
    tables = {}
    for page in pages:
        url = f"https://www.sports-reference.com/cbb/seasons/{gender.lower()}/{season}-{page}.html"
        for i,table in enumerate(scrape_tables_from_url(url)):
            j = ""
            if i > 0:
                j = f"-{i}"
            tables[f"{page}{j}"] = table
    for key, table in tables.items():
        df: pd.DataFrame = table
        if type(list(df.columns)[0]) is tuple:
            header = [pair[0] for pair in list(df.columns)]
            header2 = [pair[1] for pair in list(df.columns)]
        else:
            header = list(df.columns)
            header2 = list(df.loc[0])
            df = df.drop(df.index[0])
        for i, item in enumerate(header):
            if item.startswith("Unnamed"):
                header[i] = header2[i]
            elif item.startswith("Overall"):
                header[i] = header2[i].replace("%","_Pct").replace("-","_")
            elif item.startswith("SRS"):
                header[i] = header2[i]
            elif item.startswith("Adjusted"):
                header[i] = f"Adj_{header2[i]}"
            elif item.startswith("Conf"):
                header[i] = f"{header2[i]}_Conf"
            elif item.startswith("Home"):
                header[i] = f"{header2[i]}_Home"
            elif item.startswith("Away"):
                header[i] = f"{header2[i]}_Away"
            elif item.startswith("Points"):
                header[i] = f"Pts_{header2[i].strip('.')}"
            elif item.startswith("Totals"):
                header[i] = header2[i].replace("%","_Pct")
            elif item.startswith("Opponent"):
                header[i] = f'Opp_{header2[i].replace("%","_Pct").replace("/","per")}'
            elif item.startswith("School Advanced"):
                header[i] = f'Opp_{header2[i].replace("%","_Pct").replace("/","per")}'
            else:
                header[i] = f"{header[i]}_{header2[i]}"
        df.columns = [str(h) for h in header]
        df = df[~((df['Rk'] == "Rk") | df['Rk'].isna())]
        df = df.apply(pd.to_numeric, errors='ignore')
        try:
            df = df.drop(columns = "nan")
        except:
            pass
        df = df.drop(columns = [col for col in list(df.columns) if "Unnamed" in col])
        df = df.reset_index(drop = True)
        tables[key] = df
        df.to_csv(fr"Stats/{gender.lower()}/{key}.csv")
    with open(fr"Stats/{gender.lower()}/cache.txt","w") as f:
        f.write(str(datetime.datetime.now().isoformat()))
    return tables

def generate_date_range(start_date: datetime.datetime, end_date: datetime.datetime):
    date_list: list[datetime.datetime] = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += datetime.timedelta(days=1)
    return date_list

def fetch_games(start_date: datetime.datetime = datetime.datetime(year=2023, month=11, day=6), end_date: datetime.datetime = datetime.datetime(year=2024, month=3, day=10), sleep: int = 5, refresh: bool = True):
    date_range = generate_date_range(start_date, end_date)
    games: list[Game] = []
    for date in date_range:
        games += fetch_games_on_date(date, refresh)
        time.sleep(sleep)

def fetch_rpi_rankings(year: int = 2024, gender: str = "men"):
    url = "https://www.warrennolan.com/basketball/2021/rpi-live"

def fetch_net_rankings(year: int = 2024, gender: str = "men"):
    pass