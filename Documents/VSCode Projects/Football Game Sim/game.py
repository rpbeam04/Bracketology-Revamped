import random
import numpy as np
import pandas as pd
import math
import scipy
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
from pprint import *
from teams import *
from plays import *

class Game():
    def __init__(self, home: Team, away: Team):
        self.Home = home
        self.Away = away
        self.Quarter = 1
        self.Time = 0.0
        self.Home_Score = 0
        self.Away_Score = 0
    def __str__(self):
        return f"<Game: {self.Away.Name} @ {self.Home.Name}>"
    def coin_toss(self, call: str = "heads", home_preference: str = "receive", away_preference: str = "receive"):
        flip = success(0.5)
        if flip:
            result = "heads"
        else:
            result = "tails"
        if result == call.lower():
            if away_preference.lower() == "receive":
                pass
    def change_offense(self, new_offense: Team):
        pass
    def update_score(self, team: Team, value: int, replace: bool = False):
        pass

games_to_sim = 1000
game_results = []
for i in range(games_to_sim):
    game = True
    quarter = 1
    time = 0.0
    home = teams[0]
    away = teams[1]
    home_score = 0
    away_score = 0
    teams_receive = [home, away]
    random.shuffle(teams_receive)
    offense = teams_receive[1]
    defense = teams_receive[0]
    pat = False
    kick_after_pat = False
    game_start = False
    down = 1
    to_go = 0
    dist = 65
    while game:
        if offense.Name == home.Name:
            margin = home_score - away_score
        else:
            margin = away_score - home_score
        minute, second = convert_float_time(time, quarter)
        #print(f"{"OT" if quarter == 5 else "Q"+str(quarter)}: {display_clock_time(minute, second)} | {display_down(down, to_go, pat, kick_after_pat)} | {yard_line(dist)} yard line | {offense.Name} {margin}")
        special = False
        if quarter % 2 == 1 and time == 0 and game_start == False:
            special = True
            if quarter == 1:
                result, desc, play_time, run_clock, onside_recovery = kickoff(defense,offense,False)
                time += play_time
                game_start = True
            elif quarter == 3:
                offense = teams_receive[0]
                defense = teams_receive[1]
                result, desc, play_time, run_clock, onside_recovery = kickoff(defense,offense,False)
                time += play_time
                game_start = True
            else:
                random.shuffle(teams_receive)
                offense = teams_receive[0]
                defense = teams_receive[1]
                result, desc, play_time, run_clock, onside_recovery = kickoff(defense,offense,False)
                time += play_time
                game_start = True
            down = 1
            to_go = 10
            dist = 100 - result
        elif kick_after_pat:
            special = True
            kick_after_pat = False
            result, desc, play_time, run_clock, onside_recovery = kickoff(offense, defense, False)
            down = 1
            to_go = 10
            dist = 100 - result
            time += play_time
            if not onside_recovery:
                new_offense = defense
                defense = offense
                offense = new_offense
        elif pat:
            special = True
            kick_after_pat = True
            pat = False
            result, desc, play_time, run_clock = point_after_touchdown(offense, defense, go_for_two(quarter, time, margin))
            if result == 101:
                if home.Name == offense.Name:
                    home_score += 1
                else:
                    away_score += 1
            elif result == 110:
                pass
            elif result >= 2 and result < 101:
                if home.Name == offense.Name:
                    home_score += 2
                else:
                    away_score += 2
            else:
                pass
        if not special:
            result, desc, play_time, run_clock = generate_play(offense, defense, down, to_go, dist, quarter, time, margin)
            if result == 300:
                if home.Name == offense.Name:
                    home_score += 3
                else:
                    away_score += 3
                kick_after_pat = True
                run_clock = False
            elif score_check(result, dist)[1] and "punt" not in desc:
                if home.Name == offense.Name:
                    home_score += 6
                else:
                    away_score += 6
                pat = True
                run_clock = False
            elif result >= to_go and "punt" not in desc:
                down = 1
                to_go = 10
                dist -= score_check(result, dist)[0]
            else:
                down += 1
                to_go -= result
                dist -= score_check(result, dist)[0]
            time += play_time
            if run_clock:
                time += 0.5
        if down > 4:
            new_offense = defense
            defense = offense
            offense = new_offense
            down = 1
            to_go = 10
            if dist == 0:
                dist = 25
            dist = 100 - dist
        #print(desc)
        #print(f"{home.Name} {home_score}, {away.Name} {away_score}\n")
        if time >= 15 and pat == False:
            quarter +=1
            time = 0
            if quarter == 3:
                game_start == False
            elif quarter > 5:
                game = False
            elif quarter > 4 and home_score != away_score:
                print(f"FINAL: {home} {home_score}, {away} {away_score}")
                game_results.append({home.Name: home_score, away.Name: away_score})
                game = False
            elif quarter > 4 and home_score == away_score:
                game_start = False

        if quarter == 5 and pat:
            print(f"FINAL: {home} {home_score}, {away} {away_score}")
            game_results.append({"Legends": home_score, "All Stars": away_score})
            game = False

home_avg = 0
away_avg = 0
for game in game_results:
    home_avg += game["Legends"]
    away_avg += game["All Stars"]
home_avg /= games_to_sim
away_avg /= games_to_sim

print(home_avg, away_avg)