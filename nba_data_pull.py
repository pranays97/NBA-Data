import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

###THIS CODE SCRAPES THE BASKETBALL REFERENCE WEBSITE TO GET THE MOST COMPREHENSIVE LIST OF ALL BASKETBALL PLAYERS - CURRENT AND HISTORIC - ALONG WITH THEIR PLAYER IDs

letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
#letter_list = ['a','b']
player_df = pd.DataFrame(columns=['player_id','player_name','min_year','max_year']) #empty dataframe to store the player IDs, player names, their min_year, max_year

#loop goes through the letters in the letter list (all of them except for x) and uses beautiful soup and requests to get the html file
#then we use regex to source the actual player ID and player name from that html file and store it in the empty dataframe

for letter in letter_list:

    url_string = "https://www.basketball-reference.com/players/" + letter + "/"
    r = requests.get(url_string)

    soup = bs(r.content, features = "html.parser")
    player_list = soup.find_all("th",attrs={"scope":"row"})
    min_year_list = soup.find_all("td",attrs={"data-stat":"year_min"})
    max_year_list = soup.find_all("td", attrs={"data-stat":"year_max"})

    player_id_list = []
    player_name_list = []
    player_min_list = []
    player_max_list = []
    for player in player_list:
        player_id_re =  re.search('csv="(.+?)" data',str(player))
        player_id = player_id_re.group(1)
        player_name_re = re.search('html">(.+?)</a', str(player))
        player_name = player_name_re.group(1)

        player_id_list.append(player_id)
        player_name_list.append(player_name)
        

    for minyear in min_year_list:
        minyear_re = re.search('min">(.+?)</',str(minyear))
        min_year = minyear_re.group(1)
        print(min_year)
        player_min_list.append(int(str(min_year)))

    for maxyear in max_year_list:
        maxyear_re = re.search('max">(.+?)</',str(maxyear))
        max_year = maxyear_re.group(1)
        player_max_list.append(max_year)

    temp_df = pd.DataFrame({'player_id':player_id_list,'player_name':player_name_list,'min_year':player_min_list,'max_year':player_max_list})
    player_df = pd.concat([player_df,temp_df])

print(player_min_list)
#player_df['min_year'] = player_df['min_year'].astype('str').astype('int64')

print(player_df)


