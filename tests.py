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

Team.clean_duplicates()
#pprint(Team.team_list[0].__dict__)

games = fetch.fetch_games(sleep=1, refresh=False)
#games = fetch.fetch_games_on_date(dt(2024,2,4), refresh=False)

print(len(Game.game_list))
#pprint(Game.game_list[0].__dict__)

team: Team
for team in Team.team_list:
    if len(team.Games) < 1 or len(team.Games) > 30:
        print(team.Name, team.Gender, len(team.Games))