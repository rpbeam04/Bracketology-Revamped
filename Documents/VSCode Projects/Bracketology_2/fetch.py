import pandas as pd
from classes import *
import datetime
import re
import os

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
    with open("Stats/cache.txt","r") as f:
        cache = datetime.datetime.fromisoformat(f.read())
        now = datetime.datetime.today()
    if cache.day == now.day and ((cache.hour < 8 and now.hour < 8) or (cache.hour > 8 and now.hour > 8)):
        print("Loading stats on file.")
        tables = {}
        for file in [file for file in os.listdir("Stats") if file.endswith(".csv")]:
            tables[file.removesuffix(".csv")] = pd.read_csv(f"Stats/{file}", index_col=0)
        return tables
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
        df = table
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
        df.to_csv(f"Stats/{key}.csv")
    with open("Stats/cache.txt","w") as f:
        f.write(str(datetime.datetime.now().isoformat()))
    return tables
