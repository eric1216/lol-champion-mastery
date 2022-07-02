from riotwatcher import LolWatcher
import pandas as pd
import config

lol_watcher = LolWatcher(config.api_key)
my_region = 'na1'
me = lol_watcher.summoner.by_name(my_region, 'ericole')

versions = lol_watcher.data_dragon.versions_for_region(my_region)
champions_version = versions['n']['champion']

# create dataframe for champions key and name only
raw_champion_data = lol_watcher.data_dragon.champions(champions_version)

champion_keys_list = []*2
for key, value in raw_champion_data['data'].items():
    champion_keys_list.append([int(value['key']), key])

champion_keys = pd.DataFrame(champion_keys_list, columns=['championId', 'champion'])

# create dataframe for champion mastery data 
raw_mastery_data = lol_watcher.champion_mastery.by_summoner(my_region, me['id'])

champion_mastery = pd.DataFrame(raw_mastery_data)

# join dataframes, rearrange columns, drop "summonerID", sort by "championPoints"
final_champion_mastery = pd.merge(champion_mastery, champion_keys, how='inner')

champ_name = final_champion_mastery.pop('champion')
final_champion_mastery.insert(0, 'champion', champ_name)

final_champion_mastery = final_champion_mastery.drop(columns='summonerId')

final_champion_mastery.sort_values(by='championPoints', ascending=False)

# export final dataframe to csv
final_champion_mastery.to_csv('champion_masteries.csv', index=False)
