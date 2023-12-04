import pandas as pd

with open("test_df.csv", 'r', encoding='utf-8') as f:
    df = pd.read_csv(f)

print(df.iloc[0,1)