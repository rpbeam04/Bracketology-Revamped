### MAIN SCRIPT TO RUN BEAM BRACKETS BRACKETOLOGY
# Local Imports
import fetch
from classes import Team, Conference, Player, Game
import data
import model
from datetime import datetime as dt

# Select season, gender(s)
season: int = 2024
genders: list[str] = ["men","women"]

# 1. Data Sourcing
# Define what already exists in .csv or .json format
stats: bool = False
teams: bool = True
conferences: bool = True
games: bool = True
metrics: bool = False
seeds: bool = True
# Specify below dates where games data is missing
start_games = dt(year = 2023, month = 11, day = 6)
end_games = dt(year = 2024, month = 3, day = 11)

# Create classes and fetch new data if neccesary
if not stats:
    for gender in genders:
        fetch.fetch_team_stats(season, gender, True)
if not teams:
    Team.clear_teams()
    for gender in genders:
        Team.create_teams_from_stats(gender, season)
    Team.clean_duplicates()
    Team.write_teams_to_json()
if not conferences:
    for gender in genders:
        Conference.create_conferences_from_stats(gender, season)
    Conference.write_conferences_to_json()
if not games:
    Game.create_games_from_json()
    fetch.fetch_games(start_games, end_games)
    Game.write_games_to_json()
if not metrics:
    fetch.fetch_net_rankings(season, gender, True)
    fetch.fetch_rpi_rankings(season, gend)