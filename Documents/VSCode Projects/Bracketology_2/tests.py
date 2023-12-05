import pandas as pd
from classes import *
import datetime
import re

with open("test_df.csv", 'r', encoding='utf-8') as f:
    df = pd.read_csv(f)

def extract_name_rank(text: str):
    pattern = re.compile(r'([^()]+)(?: \((\d+)\))?')
    match = pattern.findall(text)
    name = match[0][0].rstrip()
    try:
        ranking = match[1][0]
    except:
        ranking = None
    return name, ranking

def parse_game(df: pd.DataFrame, date: datetime):
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
    month = date.month
    day = date.day
    year = date.year

Team("UNC","Women")
Team("South Carolina","Women")
date = datetime.date(2023,12,3)
print(parse_game(df, date))
