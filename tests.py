from classes import Team, Game
import fetch
from datetime import datetime as dt
import pandas as pd
import numpy as np
import random
from pprint import *
from IPython.display import display
import os

# tests = ["Miami (FL) (9)", "Miami (FL)","Miami (16)", "Miami"]
# for text in tests:
#     (name, rank) = fetch.extract_name_rank(text)
#     print(text, name, rank, len(name))

Team.create_teams_from_stats(gender = "men")
Team.create_teams_from_stats(gender = "women", write_to_json=True)

print(len(Team.team_list))
Team.clean_duplicates()

#games = fetch.fetch_games(start_date=dt(2023,12,1),end_date=dt(2024,1,10),sleep=10)
games = fetch.fetch_games_on_date(dt(2024,2,1))
Game.write_games_to_json()

print(len(Game.game_list))

team: Team
for team in Team.team_list:
    # if len(team.Games) < 1 or len(team.Games) > 30:
    #     print(team.Name, team.Gender, len(team.Games))
    pass