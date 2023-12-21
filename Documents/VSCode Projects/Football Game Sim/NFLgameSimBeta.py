import random
import numpy as np
import pandas as pd
import math
import scipy
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
from pprint import *

class Team:
    def __init__(self,name):
        self.Name = name
        self.Run_Rate = 0.5 # calculated by rush plays/(rush plays + pass plays)
        self.Yds_per_Carry = 4.5
        self.Yds_per_Completion = 10.5
        self.Completion_Pct = 0.6
        self.Players = []
        self.Coaches = []
    def __str__(self):
        return self.Name
    def return_starter(self, pos):
        return np.random.choice([player for player in self.Players if player.Pos == pos])

class Player:
    def __init__(self,name,position,team):
        self.Name = name
        self.Pos = position # QB, RB, WR, TE, OL, DL, LB, CB, SS, PK, PP for now
        self.Team = team
        if self not in team.Players:
            team.Players.append(self)
    def __str__(self):
        return f"{self.Name} ({self.Pos})"

class Coach:
    def __init__(self,name,job,team):
        self.Name = name
        self.Job = job # Either HC, OC, or DC for now
        self.Team = team
        self.Aggression = 0.5
        if self not in team.Coaches:
            team.Coaches.append(self)
    def __str__(self):
        return self.Name

teams = [Team("Legends"),Team("All Stars")]

Player("Tom Brady","QB",teams[0])
Player("Reggie Bush","RB",teams[0])
Player("Adrian Peterson","RB",teams[0])
Player("Wes Welker","WR",teams[0])
Player("Randy Moss","WR",teams[0])
Player("Antonio Brown","WR",teams[0])
Player("Rob Gronkowski","TE",teams[0])
Player("Joe Thomas","OL",teams[0])
Player("Reggie White","DL",teams[0])
Player("Luke Kuechly","LB",teams[0])
Player("Darelle Revis","CB",teams[0])
Player("Charles Woodson","CB",teams[0])
Player("Ed Reed","SS",teams[0])
Player("Adam Vinetari","PK",teams[0])
Player("Pat McAfee","PP",teams[0])
Coach("Vince Lombardi","HC",teams[0])
Coach("Don Shula","OC",teams[0])
Coach("Mike Ditka","DC",teams[0])

Player("Patrick Mahomes","QB",teams[1])
Player("Christian McCaffery","RB",teams[1])
Player("Derrick Henry","RB",teams[1])
Player("Tyreek Hill","WR",teams[1])
Player("Jamarr Chase","WR",teams[1])
Player("Keenan Allen","WR",teams[1])
Player("Sam Laporta","TE",teams[1])
Player("Tristian Wirfs","OL",teams[1])
Player("Aaron Donald","DL",teams[1])
Player("Devin White","LB",teams[1])
Player("Trevon Diggs","CB",teams[1])
Player("Patrick Surtain II","CB",teams[1])
Player("Harrison Smith","SS",teams[1])
Player("Tyler Bass","PK",teams[1])
Player("Johnny Hecker","PP",teams[1])
Coach("Dan Campbell","HC",teams[1])
Coach("Mike McDaniel","OC",teams[1])
Coach("Mike Tomlin","DC",teams[1])

teams[1].Players

def generate_play(offense: Team, defense: Team, down: int = 1, to_go: int = 10, dist: int = 75, quarter: int = 1, time: float = 0.0, margin: int = 0):
    """
    generate_play(offense: Team, defense: Team, down: int = 1, to_go: int = 10, dist: int = 75, time: float = 0.0, margin: int = 0):
    
    offense: class Team, the team on offense
    defense: class Team, the team on defense
    down: int, the down
    to_go: int, yards to get a first down
    dist: int, yards to score a touchdown
    quarter: int, quarter of the game
    time: float, game time in the quarter between 0 and 15 minutes, counting up
    margin: int, the current scoring margin between teams, positive means offense is winning
    
    Returns:
    result: int, yards gained or lost on the play
    desc: str, description of the play
    stats: list, player stats from play
    
    This function generates a play between the two teams according to the given parameters, and returns the result and stats.
    """
    # Conditions for non-standard plays (special teams, end of half, etc)
    if down == 4 and not go_for_it():
        result, desc = special_teams()
        return result, desc
    
    # Run Pass Modifiers
    run_rate = offense.Run_Rate
        
    # Standard play simulation logic (0 is run, 1 is pass)
    play_type = 0 if random.random() < run_rate else 1
    
    # Yardage and Stats calculations
    # Evenutally, defense will play a role in these
    cmp_pct = offense.CompletionPct
    ypcmp = offense.YdsCompletion
    ypc = offense.YdsCarry
    
    stats = []
    if play_type:
        complete = 1 if random.random() < cmp_pct else 0
        if complete:
            result = np.random.poisson(ypcmp, 1)[0]
            desc = f"{offense.return_starter("QB").Name} pass complete to {offense.return_starter("WR")} for {result} yards."
            return result, desc
        else:
            desc = f"{offense.return_starter("QB").Name} pass incomplete."
            return 0, desc
    else:
        result = np.random.poisson(ypc, 1)[0]
        desc = f"{offense.return_starter("RB").Name} rush for {result} yards."
        return result, desc

def go_for_it(quarter, to_go, dist, time, margin, aggression):
    if quarter == 4 and margin < 0:
        if to_go < 5 and dist < 50:
            return True
    if quarter == 4 and time > 10 and margin < 0 and margin >= 8:
        return True
    return False
    
def special_teams():
    return 0, "Special teams go brrr."

lower_bound = -10
upper_bound = 100

mu = 10.5
std_lower = 5  # Standard deviation for losses
std_upper = 20  # Standard deviation for gains

a = (lower_bound - mu) / std_lower
b = (upper_bound - mu) / std_upper
truncated_normal = truncnorm(a, b, loc=mu, scale=std_lower + std_upper)

samples = truncated_normal.rvs(100000)
# plt.hist(samples, bins=30, density=True, alpha=0.7, color='b')

# plt.xlabel('Yardage Gained on Pass')
# plt.ylabel('Probability Density')
# plt.title('Truncated Normal Distribution with Different Standard Deviations')

# plt.show()

# df = pd.read_csv('https://raw.githubusercontent.com/ArrowheadAnalytics/next-gen-scrapy-2.0/master/pass_and_game_data.csv', low_memory=False)
# #There's an additional index row we don't need, so I am getting rid of it here
# df = df.iloc[0:,1:]

# fig = plt.hist(df.y, bins = round(max(list(df.y))-min(list(df.y))), density = True)
# plt.show()

def convert_float_time(time):
    minute = 15 - math.ceil(time)
    second = round((math.ceil(time) - time)*60)
    return minute, second

def display_clock_time(minute, second):
    if second < 10:
        second = f"0{str(second)}"
    return f"{minute}:{second}"

# GAME LOOP
for time in np.arange(0,15.0001,1/24):
    quarter = math.floor(time/15) + 1
    minute, second = convert_float_time(time)
    print(f"{round(time,2)}: {quarter}Q, {display_clock_time(minute, second)}")