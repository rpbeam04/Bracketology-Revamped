from classes import Team, Game, Conference
import fetch
from datetime import datetime as dt
import pandas as pd
import numpy as np
import random
from pprint import *
from IPython.display import display
import os
import time

Team.clear_teams()
genders = ["women","men"]
years = [2021,2022,2023,2024]
for gender in genders:
    if gender == "men":
        years.insert(0,2019)
    for year in years:
        fetch.fetch_team_stats(year, gender)
        Team.create_teams_from_stats(gender, year)
        Conference.create_conferences_from_stats(gender, year)
        fetch.fetch_net_rankings(year, gender)
        time.sleep(2)
        fetch.fetch_rpi_rankings(year, gender)
Team.clean_duplicates()
Team.write_teams_to_json()
Conference.write_conferences_to_json()

# df = pd.read_csv("test2021.csv")
# df2 = pd.read_csv("Stats/2021/men/school-stats.csv")

# wrn = []
# for item in list(df["Team"]):
#     if item not in list(df2["School"]):
#         wrn.append(item)

# sr = []
# for item in list(df2["School"]):
#     if item not in list(df["Team"]):
#         sr.append(item)

# wrn.sort()
# sr.sort()
# f = open("team-bug.txt","w")
# for i, item in enumerate(wrn):
#     f.write(f"\t\"{item}\": _,\n")
#     try:
#         print(f"{item}\t {sr[i]}")
#     except:
#         print(item)
# f.close()

# tests = ["Miami (FL) (9)", "Miami (FL)","Miami (16)", "Miami"]
# for text in tests:
#     (name, rank) = fetch.extract_name_rank(text)
#     print(text, name, rank, len(name))

# Team.clean_duplicates()
# #pprint(Team.team_list[0].__dict__)

# games = fetch.fetch_games(refresh=False)
# #games = fetch.fetch_games_on_date(dt(2023,11,22), refresh=False)
# Game.write_games_to_json()

# print(len(Game.game_list))
# #pprint(Game.game_list[0].__dict__)

# team: Team
# for team in Team.team_list:
#     if len(team.Games) < 1:
#         print(team.Name, team.Gender, len(team.Games))