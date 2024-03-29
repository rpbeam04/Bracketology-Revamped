from classes import Team, Game, Conference
import fetch
from datetime import datetime as dt
import pandas as pd
import numpy as np
import random
from pprint import pprint
from IPython.display import display
import os
import time
import data
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# Team.create_teams_from_json()
Conference.create_conferences_from_json()
for conf in Conference.filtered_conference_list("men",2024):
    print(f'"{conf.Name}": "",')
# for year in [2021,2022,2023]:
#     for gender in ['men','women']:
#         data.team_training_data(year, gender)
# data.create_full_training()

# df = pd.read_csv("Model/2024/men/training.csv").drop(columns=['Name'])
# df2 = pd.read_csv("Model/2023/men/training.csv").drop(columns=['Name'])
# df.describe().to_csv("df1.csv")
# df2.describe().to_csv("df2.csv")

# data.populate_team_stats(2024, "men")
# data.populate_conference_metrics(2024, "men")
# data.populate_team_metrics(2024, "men")
# data.populate_team_metrics(2019, "men")
# ranks = Team.stat_rankings_p6("3PAr", "men", 2024)
# df = pd.DataFrame(ranks).transpose()
# df.columns = ["Rank","3PA Rate"]
# df["Rank"] = df["Rank"].astype(int)
# pd.set_option("display.max_rows",500)
# pprint(df)

# to_diffs = {}
# for team in Team.filtered_team_list("men", 2024, True):
#     to_diffs[team.Name] = -team.per_game("TOV") + team.per_game("Opp_TOV")
# to_diffs = dict(sorted(to_diffs.items(), key = lambda x: x[1], reverse=True))
# for i, ele in enumerate(list(to_diffs.items())):
#     print(i+1,ele[0],round(ele[1],2))

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