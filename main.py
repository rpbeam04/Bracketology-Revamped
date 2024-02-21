### MAIN SCRIPT TO RUN BEAM BRACKETS BRACKETOLOGY
# Local Imports
import fetch
from classes import Team, Conference, Player, Game
import data
import model
# Module Imports
from datetime import datetime as dt
import pandas as pd

# Select season, gender(s)
season: int = 2024
genders: list[str] = ["men","women"]

# Define what already exists in .csv or .json format (True if exists and up to date)
source_full: bool = False
stats: bool = True
teams: bool = False
conferences: bool = False # teams and conferences must agree
games: bool = True
metrics: bool = True
seeds: bool = True
training: bool = True
predictive_model: bool = True
# Specify below dates where games data is missing
start_games = dt(year = 2023, month = 11, day = 6)
end_games = dt(year = 2024, month = 3, day = 11)

# Create classes and fetch new data if neccesary
if source_full:
    data.full_object_sourcing()
if not stats:
    for gender in genders:
        fetch.fetch_team_stats(season, gender, True)
if not teams:
    Team.clear_teams()
    for gender in genders:
        Team.create_teams_from_stats(gender, season)
    Team.clean_duplicates()
    Team.write_teams_to_json()
elif teams:
    Team.create_teams_from_json()
if not conferences:
    for gender in genders:
        Conference.create_conferences_from_stats(gender, season)
    Conference.write_conferences_to_json()
elif conferences:
    Conference.create_conferences_from_json()
if not games:
    Game.create_games_from_json()
    fetch.fetch_games(start_games, end_games)
    Game.write_games_to_json()
elif games:
    Game.create_games_from_json()
if not metrics:
    for gender in genders:
        fetch.fetch_net_rankings(season, gender, True)
        fetch.fetch_rpi_rankings(season, gender, True)

# Loading the neccesary data to the classes
for gender in genders:
    data.populate_team_stats(season, gender)
    data.populate_team_metrics(season, gender)
    data.populate_conference_metrics(season, gender)
    if season < 2024:
        data.populate_tournament_data(season, gender)

# Preparing, loading, and creating the model
predictor = model.create_model(refresh = (not predictive_model))
model.evaluate_model(predictor)

dfs = []
for gender in genders:
    dfs.append(data.team_training_data(season, gender, True, (not training)))
for i,df in enumerate(dfs):
    df: pd.DataFrame
    names = df["Name"]
    X = df.drop(columns=['Name']).to_numpy()
    y = predictor.predict(X)
    y = 17 - y*16
    results = pd.concat([names,pd.DataFrame(y)], axis=1)
    results.columns = ["Team","Seed"]
    results["Seed"] = results["Seed"].apply(lambda x: round(x,2))
    results = results.sort_values(by="Seed")
    results = results.reset_index(drop=True)
    results.to_csv(fr"Bracket/Seeds/{genders[i]}-pred.csv")