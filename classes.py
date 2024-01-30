import datetime
import json
import pandas as pd

class Team:
    def __init__(self, name: str, gender: str, conference: str):
        self.Name = name
        self.Gender = gender
        self.Conf = conference
        self.Conference = conference
        self.Roster = []
        self.Games = []
        Team.team_list.append(self)

    def __str__(self):
        return f"<{self.Name} ({self.Gender})>"
    
    team_list: list['Team'] = []

    @classmethod
    def search_team(cls, name: str, gender: str):
        team: Team
        if name == "_":
            return None
        if len(Team.team_list) == 0:
            print("Warning: no teams created.")
            return None
        with open('Teams/alias.json', 'r', encoding='utf-8') as f:
            aliases: dict = json.load(f)
        if name in list(aliases.keys()):
            name = aliases[name]
        for team in Team.team_list:
            if team.Name == name and team.Gender == gender:
                return team
        print(f"Error (search_team): No {name}, {gender} found.")
        with open('Teams/alias.json', 'r', encoding='utf-8') as f:
            alias_data = json.load(f)
        if name not in list(alias_data.keys()):
            alias_data.update({name: "_"})
        with open('Teams/alias.json', 'w', encoding='utf-8') as f:
            json.dump(alias_data, f, indent=2)
        return None
    
    @classmethod
    def clean_duplicates(cls):
        duplicates = []
        init_len = len(Team.team_list)
        team: Team
        check: Team
        for i,team in enumerate(Team.team_list):
            for j,check in enumerate(Team.team_list):
                if (team.Name == check.Name and 
                    team.Gender == check.Gender and i != j and
                    team not in duplicates):
                    #print(f"Duplicate found: {team.Name} ({team.Gender})")
                    duplicates.append(check)
        for team in duplicates:
            Team.team_list.remove(team)
            del(team)
        print(f"Team List: {init_len} --> {len(Team.team_list)} teams.")

    @classmethod
    def write_teams_to_json(cls, filename='Teams/teams.json'):
        team_data = []
        for team in cls.team_list:
            team_dict = {}
            for attr, value in vars(team).items():
                if not callable(value) and not attr.startswith("__"):
                    team_dict[attr] = value
            team_data.append(team_dict)
        with open(filename, 'w') as json_file:
            json.dump(team_data, json_file, indent=2)

    @classmethod
    def create_teams_from_json(cls, filename='Teams/teams.json'):
        try:
            with open(filename, 'r') as json_file:
                team_data_list = json.load(json_file)
            for team_data in team_data_list:
                try:
                    del team_data["Roster"]
                except:
                    pass
                team = Team(team_data["Name"], team_data["Gender"], team_data["Conference"])
                del team_data["Name"]
                del team_data["Gender"]
                del team_data["Conference"]
                for key, val in team_data.items():
                    if key == "Games":
                        setattr(team, key, [])
                    else:
                        setattr(team, key, val)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    @classmethod
    def create_teams_from_stats(cls, gender: str = "men", write_to_json: bool = False):
        """
        Since write to json will reset all other teams, only do so after creating mens and womens teams.
        """
        try:
            ratings = pd.read_csv(fr"Stats/{gender.lower()}/ratings.csv")
        except:
            print("Error: No stats files.")
            return None
        for _, row in ratings[["School","Conf"]].iterrows():
            Team(name = row["School"], gender = gender.lower(), conference = row["Conf"])
        Team("Non D1",gender.lower(),"D2")
        if write_to_json:
            Team.write_teams_to_json()

    @classmethod
    def find_teams_in_conference(cls, conference: str, gender: str = "men"):
        team: Team
        members: list[Team] = []
        for team in Team.team_list:
            if isinstance(team.Conf, str):
                if team.Conf == conference and team.Gender == gender:
                    members.append(team)
            else:
                if team.Conf.Name == conference and team.Gender == gender:
                    members.append(team)
        return members
    
    @classmethod
    def clear_teams(cls):
        for team in Team.team_list:
            del(team)
        Team.team_list = []

class Game:
    def __init__(self, home: Team, away: Team, home_score: int, 
                 away_score: int, gender: str, date: datetime):
        self.Home = home
        self.Away = away
        self.Home_Score = int(home_score)
        self.Away_Score = int(away_score)
        self.Gender = gender
        self.Date = date
        self.Neutral = False
        if self.Home_Score > 0 or self.Away_Score > 0:
            self.Complete = True
        else:
            self.Complete = False
        Game.game_list.append(self)
        home.Games.append(self)
        away.Games.append(self)

    def __str__(self):
        return f"<{self.Away.Name} @ {self.Home.Name} ({self.Home.Gender[0]})| {self.Date.month}-{self.Date.day}>"
    
    game_list: list['Game'] = []

    @classmethod
    def search_games(cls, home: str, away: str, gender: str):
        games: list[Game] = []
        game: Game
        for game in Game.game_list:
            if game.Away.Name == away and game.Home.Name == home and game.Gender == gender:
                games.append(game)
        if len(games) == 0:
            print("No games found.")
        return games
    
    @classmethod
    def write_games_to_json(cls, filename='Games/games.json'):
        game_data = []
        for game in cls.game_list:
            game_dict = {}
            for attr, value in vars(game).items():
                if not callable(value) and not attr.startswith("__"):
                    if type(value) == Team:
                        game_dict[attr] = value.Name
                    elif type(value) == datetime.datetime or type(value) == datetime.date:
                        game_dict[attr] = value.isoformat()
                    else:
                        game_dict[attr] = value
            game_data.append(game_dict)
        with open(filename, 'w') as json_file:
            json.dump(game_data, json_file, indent=2)

    @classmethod
    def create_games_from_json(cls, filename='Games/games.json'):
        try:
            with open(filename, 'r') as json_file:
                game_data_list = json.load(json_file)
            for game_data in game_data_list:
                game = Game(Team.search_team(game_data["Home"], game_data["Gender"]),
                            Team.search_team(game_data["Away"], game_data["Gender"]),
                            game_data["Home_Score"],
                            game_data["Away_Score"],
                            game_data["Gender"],
                            datetime.datetime.fromisoformat(game_data["Date"])
                            )
                del game_data["Home"]
                del game_data["Away"]
                del game_data["Home_Score"]
                del game_data["Away_Score"]
                del game_data["Gender"]
                del game_data["Date"]
                for key, val in game_data.items():
                    setattr(game, key, val)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
    
class Player:
    def __init__(self, name: str, position: str, team: Team):
        self.Name = name
        self.Pos = position
        self.Position = position
        self.Team = team
        self.Gender = team.Gender
        team.Roster.append(self)

    def __str__(self):
        return f"{self.Name} ({self.Pos})"

class Conference:
    def __init__(self, name: str, gender: str):
        self.Name = name
        self.Gender = gender
        self.Teams = []
        for team in Team.team_list:
            if team.Conf == name and team.Gender == gender:
                self.Teams.append(team)
                team.Conf = self
                team.Conference = self
        Conference.conf_list.append(self)
    
    def __str__(self):
        return f"Conf: {self.Name}, {self.Gender}"
    
    conf_list: list['Conference'] = []

    @classmethod
    def search_conference(cls, name: str, gender: str):
        conf: Conference
        if name == "_":
            return None
        if len(Conference.conf_list) == 0:
            print("Warning: no conferences created.")
            return None
        with open('Teams/alias.json', 'r', encoding='utf-8') as f:
            aliases: dict = json.load(f)
        if name in list(aliases.keys()):
            name = aliases[name]
        for conf in Conference.conf_list:
            if conf.Name == name and conf.Gender == gender:
                return conf
        print(f"Error (search_conference): No {name}, {gender} found.")
        with open('Teams/alias.json', 'r', encoding='utf-8') as f:
            alias_data = json.load(f)
        if name not in list(alias_data.keys()):
            alias_data.update({name: "_"})
        with open('Teams/alias.json', 'w', encoding='utf-8') as f:
            json.dump(alias_data, f, indent=2)
        return None

    @classmethod
    def write_conferences_to_json(cls, filename='Teams/conferences.json'):
        conf_data = []
        for conf in cls.conf_list:
            conf_dict = {}
            for attr, value in vars(conf).items():
                if not callable(value) and not attr.startswith("__"):
                    conf_dict[attr] = value
                if attr == "Teams":
                    teams = [team.Name for team in value]
                    conf_dict[attr] = teams
            conf_data.append(conf_dict)
        with open(filename, 'w') as json_file:
            json.dump(conf_data, json_file, indent=2)

    @classmethod
    def create_conferences_from_json(cls, filename='Teams/conferences.json'):
        try:
            with open(filename, 'r') as json_file:
                conf_data_list = json.load(json_file)
            for conf_data in conf_data_list:
                conf = Conference(conf_data["Name"], conf_data["Gender"])
                del conf_data["Name"]
                del conf_data["Gender"]
                for key, val in conf_data.items():
                    if key == "Teams":
                        teams = [Team.search_team(name, conf.Gender) for name in val]
                        setattr(conf, key, teams)
                    else:
                        setattr(conf, key, val)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")