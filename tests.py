from classes import Team, Game, Conference
import fetch
from datetime import datetime as dt
import pandas as pd
import numpy as np
import random
from pprint import *
from IPython.display import display
import os

genders = ["men", "women"]

Team.create_teams_from_json()
Conference.create_conferences_from_json()
for gender in genders:
    fetch.fetch_rpi_rankings(gender=gender)
    fetch.fetch_rpi_rankings(gender=gender)

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