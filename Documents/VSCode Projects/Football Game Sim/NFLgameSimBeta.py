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

def score_check(result, dist):
    if result > dist:
        return dist, True
    return result, False

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
    result: int, yards gained or lost on the play, or play result code (> 100)
        result codes:
        101: PAT successful
        110: PAT unsuccessful
        300: made field goal
    desc: str, description of the play
    play_time: float, time taken by the play
    run_clock: bool, whether the clock keeps running after the play
    
    This function generates a play between the two teams according to the given parameters, and returns the result and stats.
    """
    # Conditions for non-standard plays (special teams, end of half, etc)
    if down == 4 and not go_for_it():
        result, desc, play_time = special_teams(quarter, time, dist, margin)
        return result, desc, play_time, False
    
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
            desc = f"{offense.return_starter("QB").Name} pass complete to {offense.return_starter("WR")} for {score_check(result, dist)[0]} yards."
            return result, desc, 0.1, True
        else:
            desc = f"{offense.return_starter("QB").Name} pass incomplete."
            return 0, desc, 0.1, False
    else:
        result = np.random.poisson(ypc, 1)[0]
        desc = f"{offense.return_starter("RB").Name} rush for {score_check(result, dist)[0]} yards."
        return result, desc, 0.1, True

def go_for_it(quarter, to_go, dist, time, margin, aggression):
    if quarter == 4 and margin < 0:
        if to_go < 5 and dist < 50:
            return True
    if quarter == 4 and time > 10 and margin < 0 and margin >= 8:
        return True
    return False
    
def special_teams(quarter, time, dist, margin):
    if dist < 40:
        a = -4.4947 * 10**(-126)
        b = 1.736 * 10**9
        c = 0.993889
        d = 89.081
        outcome = success(a*math.log(b*(dist+17))**d + c + 0.01)
        if outcome:
            return 300, f"{"kicker"} {dist+17} yard field goal is good."
        else:
            return 0, f"{"kicker"} {dist+17} yard field goal is no good."
    else:
        punt = rand_norm_int(45,10)
        if punt < 25:
            punt = rand_norm_int(35,5)
        while punt < 0:
            punt = rand_norm_int(45,10)



def yard_line(distance):
    """
    Convert distance from end zone to yard line.
    """
    if distance > 50:
        return 100 - distance
    return distance


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

def success(pct):
    """
    Given pct [0,1], returns random trial result where pct is chance of success.
    """
    outcome = random.random()
    if outcome <= success:
        return True
    return False

def convert_float_time(time):
    minute = 15 - math.ceil(time)
    second = round((math.ceil(time) - time)*60)
    return minute, second

def display_clock_time(minute, second):
    if second < 10:
        second = f"0{str(second)}"
    return f"{minute}:{second}"

def rand_norm_int(mean, std_dev):
    random_float = np.random.normal(mean, std_dev)
    return round(random_float)

def kickoff(kicking: Team, receiving: Team, onside: bool = False):
    """
    Returns:
    result: int, returm yardage from end zone
    desc: str, play description
    play_time: float, play time
    run_clock: False
    onside_recovery: bool, if kicking team recovers onside kick
    """
    if not onside:
        touchback = success(0.78)
        if touchback:
            return 25, f"{kicking.Name} for a touchback.", 0, False, False
        else:
            yards = rand_norm_int(22,8)
            if yards <= 10:
                yards = rand_norm_int(18,5)
            while yards <= 0:
                yards = rand_norm_int(18,5)
            return yards, f"{kicking.Name} kickoff, returned for {yards} yards by {receiving.return_starter("WR")}.", 0.1, False, False
    else:
        yards = rand_norm_int(54,2)
        outcome = success(0.02)
        if outcome:
            if yards < 50:
                desc = f"{kicking.Name} recover onside kick at opponent {yards} yard line."
            elif yards == 50:
                desc = f"{kicking.Name} recover onside kick at 50 yard line."
            else:
                desc = f"{kicking.Name} recover onside kick at own {yard_line(yards)} yard line."
            return yards, desc, 0.1, False, True
        else:
            if yards < 50:
                desc = f"{receiving.Name} recover onside kick at own {yards} yard line."
            elif yards == 50:
                desc = f"{receiving.Name} recover onside kick at 50 yard line."
            else:
                desc = f"{receiving.Name} recover onside kick at opponent {yard_line(yards)} yard line."
            return yards, desc, 0.1, False, False

def go_for_two(quarter, time, margin):
    margins = [10,5,2]
    if quarter == 4:
        if margin in margins:
            return True
        elif margin == 8:
            return success(0.5)
    return False

def point_after_touchdown(offense: Team, defense: Team, two_pt_conv: bool = False):
    if not two_pt_conv:
        outcome = success(0.95)
        if outcome:
            return 101, desc, 0, False
    else:
        result, desc, play_time, run_clock = generate_play(offense, defense, 1, 2, 2, 1, 5, 0)
        return result, f"{desc}", play_time, run_clock

# GAME LOOP
game = True
quarter = 1
time = 0.0
home = teams[0]
away = teams[1]
home_score = 0
away_score = 0
teams_receive = [home, away]
random.shuffle(teams_receive)
pat = False
while game:
    special = False
    if quarter % 2 == 1 and time == 0:
        special = True
        if quarter == 1:
            result, desc, play_time, run_clock, onside_recovery = kickoff(teams_receive[0],teams_receive[1],False)
            offense = teams_receive[1]
            defense = teams_receive[0]
        elif quarter == 3:
            result, desc, play_time, run_clock, onside_recovery = kickoff(teams_receive[1],teams_receive[0],False)
            offense = teams_receive[0]
            defense = teams_receive[1]
    elif kick_after_pat:
        special = True
        kick_after_pat = False
        result, desc, play_time, run_clock, onside_recovery = kickoff(offense, defense, False)
    elif pat:
        special = True
        kick_after_pat = True
        pat = False
        result, desc, play_time, run_clock = point_after_touchdown(offense, defense, go_for_two(quarter, time, margin))
    if not special:
        result, desc, run_clock = generate_play(offense, defense, down, to_go, dist, quarter, time, margin)