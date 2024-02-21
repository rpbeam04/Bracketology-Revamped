from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
from pprint import pprint
from classes import Team
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
import os

def create_model(estimators: int = 175, refresh = False):
    if not refresh and os.path.exists("Model/extra_trees_model.pkl"):
        with open('Model/extra_trees_model.pkl', 'rb') as f:
            model = pickle.load(f)
            return model
    
    Team.create_teams_from_json()

    # Sample data (replace this with your own data)
    data = pd.read_csv("Model/full-training.csv").drop(columns=["Name"])
    X = data.drop(columns=['Seed']).to_numpy()
    y = data["Seed"].to_numpy()

    extra_trees = ExtraTreesRegressor(n_estimators=estimators, random_state=10)

    # Train the model
    extra_trees.fit(X, y)

    with open('Model/extra_trees_model.pkl', 'wb') as f:
        pickle.dump(extra_trees, f)

    return extra_trees
    
def evaluate_model(extra_trees: ExtraTreesRegressor):
    # Predict on the test set
    data = pd.read_csv("Model/2024/men/training.csv")
    names = data['Name']
    Xx = data.drop(columns=['Name']).to_numpy()
    pred = []
    y_pred = extra_trees.predict(Xx)
    seeds = []
    for i,name in enumerate(names):
        seeds.append((Team.search_team(name,"men",2024),round(17-16*y_pred[i],4)))
    pred.append(y_pred)

    df = pd.read_csv("Model/matrix.csv").dropna(subset=['0'])
    df = df[['1','3']].reset_index(drop=True)
    df.columns = ['Team','Seed']
    df['Seed'] = (17-pd.to_numeric(df['Seed']))/16
    matrix = []
    for _,row in df.iterrows():
        matrix.append((Team.search_team(row["Team"],"men",2024),round(17-16*row["Seed"],4)))

    team_seeds = []
    for team in matrix:
        for seed in seeds:
            if team[0] == seed[0]:
                team_seeds.append({team[0].Name: [team[1], seed[1]]})

    seed = 0
    j = 0
    s_pred = []
    y = []
    y_pred = []
    flag = True
    team_seeds = sorted(team_seeds, key=lambda x: list(x.values())[0][1])
    for i, team in enumerate(team_seeds):
        if j%4 == 0:
            seed += 1
        if seed == 11 and j%4 == 3 and flag:
            j -= 2
            flag = False
        if seed > 16:
            seed = 16
        j += 1
        team_seeds[i][list(team.keys())[0]].insert(0,seed)
        s_pred.append(seed)
        y.append(team_seeds[i][list(team.keys())[0]][1])
        y_pred.append(team_seeds[i][list(team.keys())[0]][2])

    pprint(team_seeds)
    mse = mean_squared_error(y, y_pred)
    print(f"Mean Squared Error:", round(mse,3))
    mse2 = mean_squared_error(y, s_pred)
    print(f"Mean SeedSq Error:", round(mse2,3))
