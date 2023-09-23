# url to download icon file
# https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{app_id}/{client_icon_filename}
# https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/497400/597ba5dfca98cf68bbd1fd5e080e70518387b3dd.ico

import os
import requests

# list directory of this folder ( Desktop )
files = os.listdir('.')

# get all .url file, url file is steam shortcut file
shortcuts = [file for file in files if file.endswith('.url')]

# Store all Steam games in games dictionaries
games = []

# loop shortcuts to fetch all Steam games needed data
for shortcut in shortcuts:
    game = {}
    with open(shortcut, "r") as file:
        lines = file.readlines()

    for line in lines:
        if "URL=steam:" in line:
            game["app_id"] = line.strip()[22:]

        if "IconFile" in line:
            game["icon_filename"] = line.strip().split('\\')[-1:][0]
            game["icon_install"] = line.strip()[9:]

    if(len(game) == 3):
        games.append(game)

# Loop game data to download all icons and store it
for game in games:
    base = "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/"
    url = base + game["app_id"] + "/" + game["icon_filename"]
    
    print(f"Download from: {url}")
    response = requests.get(url)

    if response.status_code == 200:
        with open(game["icon_install"], "wb") as icon_file:
            icon_file.write(response.content)

    else:
        print(f"Failed to download Client Icon from URL: {url}")
