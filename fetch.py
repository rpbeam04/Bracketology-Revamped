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
        if gender.lower() == "nit":
            gender = "men"
    except:
        gender = "women"
        print("Error (game): No gender, default to women's.")
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
            with open(fr"Stats/{season}/{gender.lower()}/cache.txt","r") as f:
                cache = datetime.datetime.fromisoformat(f.read())
                now = datetime.datetime.today()
            if True:
            #if cache.day == now.day and ((cache.hour < 8 and now.hour < 8) or (cache.hour > 8 and now.hour > 8)):
                print("Loading stats on file.")
                tables = {}
                for file in [file for file in os.listdir(fr"Stats/{season}/{gender.lower()}") if file.endswith(".csv")]:
                    tables[file.removesuffix(".csv")] = pd.read_csv(fr"Stats/{season}/{gender.lower()}/{file}", index_col=0)
                return tables
            elif season < 2024:
                print("Loading stats on file.")
                tables = {}
                for file in [file for file in os.listdir(fr"Stats/{season}/{gender.lower()}") if file.endswith(".csv")]:
                    tables[file.removesuffix(".csv")] = pd.read_csv(fr"Stats/{season}/{gender.lower()}/{file}", index_col=0)
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
                header[i] = header2[i].replace(" ","_")
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
                header[i] = f'{header2[i].replace("%","_Pct").replace("/","per")}'
            else:
                header[i] = f"{header[i]}_{header2[i]}"
        df.columns = [str(h) for h in header]
        df = df[~((df['Rk'] == "Rk") | df['Rk'].isna())]
        df = df.apply(pd.to_numeric, errors='ignore')
        try:
            df = df.drop(columns = "nan")
        except:
            pass
        for i,_ in df.iterrows():
            team = df.loc[i,"School"]
            team: str
            if team.endswith("NCAA"):
                df.at[i,"School"] = team.removesuffix("NCAA")[0:-1]
            if team == "FDU":
                df.at[i,"School"] = "Fairleigh Dickinson"
            try:
                if df.loc[i,"Conf"].startswith("MAC"):
                    df.at[i,"Conf"] = "MAC"
            except:
                pass
        df = df[(df['W'] != 0) | (df['L'] != 0)]
        df = df.drop(columns = [col for col in list(df.columns) if "Unnamed" in col])
        df = df.reset_index(drop = True)
        tables[key] = df
        file_path = fr"Stats/{season}/{gender.lower()}"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        df.to_csv(fr"{file_path}/{key}.csv", index=False)
    with open(fr"{file_path}/cache.txt","w") as f:
        f.write(str(datetime.datetime.now().isoformat()))
    return tables

def generate_date_range(start_date: datetime.datetime, end_date: datetime.datetime):
    date_list: list[datetime.datetime] = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += datetime.timedelta(days=1)
    return date_list

def fetch_games(start_date: datetime.datetime = datetime.datetime(year=2023, month=11, day=6), end_date: datetime.datetime = datetime.datetime(year=2024, month=3, day=10), sleep: int = 0, refresh: bool = True):
    date_range = generate_date_range(start_date, end_date)
    games: list[Game] = []
    for date in date_range:
        games += fetch_games_on_date(date, refresh)
        time.sleep(sleep)

def fetch_rpi_rankings(year: int = 2024, gender: str = "men", refresh_override: bool = False):
    if not refresh_override:
        try:
            rpi_ranks = pd.read_csv(fr"Metrics/{year}/{gender.lower()}/RPI.csv")
            print("RPI found locally.")
            return rpi_ranks
        except:
            pass
    gender_flag = ""
    if gender == "women":
        gender_flag = "w"
    url = fr"https://www.warrennolan.com/basketball{gender_flag}/{year}/rpi-live"
    if year < 2021:
        url = url.replace("rpi-live","nitty-live")
    rpi_ranks = scrape_tables_from_url(url)[-1]
    try:
        rpi_ranks = rpi_ranks.drop(columns= ["RPI Delta"])
    except:
        pass
    rpi_ranks = rpi_ranks.dropna(axis=1, how='all')
    rpi_ranks = rpi_ranks[rpi_ranks["Record"] != "0 - 0"]
    rpi_ranks = rpi_ranks[rpi_ranks["Record"] != "0-0"]
    rpi_ranks = rpi_ranks[rpi_ranks["Team"] != "Team"]
    rpi_ranks = rpi_ranks[~rpi_ranks["Team"].str.startswith("freestar.config")]
    rpi_ranks['Team'] = rpi_ranks['Team'].apply(lambda x: x.split('  ')[0].strip())
    rpi_ranks['Team'] = rpi_ranks['Team'].apply(lambda x: Team.search_team(x, gender, year).Name)
    rpi_ranks.columns = [str(h.replace(" ","_")) for h in list(rpi_ranks.columns)]
    rpi_ranks = rpi_ranks.apply(pd.to_numeric, errors='ignore')
    rpi_ranks = rpi_ranks.reset_index(drop=True)
    file_path = fr"Metrics/{year}/{gender}"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    rpi_ranks.to_csv(fr"{file_path}/RPI.csv", index=False)
    return rpi_ranks

def fetch_net_rankings(year: int = 2024, gender: str = "men", refresh_override: bool = False):
    if not refresh_override:
        try:
            net_ranks = pd.read_csv(fr"Metrics/{year}/{gender.lower()}/NET.csv")
            net_conf = pd.read_csv(fr"Metrics/{year}/{gender.lower()}/NET-conf.csv")
            print("NET found locally.")
            return net_ranks, net_conf
        except:
            pass
    if year < 2019:
        print("Warning: NET rankings began in the 2018-19 season, year 2019.")
        return None
    if year < 2021 and gender == "women":
        print("Warning: Women's NET rankings began in the 2020-21 season, year 2021.")
        return None
    gender_flag = ""
    if gender.lower() == "women":
        gender_flag = "w"
    url = fr"https://www.warrennolan.com/basketball{gender_flag}/{year}/net"
    if year < 2021:
        url += "-nitty"
    net_ranks = scrape_tables_from_url(url)[-1]
    try:
        net_ranks = net_ranks.drop(columns= ["NET Delta"])
    except:
        pass
    net_ranks = net_ranks.dropna(axis=1, how='all')
    net_ranks = net_ranks[net_ranks["Record"] != "0 - 0"]
    net_ranks = net_ranks[net_ranks["Record"] != "0-0"]
    if year < 2021:
        net_ranks = net_ranks[net_ranks["Team"] != "Team"]
        net_ranks['Team'] = net_ranks['Team'].apply(lambda x: x.split('  ')[0].strip())
    net_ranks['Team'] = net_ranks['Team'].apply(lambda x: Team.search_team(x, gender, year).Name)
    net_ranks.columns = [str(h.replace(" ","_")) for h in list(net_ranks.columns)]
    net_ranks = net_ranks.apply(pd.to_numeric, errors='ignore')
    file_path = fr"Metrics/{year}/{gender.lower()}"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    net_ranks.to_csv(fr"{file_path}/NET.csv", index=False)
    # Conference NET
    url = fr"https://www.warrennolan.com/basketball{gender_flag}/{year}/net-conference"
    if year < 2021:
        url = url.replace("net-conference","conferencenet")
    net_conf = scrape_tables_from_url(url)[-1]
    net_conf = net_conf.dropna(axis=1, how='all')
    net_conf.columns = [str(h.replace(" ","_").removesuffix(".1")) for h in list(net_conf.columns)]
    net_conf = net_conf.apply(pd.to_numeric, errors='ignore')
    net_conf.to_csv(fr"{file_path}/NET-conf.csv", index=False)
    return net_ranks, net_conf