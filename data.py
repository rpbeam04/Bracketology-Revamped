import pandas as pd
from classes import *
import fetch
from pprint import *
import os
from sklearn.preprocessing import StandardScaler

def populate_team_stats(year: int, gender: str):
    tables = list(fetch.fetch_team_stats(year, gender).values())
    table: pd.DataFrame
    for table in tables:
        for _,row in table.iterrows():
            team = Team.search_team(row["School"], gender, year)
            for item in list(row.keys()):
                if item not in ["School","Rk"]:
                    setattr(team, item, row[item])

def populate_team_metrics(year: int, gender: str):
    tables = []
    tables.append(fetch.fetch_net_rankings(year, gender)[0])
    tables.append(fetch.fetch_rpi_rankings(year, gender))
    table: pd.DataFrame
    for table in tables:
        for _,row in table.iterrows():
            team = Team.search_team(row["Team"], gender, year)
            cols = list(row.keys())
            item: str
            for item in cols:
                if item == "Team" or item.endswith(".1") or item.startswith("Unnamed"):
                    continue
                elif item == "NET_Rank":
                    setattr(team, "NET", row[item])
                elif item in ["NC_SOS","Q1","Q2","Q3","Q4","SOS"] and "RPI" in cols:
                    try:
                        val = row[item].replace(" ","")
                    except:
                        val = row[item]
                    setattr(team, f"{item}_RPI", val)
                elif item in ["SOS","Q1","Q2","Q3","Q4","NC_SOS"] and "NET" in cols:
                    try:
                        val = row[item].replace(" ","")
                    except:
                        val = row[item]
                    setattr(team, f"{item}_NET", val)
                else:
                    setattr(team, item, row[item])

def populate_conference_metrics(year: int, gender: str):
    table = fetch.fetch_net_rankings(year, gender)[1]
    for _,row in table.iterrows():
        conf = Conference.search_conference(row["Conference"], gender, year)
        cols = list(row.keys())
        item: str
        for item in cols:
            if item == "Conference":
                continue
            elif item == "Conference_Leader":
                setattr(conf, item, row[item])
            else:
                try:
                    val = row[item].replace(" ","")
                except:
                    val = row[item]
                setattr(conf, item, val)

def populate_tournament_data(year: int, gender: str):
    data = fetch.fetch_tourney_seed_data(year, gender)
    for _, row in data.iterrows():
        team = Team.search_team(row["School"], gender, year)
        for item in list(data.columns):
            if item not in ["School", "Conference"]:
                setattr(team, item, row[item])

def team_training_data(year: int, gender: str, predictive: bool = False, refresh: bool = False):
    filepath = fr"Model/{year}/{gender.lower()}"
    if not refresh and os.path.exists(fr"{filepath}/training.csv"):
        data = pd.read_csv(fr"{filepath}/training.csv")
        return data

    n_teams = pd.read_csv(fr"Stats/{year}/{gender.lower()}/school-stats.csv").shape[0]    
    # ML Data Points (NEED TO SWITCH RPI OUT FOR NET B/C IT SUCKS BUT THE DATA WAS EASY TO GET)
    #  Adj_NRtg
    #  NC_Rec to percent
    #  NC_SOS_RPI
    #  NET_Rank
    #  Pre_Tourn_Record to percent
    #  Q1_RPI to pct
    #  Q3_RPI + Q4_RPI to pct
    #  SOS (archived)
    #  NC_WP (Conf)
    header = ["Seed","Name","Adj_NRtg","NC_Rec","NC_SOS_RPI","NET",
              "Record","Q1","Q2","Q34","Conf_NC_WP"]
    rows = []
    if predictive:
        header.remove("Seed")
    for team in Team.filtered_team_list(gender, year):
        if hasattr(team, "Adj_NRtg"):
            row = []
            for h in header:
                if h == "NC_Rec":
                    row.append(team.rec_to_pct("NC_Rec"))
                elif h == "Record":
                    if hasattr(team, "Pre_Tourn_Record"):
                        row.append(team.rec_to_pct("Pre_Tourn_Record"))
                    else:
                        row.append(team.W_L_Pct)
                elif h == "Q1":
                    row.append(team.rec_to_pct("Q1_RPI"))
                elif h == "Q2":
                    row.append(team.rec_to_pct("Q2_RPI"))
                elif h == "Q34":
                    row.append(team.comb_rec_to_pct(["Q3_RPI","Q4_RPI"]))
                elif h == "Conf_NC_WP":
                    if not hasattr(team.Conference, "NC_WP"):
                        print(team.Name, team.Gender)
                    row.append(team.Conference.NC_WP)
                elif h == 'Name':
                    row.append(f"{team.Name}{"-"+str(team.Year) if not predictive else ''}")
                elif h == 'Seed':
                    if hasattr(team, "Seed"):
                        row.append((17-team.Seed)/16)
                    else:
                        row.append(0)
                else:
                    row.append(getattr(team, h))
            rows.append(row)
    data = pd.DataFrame(rows, columns=header)
    data.apply(pd.to_numeric, errors = 'ignore')
    for col in [col for col in data.columns if col not in ["Seed","Name"]]:
        if col in ["NC_SOS_RPI","NET"]:
            data[col] = (n_teams-data[col])/(n_teams-1)
            values = data[col].values.reshape(-1, 1)
            data[col] = StandardScaler().fit_transform(values)
            data[col] = data[col].apply(lambda x: round(x,4))
        else:
            values = data[col].values.reshape(-1, 1)
            data[col] = StandardScaler().fit_transform(values)
            data[col] = data[col].apply(lambda x: round(x,4))
    if not predictive:
        data = data[data['Seed'] > 0]
    filepath = fr"Model/{year}/{gender.lower()}"
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    data = data.reset_index(drop=True)
    data.to_csv(fr"{filepath}/training.csv", index=False)
    return data

def create_full_training(current_year: int = 2024, gender: str = None):
    dirs = os.listdir("Model")
    data = []
    for d in dirs:
        if not (d.endswith(".csv") or d.endswith(".pkl")) and int(d) != current_year and int(d) != 2019:
            try:
                if gender != "women":
                    data.append(pd.read_csv(fr"Model/{d}/men/training.csv"))
            except:
                pass
            try:
                if gender != "men":
                    data.append(pd.read_csv(fr"Model/{d}/women/training.csv"))
            except:
                pass
    full = pd.concat(data)
    full.to_csv("Model/full-training.csv", index=False)
    return full

def full_object_sourcing(refresh: bool = False):
    # FULL OBJECT SOURCING
    Team.clear_teams()
    genders = ["women","men"]
    years = [2021,2022,2023,2024]
    for gender in genders:
        if gender == "men":
            years.insert(0,2019)
        for year in years:
            refr = False
            if year == 2024:
                refr = refresh
            print(year, gender)
            fetch.fetch_team_stats(year, gender, refresh_override=refr)
            Team.create_teams_from_stats(gender, year)
            Conference.create_conferences_from_stats(gender, year)
            fetch.fetch_net_rankings(year, gender, refr)
            fetch.fetch_rpi_rankings(year, gender, refr)
            populate_team_stats(year, gender)
            populate_team_metrics(year, gender)
            populate_conference_metrics(year, gender)
            if year != 2024:
                populate_tournament_data(year, gender)
                if year != 2019:
                    team_training_data(year, gender)
            if year == 2024:
                team_training_data(year, gender, True)
    Team.clean_duplicates()
    Team.write_teams_to_json()
    Conference.write_conferences_to_json()
    create_full_training()
    if not refresh:
        matrix: pd.DataFrame = fetch.scrape_tables_from_url("http://www.bracketmatrix.com/")[0]
        matrix.to_csv("Model/matrix.csv")
    return None