import csv
import numpy
from lxml import html
import requests, re, math
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
players = []
with open('playerDB.csv', mode='r') as player_csv:
    player_reader = csv.DictReader(player_csv)
    line_count = 0
    for row in player_reader:
        players.append(dict(row))

plr_draft_yr = {}

for player in players:
    if 'Draft' not in player:
        if player['urlID'] in plr_draft_yr:
            player['Draft'] = plr_draft_yr[player['urlID']]
        else:
            player_url = "https://www.basketball-reference.com/players/" + player['urlID'][0] + "/" + player['urlID'] + ".html"
            player_rest = requests.get(player_url)
            player_soup = BeautifulSoup(player_rest.content, 'lxml')
            player_info = player_soup.find(name = 'div', attrs = {'itemtype' : 'https://schema.org/Person'})
            
            # Adding name for clarity

            
            # Using RegEx to extract height, weight, and position from each player's web profile.
            # The '(.*)' regex notation allows the extraction of text from in between two known substrings,
            # which is the text written on either side of '(.*)' in the below code. 
            
            s = str(player_info.find_all('p'))
            draft = str(re.search('(pick).*(overall)', s)).split(',')[-1]
            if draft == 'None':
                player['Draft'] = 'Undrafted'
            else:
                player['Draft'] = re.search('\d+', draft).group(0)
            
            
            
            plr_draft[player['urlID']] = player['Draft']
    print(player['Draft'])


keys = players[0].keys()

with open('concat.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(players)
            # 
            # if player['urlID'] == "aldrila01":
            # 
            #     result = requests.get(player_url)
            #     tree = html.fromstring(result.content)
            #     table = tree.xpath('//table[@id="all_college_stats"]')
            #     rows = table[0].xpath('./tbody/tr')
            # 
            #     print(len(rows))
        