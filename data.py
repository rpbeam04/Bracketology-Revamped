import pandas as pd
from classes import *
import fetch
from pprint import *

def populate_team_stats(year: int, gender: str):
    tables = list(fetch.fetch_team_stats(year, gender).values())
    table: pd.DataFrame
    for table in tables:
        for _,row in table.iterrows():
            team = Team.search_team(row["School"], gender, year)
            for item in list(row.keys()):
                if item not in ["School","Rk"]:
                    setattr(team, item, row[item])

def populate_team_metrics(year: int, gender: str):
    tables = []
    tables.append(fetch.fetch_net_rankings(year, gender)[0])
    tables.append(fetch.fetch_rpi_rankings(year, gender))
    table: pd.DataFrame
    for table in tables:
        for _,row in table.iterrows():
            team = Team.search_team(row["Team"], gender, year)
            cols = list(row.keys())
            item: str
            for item in cols:
                if item == "Team" or item.endswith(".1") or item.startswith("Unnamed"):
                    continue
                elif item == "Net_Rank":
                    setattr(team, "NET", row[item])
                elif item in ["NC_SOS","Q1","Q2","Q3","Q4","SOS"] and "RPI" in cols:
                    try:
                        val = row[item].replace(" ","")
                    except:
                        val = row[item]
                    setattr(team, f"{item}_RPI", val)
                elif item in ["SOS","Q1","Q2","Q3","Q4","NC_SOS"] and "NET" in cols:
                    try:
                        val = row[item].replace(" ","")
                    except:
                        val = row[item]
                    setattr(team, f"{item}_NET", val)
                else:
                    setattr(team, item, row[item])

def populate_conference_metrics(year: int, gender: str):
    table = fetch.fetch_net_rankings(year, gender)[1]
    for _,row in table.iterrows():
        conf = Conference.search_conference(row["Conference"], gender, year)
        cols = list(row.keys())
        item: str
        for item in cols:
            if item == "Conference":
                continue
            elif item == "Conference_Leader":
                setattr(conf, item, row[item])
            else:
                try:
                    val = row[item].replace(" ","")
                except:
                    val = row[item]
                setattr(conf, item, val)

def populate_tournament_data(year: int, gender: str):
    data = fetch.fetch_tourney_seed_data(year, gender)
    for _, row in data.iterrows():
        team = Team.search_team(row["School"], gender, year)
        for item in list(data.columns):
            if item not in ["School", "Conference"]:
                setattr(team, item, row[item])

def team_training_data():
    pass