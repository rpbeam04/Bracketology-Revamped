import pandas as pd
from classes import Team, Conference

def create_bracket(gender: str, season: int, conference_champions: list[dict] = None):
    teams = Team.filtered_team_list(gender, season)
    assert hasattr(teams[0], "Predicted_Seed"), "Error: seeds have not been predicted."
    teams = sorted(teams, key=lambda x: getattr(x, "Predicted_Seed"))
    auto_bids = conference_champions
    if auto_bids:
        for i,bid in enumerate(auto_bids):
            conf = Conference.search_conference(list(bid.keys())[0], gender, season)
            team = Team.search_team(list(bid.values())[0], gender, season)
            auto_bids[i] = {conf: team}
        auto_confs = [list(bid.keys())[0] for bid in auto_bids]
        auto_teams = [list(bid.values())[0] for bid in auto_bids]
    else:
        auto_confs = []
        auto_teams = []
    at_large_teams = []
    bubble = []
    n_conferences = len(Conference.filtered_conference_list(gender, season)) - len(auto_confs)
    team: Team
    for team in teams:
        if team in auto_teams:
            team.Bid = "Auto"
            continue
        elif team.Conference not in auto_confs and team.Conference.Name != "Ind":
            team.Bid = "Auto"
            auto_teams.append(team)
            auto_confs.append(team.Conference)
            n_conferences -= 1
        elif len(at_large_teams) + len(auto_teams) + n_conferences < 68:
            team.Bid = "At-Large"
            at_large_teams.append(team)
        elif len(bubble) < 8:
            team.Bid = "Bubble"
            bubble.append(team)
        else:
            continue
    field = sorted(auto_teams+at_large_teams, key = lambda x: getattr(x, "Predicted_Seed"), reverse=True)
    at_large_ct = 0
    team: Team
    for i,team in enumerate(field):
        if i < 4:
            team.First_Four = True
        elif team.Bid == "At-Large" and at_large_ct < 4:
            team.First_Four = True
            at_large_ct += 1
        else:
            team.First_Four = False
    
    seed = 16
    current_seed_ct = 0
    bubble_ct = 0
    bubble_flag = False
    only_auto = True 
    for team in field:
        if seed != 16 and current_seed_ct >= 4:
            seed -= 1
            current_seed_ct = 0
        elif seed == 16 and current_seed_ct >= 6:
            seed -= 1
            current_seed_ct = 0
        if team.Bid == "At-Large" and bubble_flag:
            team.Seed = bubble_seed
            bubble_flag = False
            bubble_ct += 1
        else:
            current_seed_ct += 1
            team.Seed = seed
        if only_auto and team.Bid != "Auto" and bubble_ct < 2:
            bubble_flag = True
            bubble_seed = seed

    field.reverse()
    with open(fr"test-{gender}.txt", "w") as f:
        for team in field:
            f.write(f"{team.Seed}\t{team.Name}\t{team.Bid}\t{team.First_Four}\n")
        f.write("\nFirst Teams Out\n")
        for i,team in enumerate(bubble):
            f.write(f"{i}\t{team.Name}\n")