from classes import Team, Game, Conference, Player
import fetch
import data
import pandas as pd
import matplotlib.pyplot as plt

# Metrics vs. Seed
df = pd.read_csv("Model/full-training.csv").drop(columns=['Name'])
df = df.groupby('Seed').mean()
plt.figure(figsize=(11,8))
for col in df.columns:
    if col != 'Name':
        plt.plot(df[col])
plt.legend(list(df.columns), loc='lower left')
plt.title("Impact of Metrics on Men's and Women's Tournament Seed (2021-2023)")
plt.xlabel("Seed")
plt.ylabel("Normalized Metric")
plt.xticks(range(1,17))
plt.show()