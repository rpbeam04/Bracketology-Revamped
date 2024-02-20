from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
from pprint import pprint
from classes import Team

Team.create_teams_from_json()

# Sample data (replace this with your own data)
data = pd.read_csv("Model/full-training.csv").drop(columns=["Name"])
X = data.drop(columns=['Seed']).to_numpy()
y = data["Seed"].to_numpy()

# Initialize the MLPRegressor
layers = [(950,950)]
models = {}
for pair in layers:
    mlp_regressor = MLPRegressor(hidden_layer_sizes=pair, activation='relu', solver='adam', max_iter=5000, random_state=10)
    mlp_regressor.fit(X, y)
    models[str(pair)] = mlp_regressor

# Predict on the test set
data = pd.read_csv("Model/2024/men/training.csv")
names = data['Name']
Xx = data.drop(columns=['Name']).to_numpy()
pred = []
for key, mlp_regressor in models.items():
    y_pred = mlp_regressor.predict(Xx)
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
print(f"Mean Squared Error {key}:", round(mse,3))
mse2 = mean_squared_error(y, s_pred)
print(f"Mean SeedSq Error {key}:", round(mse2,3))
