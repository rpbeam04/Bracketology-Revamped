import datetime
import json
import pandas as pd

class Team:
    def __init__(self, name: str, gender: str, conference: str, year: int):
        self.Name = name
        self.Gender = gender
        self.Conf = conference
        self.Year = year
        self.Roster = []
        self.Games = []
        Team.team_list.append(self)

    def __str__(self):
        return f"<{self.Name} ({self.Gender}-{self.Year})>"
    
    team_list: list['Team'] = []

    def rec_to_pct(self, record: str):
        record = getattr(self, record)
        record = record.split("-")
        w = int(record[0].strip())
        l = int(record[1].strip())
        return round(w/(w+l),4)
    
    def comb_rec_to_pct(self, records: list[str]):
        ws = []
        ls = []
        for record in records:
            record = getattr(self, record)
            record = record.split("-")
            ws.append(int(record[0].strip()))
            ls.append(int(record[1].strip()))
        return round(sum(ws)/(sum(ws)+sum(ls)),4)

    def per_game(self, stat: str):
        try:
            games = self.G
            stat = getattr(self, stat)
            return stat/games
        except:
            print("Error (per game): make sure stats loaded.")
            return None

    def stat_rank(self, stat: str, per_game: bool = False, descend: bool = True):
        team_stat = {}
        gender = self.Gender
        year = self.Year
        for team in [team for team in Team.team_list if team.Name != "Non D1"]:
            if team.Year == year and team.Gender == gender.lower():
                statv = getattr(team, stat)
                if per_game:
                    statv = team.per_game(stat)
                team_stat[team.Name] = statv
        team_stat = dict(sorted(team_stat.items(), key=lambda item: item[1], reverse=descend))
        return list(team_stat.keys()).index(self.Name)+1

    def stat_rank_p6(self, stat: str, per_game: bool = False, descend: bool = True):
        team_stat = {}
        gender = self.Gender
        year = self.Year
        for team in [team for team in Team.team_list if team.Name != "Non D1"]:
            if team.Conf in ["ACC","SEC","Big Ten","Pac-12","Big 12","Big East"] and team.Year == year and team.Gender == gender.lower():
                statv = getattr(team, stat)
                if per_game:
                    statv = team.per_game(stat)
                team_stat[team.Name] = statv
        team_stat = dict(sorted(team_stat.items(), key=lambda item: item[1], reverse=descend))
        return list(team_stat.keys()).index(self.Name)+1

    @classmethod
    def filtered_team_list(cls, gender: str | list[str], year: int | list[int], power_6: bool = False, non_d1: bool = False):
        if isinstance(gender, str):
            gender = [gender]
        if isinstance(year, int):
            year = [year]
        if non_d1:
            tl = [team for team in Team.team_list if team.Gender in gender and team.Year in year]
        else:
            tl = [team for team in Team.team_list if team.Gender in gender and team.Year in year and team.Name != "Non D1"]
        if power_6:
            return [team for team in tl if team.Conf in ["ACC","SEC","Big Ten","Pac-12","Big 12","Big East"]]
        else:
            return tl

    @classmethod
    def stat_rankings(cls, stat: str, gender: str, year: int, per_game: bool = False, descend: bool = True):
        team_stat = {}
        for team in [team for team in Team.team_list if team.Name != "Non D1"]:
            if team.Year == year and team.Gender == gender.lower():
                statv = getattr(team, stat)
                if per_game:
                    statv = team.per_game(stat)
                team_stat[team.Name] = statv
        team_stat = dict(sorted(team_stat.items(), key=lambda item: item[1], reverse=descend))
        for i, key in enumerate(list(team_stat.keys())):
            team_stat[key] = (i+1, team_stat[key])
        return team_stat
    
    @classmethod
    def stat_rankings_p6(cls, stat: str, gender: str, year: int, per_game: bool = False, descend: bool = True):
        team_stat = {}
        for team in [team for team in Team.team_list if team.Name != "Non D1"]:
            if team.Conf in ["ACC","SEC","Big Ten","Pac-12","Big 12","Big East"] and team.Year == year and team.Gender == gender.lower():
                statv = getattr(team, stat)
                if per_game:
                    statv = team.per_game(stat)
                team_stat[team.Name] = statv
        team_stat = dict(sorted(team_stat.items(), key=lambda item: item[1], reverse=descend))
        for i, key in enumerate(list(team_stat.keys())):
            team_stat[key] = (i+1, team_stat[key])
        return team_stat

    @classmethod
    def search_team(cls, name: str, gender: str, year: int = 2024):
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
            if team.Name == name and team.Gender == gender and team.Year == year:
                return team
        print(f"Error (search_team): No {name}, {gender}, {year} found.")
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
                    team.Year == check.Year and
                    team not in duplicates):
                    #print(f"Duplicate found: {team.Name} ({team.Gender}-{team.Year})")
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
                if isinstance(value, Conference):
                    continue
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
                team = Team(team_data["Name"], team_data["Gender"], team_data["Conf"], team_data["Year"])
                del team_data["Name"]
                del team_data["Gender"]
                del team_data["Conf"]
                del team_data["Year"]
                for key, val in team_data.items():
                    if key == "Games":
                        setattr(team, key, [])
                    else:
                        setattr(team, key, val)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    @classmethod
    def create_teams_from_stats(cls, gender: str = "men", year: int = 2024, write_to_json: bool = False):
        """
        Since write to json will reset all other teams, only do so after creating mens and womens teams.
        """
        try:
            ratings = pd.read_csv(fr"Stats/{year}/{gender.lower()}/ratings.csv")
        except:
            print("Error: No stats files.")
            return None
        for _, row in ratings[["School","Conf"]].iterrows():
            Team(name = row["School"], gender = gender.lower(), conference = row["Conf"], year = year)
        Team("Non D1", gender.lower(), "D2", year)
        if write_to_json:
            Team.write_teams_to_json()

    @classmethod
    def find_teams_in_conference(cls, conference: str, gender: str = "men", year: int = 2024):
        team: Team
        members: list[Team] = []
        for team in Team.team_list:
            if isinstance(team.Conf, str):
                if team.Conf == conference and team.Gender == gender and team.Year == year:
                    members.append(team)
            else:
                if team.Conference.Name == conference and team.Gender == gender and team.Year == year:
                    members.append(team)
        return members
    
    @classmethod
    def clear_teams(cls):
        for team in Team.team_list:
            del(team)
        Team.team_list = []

class Game:
    # Note: Games have not yet had multi-season functionality implemented, be careful with that
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
    def __init__(self, name: str, gender: str, year: int):
        self.Name = name
        self.Gender = gender
        self.Year = year
        self.Teams = []
        for team in Team.team_list:
            if team.Conf == name and team.Gender == gender and team.Year == year:
                self.Teams.append(team)
                team.Conference = self
        Conference.conf_list.append(self)
    
    def __str__(self):
        return f"Conf: {self.Name}, {self.Gender}-{self.Year}"
    
    conf_list: list['Conference'] = []

    @classmethod
    def search_conference(cls, name: str, gender: str, year: int):
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
            if conf.Name == name and conf.Gender == gender and conf.Year == year:
                return conf
        print(f"Error (search_conference): No {name}, {gender}, {year} found.")
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
                conf = Conference(conf_data["Name"], conf_data["Gender"], conf_data["Year"])
                del conf_data["Name"]
                del conf_data["Gender"]
                del conf_data["Year"]
                for key, val in conf_data.items():
                    if key == "Teams":
                        teams = [Team.search_team(name, conf.Gender, conf.Year) for name in val]
                        setattr(conf, key, teams)
                    else:
                        setattr(conf, key, val)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    @classmethod
    def create_conferences_from_stats(cls, gender: str = "men", year: int = 2024, write_to_json: bool = False):
        try:
            df = pd.read_csv(fr"Stats/{year}/{gender.lower()}/ratings.csv")
        except:
            print("Error creating conferences: no stats.")
            return None
        for conf_name in list(df["Conf"].unique()):
            Conference(conf_name, gender, year)
        if write_to_json:
            Conference.write_conferences_to_json()

    def conf_stat_rankings(self, stat: str, per_game: bool = False, descend: bool = True):
        team_stat = {}
        team: Team
        for team in self.Teams:
                if per_game:
                    team_stat[team.Name] = team.per_game(stat)
                else:
                    team_stat[team.Name] = getattr(team, stat)
        team_stat = dict(sorted(team_stat.items(), key=lambda item: item[1], reverse=descend))
        for i, key in enumerate(list(team_stat.keys())):
            team_stat[key] = (i+1, team_stat[key])
        return team_stat