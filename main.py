from riotwatcher import LolWatcher
import config
import pandas as pd

lol_watcher = LolWatcher(config.api_key)
my_region = 'na1'
me = lol_watcher.summoner.by_name(my_region, 'ericole')

#get regions current game version
versions = lol_watcher.data_dragon.versions_for_region(my_region)
champions_version = versions['n']['champion']

#get champions
current_champ_list = lol_watcher.data_dragon.champions(champions_version)

#create a dataframe with champion names and their unique identifier
champ_keys = []*2
for key, value in current_champ_list['data'].items():
    champ_keys.append([int(value['key']), key])

champion_keys = pd.DataFrame(champ_keys, columns=['championId', 'champion'])

#get champion mastery data
champ_mastery_raw = lol_watcher.champion_mastery.by_summoner(my_region, me['id'])

#create a dataframe with champion mastery data
champion_mastery = pd.DataFrame(champ_mastery_raw)

#join champion_mastery and champion_keys dataframes to add champion names
summoner_champion_mastery = pd.merge(champion_mastery, champion_keys, how='inner')

#move champion names to the first columm, drop summonerId, sort by championPoints desc
champ_name = summoner_champion_mastery.pop('champion')
summoner_champion_mastery.insert(0, 'champion', champ_name)
summoner_champion_mastery = summoner_champion_mastery.drop(columns='summonerId')
summoner_champion_mastery.sort_values(by='championPoints', ascending=False)

#output dataframe to csv
summoner_champion_mastery.to_csv('champion_masteries.csv', index=False)

