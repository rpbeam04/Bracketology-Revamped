import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import json
import re

def scrape_to_soup(url: str):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def show_image_from_url(image_url):
    # Download the image from the URL
    response = requests.get(image_url)

    # Check if the image was successfully downloaded
    if response.status_code == 200:
        # Open and display the image using Pillow
        image = Image.open(BytesIO(response.content))
        image.show()
    else:
        print(f"Error: Unable to download image from URL. Status code: {response.status_code}")

def fetch_logo(team_name: str, logo_type: str = "primary", team_data: dict = None):
    if team_name.lower().startswith(("a","b","c")):
        league_id = 30
    elif team_name.lower().startswith(("d","e","f","g","h")):
        league_id = 31
    elif team_name.lower().startswith(("i","j","k","l","m")):
        league_id = 32
    elif team_name.lower().startswith(("n","o","p","q","r")):
        league_id = 33
    elif team_name.lower().startswith(("s","t")):
        league_id = 34
    elif team_name.lower().startswith(("u","v","w","x","y","z")):
        league_id = 35
    else:
        print("Error finding league id.")
        return None
    if not team_data:
        try:
            with open("Logos/all_team_data.json","r") as f:
                team_data = json.load(f)
        except:
            team_data = extract_team_id_data()
            
    query_team_name = team_data[team_name]["team_name"]
    team_id = str(team_data[team_name]["team_id"])
    image_id = str(team_data[team_name]["image_id"])
    year = str(team_data[team_name]["year"])
    logo_size = "full"
    
    image_url = f"https://content.sportslogos.net/logos/{league_id}/{team_id}/{logo_size}/{query_team_name}_logo_{logo_type}_{year}_sportslogosnet-{image_id}.png"

    response = requests.get(image_url)

    # Check if the image was successfully downloaded
    if response.status_code == 200:
        # Open and display the image using Pillow
        image = Image.open(BytesIO(response.content))
        image.save(f"Logos/{query_team_name}_{logo_type}.png")
    else:
        print(f"Error: Unable to download image from URL. Status code: {response.status_code}")

# team_name = "alabama_crimson_tide"
# fetch_logo(team_name)

def fetch_team_urls():
    image_urls = {}
    for _id in range(30,36):
        soup = scrape_to_soup(f"https://www.sportslogos.net/teams/list_by_league/{_id}")
        img_tags = soup.find_all('img')

        # Extract the source URLs from the image tags
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url and "content.sportslogos.net" in img_url:
                # Find the next sibling (the text following the image)
                text = img_tag.find_next_sibling(string = True)

                # Clean up the text (remove leading/trailing whitespaces)
                text = text.strip() if text else None
                try:
                    if text != "":
                        image_urls[text] = img_url
                except:
                    pass
    with open("Logos/team_ids.json","w") as f:
        json.dump(image_urls, f, indent=4)
    return image_urls

def extract_team_id_data():
    try:
        with open("Logos/team_ids.json","r") as f:
            team_urls: dict = json.load(f)
    except:
        team_urls: dict = fetch_team_urls()
    
    team_data = {}
    for name, url in team_urls.items():
        data_dict = {}
        data_dict["team_name"] = format_team_name(name)
        data_dict["src_url"] = url
        pattern = r"(\d+)\/thumbs\/(\d+)"
        match = re.search(pattern, url)
        if match:
            data_dict["team_id"] = match.group(1)
            group_2 = match.group(2)
            data_dict["image_id"] = group_2.removeprefix(str(match.group(1)))[0:4]
            data_dict["year"] = group_2.removeprefix(str(match.group(1)))[-4:]
        team_data[name] = data_dict
    with open("Logos/all_team_data.json","w") as f:
        json.dump(team_data, f, indent=4)
    return team_data
                
def format_team_name(team_name: str):
    return team_name.strip().replace(" ","_").lower()

with open("Logos/all_team_data.json","r") as f:
    team_data: dict = json.load(f)

for team in team_data.keys():
    fetch_logo(team_name=team, team_data=team_data)

# Still not working correctly