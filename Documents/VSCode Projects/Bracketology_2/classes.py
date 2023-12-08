import datetime
import json

class Team:
    def __init__(self, name: str, gender: str):
        self.Name = name
        self.Gender = gender
        self.Roster = []
        self.Games = []
        Team.team_list.append(self)

    def __str__(self):
        return f"<{self.Name} ({self.Gender})>"
    
    team_list = []

    @classmethod
    def search_team(cls, name: str, gender: str):
        for team in Team.team_list:
            if team.Name == name and team.Gender == gender:
                return team
        print("No team found.")
        return None
    
    @classmethod
    def clean_duplicates(cls):
        for i,team in enumerate(Team.team_list):
            for j,check in enumerate(Team.team_list):
                if (team.Name == check.Name and 
                    team.Gender == check.Gender and i != j):
                    print(f"Duplicate found: {team.Name} ({team.Gender})")

    @classmethod
    def write_teams_to_json(cls, filename='teams.json'):
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
    def create_teams_from_json(cls, filename='teams.json'):
        try:
            with open(filename, 'r') as json_file:
                team_data_list = json.load(json_file)
            for team_data in team_data_list:
                try:
                    del team_data["Roster"]
                except:
                    pass
                team = Team(team_data["Name"], team_data["Gender"])
                del team_data["Name"]
                del team_data["Gender"]
                for key, val in team_data.items():
                    if key == "Games":
                        setattr(team, key, [])
                    else:
                        setattr(team, key, val)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

class Game:
    def __init__(self, home: Team, away: Team, home_score: int, 
                 away_score: int, gender: str, date: datetime):
        self.Home = home
        self.Away = away
        self.Home_Score = home_score
        self.Away_Score = away_score
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
    
    game_list = []

    @classmethod
    def search_games(cls, home: str, away: str, gender: str):
        games = []
        for game in Game.game_list:
            if game.Away.Name == away and game.Home.Name == home and game.Gender == gender:
                games.append(game)
        if len(games) == 0:
            print("No games found.")
        return games
    
    @classmethod
    def write_games_to_json(cls, filename='games.json'):
        game_data = []
        for game in cls.game_list:
            game_dict = {}
            for attr, value in vars(game).items():
                if not callable(value) and not attr.startswith("__"):
                    if type(value) == Team:
                        game_dict[attr] = value.Name
                    elif type(value) == datetime.date:
                        game_dict[attr] = value.isoformat()
                    else:
                        game_dict[attr] = value
            game_data.append(game_dict)
        with open(filename, 'w') as json_file:
            json.dump(game_data, json_file, indent=2)

    @classmethod
    def create_games_from_json(cls, filename='games.json'):
        try:
            with open(filename, 'r') as json_file:
                game_data_list = json.load(json_file)
            for game_data in game_data_list:
                game = Game(Team.search_team(game_data["Home"]),
                            Team.search_team(game_data["Away"]),
                            game_data["Home_Score"],
                            game_data["Away_Score"],
                            game_data["Gender"],
                            datetime.fromisoformat(game_data["Date"])
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
