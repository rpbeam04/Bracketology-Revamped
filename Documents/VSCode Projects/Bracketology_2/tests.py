import fetch
import datetime
import pandas as pd
import numpy as np
from pprint import *
from IPython.display import display
import os

x = fetch.fetch_team_stats()
for k,v in x.items():
    print(k,v)
