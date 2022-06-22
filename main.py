from riotwatcher import LolWatcher
import config

lol_watcher = LolWatcher(config.api_key)
my_region = 'na1'
me = lol_watcher.summoner.by_name(my_region, 'ericole')

my_mastery = lol_watcher.champion_mastery.by_summoner(my_region, me['id'])
print(my_mastery)