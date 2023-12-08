import fetch
import datetime
import pandas as pd
from pprint import *
from IPython.display import display

with open("Stats/school-stats.csv") as f:
    df = pd.read_csv(f)

df.columns = [1]*len(df.columns)
print(df.columns)