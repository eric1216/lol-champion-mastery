from riotwatcher import LolWatcher
import config
import pandas as pd

lol_watcher = LolWatcher(config.api_key)
my_region = 'na1'
me = lol_watcher.summoner.by_name(my_region, 'ericole')

#get regions current game version
versions = lol_watcher.data_dragon.versions_for_region(my_region)
champions_version = versions['n']['champion']

#get raw champion data
raw_champion_data = lol_watcher.data_dragon.champions(champions_version)

#itterate over the raw champion data to create a list of only champion ids and champion names
champ_keys = []*2
for key, value in raw_champion_data['data'].items():
    champ_keys.append([int(value['key']), key])

#create a datafrom from champ_keys list
champion_keys = pd.DataFrame(champ_keys, columns=['championId', 'champion'])

#get champion mastery data
raw_champion_mastery = lol_watcher.champion_mastery.by_summoner(my_region, me['id'])

#create a dataframe from the raw champion mastery data
champion_mastery = pd.DataFrame(raw_champion_mastery)

#join champion_mastery and champion_keys dataframes to add champion names
final_champion_mastery = pd.merge(champion_mastery, champion_keys, how='inner')

#move champion column to the first columm, drop summonerId, sort by championPoints desc
champ_name = final_champion_mastery.pop('champion')
final_champion_mastery.insert(0, 'champion', champ_name)
final_champion_mastery = final_champion_mastery.drop(columns='summonerId')
final_champion_mastery.sort_values(by='championPoints', ascending=False)

#save dataframe to csv
final_champion_mastery.to_csv('champion_masteries.csv', index=False)

