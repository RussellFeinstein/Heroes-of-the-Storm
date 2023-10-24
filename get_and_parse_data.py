"""
Russell Feinstein
Class: CS 677
Date: Wednesday, April 27, 2022
Final Project
Retrieves match data from Blizzard's Heroes of the Storm via
www.heroesprofile.com and organizes that data into a usable format
for our purposes in this project.
"""
import json

import pandas as pd
import numpy as np
import requests

def main():
  with open('master_matches.json', 'r') as file:
    masters = json.load(file)

  # Get replay IDs  
  replayIDs = []
  for x in masters:
    replayIDs.append(x['replayID'])

  # Create empty dataframe with each hero as a column
  hero_data = pd.read_csv('Heroes.csv', sep=';', encoding='cp1252')

  hero_names = hero_data.loc[:,'name'].tolist()
  for name in hero_names:
    print(name)

  df = pd.DataFrame(columns=hero_names)
  df['winner'] = np.NaN
  
  for ID in replayIDs:
    call = 'https://api.heroesprofile.com/api/Replay/Data?replayID='+str(ID)+'&api_token=dyyQsaSg4h8mBpHRvwZgbVWLex8F3ax6BwqoIa5NyRIhh39PXxvatmMosMEJ'
    response = requests.get(call)
    
    replay = response.json()


    match_heroes = {key: 0 for key in hero_names}
    for x in replay:
      for y in replay[x]:
        if not (  y == 'game_type'
          or y == 'game_date'
          or y == 'game_length'
          or y == 'game_map'
          or y == 'game_version'
          or y == 'region'
          or y == 'experience_breakdown'
        ):
          tmp = replay[x][y]
          match_heroes[tmp['hero']] = [tmp['team'] + 1]
          if 'winner' not in match_heroes:
            if tmp['winner'] == True:
              if tmp['team'] == 0:
                match_heroes['winner'] = [0]
              else:
                match_heroes['winner'] = [1]

    df2 = pd.DataFrame(match_heroes)
    df = pd.concat([df, df2], ignore_index=True)
    df.reset_index

  df.to_csv('match_history.csv', index=False)



  

if __name__ == '__main__':
  main()