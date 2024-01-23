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

Team.create_teams_from_json()

print(len(Team.team_list))
Team.clean_duplicates()
#pprint(Team.team_list[0].__dict__)

#games = fetch.fetch_games(start_date=dt(2023,12,1),end_date=dt(2024,1,10),sleep=10)
games = fetch.fetch_games_on_date(dt(2024,2,3))

print(len(Game.game_list))
#pprint(Game.game_list[0].__dict__)

team: Team
for team in Team.team_list:
    # if len(team.Games) < 1 or len(team.Games) > 30:
    #     print(team.Name, team.Gender, len(team.Games))
    if len(team.Games) > 0:
        pprint(team.__dict__)
        break