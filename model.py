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
layers = [(15,100,20,100,50)]
models = {}
for pair in layers:
    mlp_regressor = MLPRegressor(hidden_layer_sizes=pair, activation='relu', solver='adam', max_iter=1000, random_state=42)
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
        seeds.append((Team.search_team(name,"men",2024),round(y_pred[i],4)))
    pred.append(y_pred)

df = pd.read_csv("Model/matrix.csv").dropna(subset=['0'])
df = df[['1','3']].reset_index(drop=True)
df.columns = ['Team','Seed']
df['Seed'] = (17-pd.to_numeric(df['Seed']))/16
matrix = []
for _,row in df.iterrows():
    matrix.append((Team.search_team(row["Team"],"men",2024),row["Seed"]))
y = []
y_pred = []
for team in matrix:
    y.append(team[1])
    for seed in seeds:
        if team[0] == seed[0]:
            y_pred.append(seed[1])

mse = mean_squared_error(y, y_pred)
print(f"Mean Squared Error {key}:", mse)
