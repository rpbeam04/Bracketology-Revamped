import random
import numpy as np
import pandas as pd
import math
import scipy
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
from pprint import *
from teams import *

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
        400: touchback
    desc: str, description of the play
    play_time: float, time taken by the play
    run_clock: bool, whether the clock keeps running after the play
    
    This function generates a play between the two teams according to the given parameters, and returns the result and stats.
    """
    # Conditions for non-standard plays (special teams, end of half, etc)
    if down == 4 and not go_for_it(quarter, to_go, dist, time, margin, 0):
        result, desc, play_time, test = special_teams(offense, quarter, time, dist, margin)
        return result, desc, play_time, False
    
    # Run Pass Modifiers
    run_rate = offense.Run_Rate

    # Standard play simulation logic (0 is run, 1 is pass)
    play_type = 0 if random.random() < run_rate else 1
    
    # Yardage and Stats calculations
    # Evenutally, defense will play a role in these
    cmp_pct = offense.Completion_Pct
    ypcmp = offense.Yds_per_Completion
    ypc = offense.Yds_per_Carry
    
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
    if not(margin >= -3 and margin <= 0 and dist < 40):
        if quarter == 4 and margin < 0:
            if to_go < 5 and dist < 50:
                return True
            if time > 10 and margin >= -8:
                return True
        return False
    return False
    
def special_teams(offense: Team, quarter, time, dist, margin):
    if dist < 43:
        a = -4.4947 * 10**(-126)
        b = 1.736 * 10**9
        c = 0.993889
        d = 89.081
        outcome = success(a*math.log(b*(dist+17))**d + c + 0.01)
        if outcome:
            return 300, f"{offense.return_starter("PK")} {dist+17} yard field goal is good.", 0.1, False
        else:
            return 0, f"{offense.return_starter("PK")} {dist+17} yard field goal is no good.", 0.1, False
    else:
        punt = rand_norm_int(45,10)
        touchback = ""
        if punt < 25:
            punt = rand_norm_int(35,5)
        while punt < 0:
            punt = rand_norm_int(45,10)
        if dist - punt <= 0:
            punt = dist
            touchback = " Touchback."
        return punt, f"{offense.return_starter("PP")} punt for {punt} yards.{touchback}", 1/6, False

def yard_line(distance):
    """
    Convert distance from end zone to yard line.
    """
    if distance > 50:
        return 100 - distance
    return distance

def success(pct):
    """
    Given pct [0,1], returns random trial result where pct is chance of success.
    """
    outcome = random.random()
    if outcome <= pct:
        return True
    return False

def convert_float_time(time, quarter):
    if quarter <= 4:
        minute = 15 - math.ceil(time)
    else:
        minute = 10 - math.ceil(time)
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
            return 25, f"{kicking.Name} kick off for a touchback.", 0, False, False
        else:
            yards = rand_norm_int(22,8)
            if yards <= 10:
                yards = rand_norm_int(18,5)
            while yards <= 0:
                yards = rand_norm_int(18,5)
            return yards, f"{kicking.Name} kickoff, returned for {yards} yards by {receiving.return_starter("WR")}.", 0.1, False, False
    else:
        yards =  rand_norm_int(54,2)
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
    margins = [-10,-5,-2,1,5]
    if quarter == 4:
        if margin in margins:
            return True
        elif margin == -8:
            return success(0.5)
    return False

def point_after_touchdown(offense: Team, defense: Team, two_pt_conv: bool = False):
    if not two_pt_conv:
        outcome = success(0.95)
        if outcome:
            return 101, f"PAT attempt by {offense.return_starter("PK")} is good.", 0, False
        else:
            return 110, f"PAT attempt by {offense.return_starter("PK")} is no good.", 0, False
    else:
        result, desc, play_time, run_clock = generate_play(offense, defense, 1, 2, 2, 1, 5, 0)
        return result, f"{desc}", play_time, run_clock

def display_down(down, to_go, pat, kick_after_pat):
    if pat:
        return "PAT"
    elif kick_after_pat:
        return "Kickoff"
    else:
        if down == 1:
            suffix = "st"
        elif down == 2:
            suffix = "nd"
        elif down == 3:
            suffix = "rd"
        else:
            suffix = "th"
        return f"{down}{suffix} & {to_go}"