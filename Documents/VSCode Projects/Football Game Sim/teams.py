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