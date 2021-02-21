import pandas as pd
import tweepy
from datetime import datetime

# Twitter authorisation - you need to fill in your own API details (https://dev.twitter.com)
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("access_token", "access_token_secret")
api = tweepy.API(auth)

# How many blocks you want in progress bar, 15 works well with Twitter ▓▓▓▓▓░░░░░░░░░░
bar_total = 15
perc_per_bar = 100/bar_total

# This sets date
from datetime import date, timedelta
date_to_check = (date.today()).isoformat()

# GOV UK data source API:
data_read = pd.read_csv(
    'https://health-infobase.canada.ca/src/data/covidLive/vaccination-coverage-map.csv', delimiter=',')

def AddDataToTweet(dataValue, textValue):
    dataToAdd = ''
    total_vacs = data_read.loc[ (data_read['prename'] == 'Canada') & (data_read.week_end == date_to_check), dataValue].values[0]
    #.astype(float).round(2)
    perc_rounded = round( (float(total_vacs)),2)

    solid_bars_to_print = perc_rounded // perc_per_bar
    empty_bars_to_print = bar_total - solid_bars_to_print

    dataToAdd += textValue
    while solid_bars_to_print > 0:
        dataToAdd += '▓'
        solid_bars_to_print -=1

    while empty_bars_to_print > 0:
        dataToAdd += '░'
        empty_bars_to_print -= 1

    dataToAdd += ' ' + str(perc_rounded) + '%\n\n'
    return dataToAdd


def SourceAndSendTweet(stringToTweet):
    stringToTweet += 'As of '+str(date_to_check)+'\n'
    stringToTweet += 'Using data from Gov of Canada API\n'
    stringToTweet += '#CovidVaccine'
    print(stringToTweet)
    api.update_status(stringToTweet)


stringToTweet = ''
stringToTweet += AddDataToTweet('proptotal_1dose','1st dose of vaccine progress: \n\n')
stringToTweet += AddDataToTweet('proptotal_2doses','2nd dose of vaccine progress: \n\n')
SourceAndSendTweet(stringToTweet)

