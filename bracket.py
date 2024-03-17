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

# region_names = ["East","South","Midwest","West"]

# html_region = f"""
# <!DOCTYPE html>
# <html lang="en">

# <head>
#   <meta charset="UTF-8">
#   <title id="title">{region_name}</title>
#   <link href="https://fonts.googleapis.com/css?family=Poppins" rel="stylesheet">
# </head>

# <body>
#   <main id="tournament">
#     <ul class="round round-1">
#       <li class="spacer"></li>
#       <li class="game game-top"><rb>1) </rb><span></span>{Louisville}</li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom "><rb>16) </rb>NC A&T <span></span></li>
#       <li class="spacer"></li>
#       <li class="game game-top winner">Colo St <span>84</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom ">Missouri <span>72</span></li>
#       <li class="spacer"></li>
#       <li class="game game-top ">Oklahoma St <span>55</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom winner">Oregon <span>68</span></li>
#       <li class="spacer"></li>
#       <li class="game game-top winner">Saint Louis <span>64</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom ">New Mexico St <span>44</span></li>
#       <li class="spacer"></li>
#       <li class="game game-top winner">Memphis <span>54</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom ">St Mary's <span>52</span></li>
#       <li class="spacer"></li>
#       <li class="game game-top winner">Mich St <span>65</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom ">Valparaiso <span>54</span></li>
#       <li class="spacer"></li>
#       <li class="game game-top winner">Creighton <span>67</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom ">Cincinnati <span>63</span></li>
#       <li class="spacer"></li>
#       <li class="game game-top winner">Duke <span>73</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom ">Albany <span>61</span></li>
#       <li class="spacer"></li>
#     </ul>
#     <ul class="round round-2">
#       <li class="spacer"></li>
#       <li class="game game-top winner">Lousville <span>82</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom ">Colo St <span>56</span></li>
#       <li class="spacer"></li>
#       <li class="game game-top winner">Oregon <span>74</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom ">Saint Louis <span>57</span></li>
#       <li class="spacer"></li>
#       <li class="game game-top ">Memphis <span>48</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom winner">Mich St <span>70</span></li>
#       <li class="spacer"></li>
#       <li class="game game-top ">Creighton <span>50</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom winner">Duke <span>66</span></li>
#       <li class="spacer"></li>
#     </ul>
#     <ul class="round round-3">
#       <li class="spacer"></li>
#       <li class="game game-top winner">Lousville <span>77</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom ">Oregon <span>69</span></li>
#       <li class="spacer"></li>
#       <li class="game game-top ">Mich St <span>61</span></li>
#       <li class="game game-spacer">&nbsp;</li>
#       <li class="game game-bottom winner">Duke <span>71</span></li>
#       <li class="spacer"></li>
#     </ul>
#     <ul class="round round-4">
#       <li class="spacer"></li>
#       <li class="game game-top winner">Lousville <span>85</span></li>
#       <li class="game game-spacer"></li>
#       <li class="game game-bottom ">Duke <span>63</span></li>
#       <li class="spacer"></li>
#     </ul>
#     <ul class="round round-5">
#       <li class="spacer"></li>
#       <li class="game game-top">Lousville</span></li>
#       <li class="spacer"></li>
#     </ul>
#   </main>
#   <style>
#     /*
#      *  Flex Layout Specifics
#       */
#     main {{
#       display: flex;
#       flex-direction: row;
#     }}

#     h1 {{
#       text-align: center;
#       margin-top: 50px;
#       margin-bottom: 50px;
#     }}

#     .round {{
#       display: flex;
#       flex-direction: column;
#       justify-content: center;
#       min-width: 120px;
#       list-style: none;
#       padding: 0;
#     }}

#     .round .spacer {{
#       flex-basis: 4px;
#       flex-grow: 2;
#     }}

#     .round .spacer:first-child,
#     .round .spacer:last-child {{
#       flex-grow: 1;
#     }}

#     .round .game-spacer {{
#       flex-basis: 2px;
#       flex-grow: 2;
#     }}

#     /*
#      *  General Styles
#     */
#     body {{
#       font-family: "Poppins", sans-serif;
#       font-weight: 400;
#       font-size: 8pt;
#       padding: 0px;
#       line-height: 1.1em;
#     }}

#     li.game {{
#       padding-left: 10px;
#     }}

#     li.game.winner {{
#       font-style: italic;
#     }}

#     li.game span {{
#       float: right;
#       margin-right: 8px;
#     }}

#     li.game-top {{
#       border-bottom: 1px solid #aaa;
#       padding-right: 1px;
#     }}

#     li.game-spacer {{
#       border-right: 1px solid #aaa;
#     }}

#     li.game-bottom {{
#       border-right: 1px solid #aaa;
#       border-bottom: 1px solid #aaa;
#     }}
#   </style>
# </body>

# </html>
# """