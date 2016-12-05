from zipline.api import order, record, symbol, get_datetime
import pandas as pd
from datetime import datetime
import

#TODO: What is a good threshold?
LONG_THRESH = 5
SHORT_THRESH = -5

def initialize(context):
    headlines = pd.read_csv('data/headlines.csv').sort_values('date')
    headlines['date'] = pd.to_datetime(headlines['date'])
    context.headlines = headlines
    context.long_thresh = long_thresh
    context.short_thresh = short_thresh

def handle_data(context, data):
    now = get_datetime()
    today = datetime(now.year, now.month, now.day, 0, 0)

    # Get current day's headlines
    current_headlines = []
    for i in range(0, len(context.headlines)):
        if(today == context.headlines.iloc[i]['date']):
            current_headlines.append((context.headlines.iloc[i]['ticker'], context.headlies.iloc[i]['text']

    # Calculate sentiment
    sentiment = dict()
    for headline in current_headlines:
        ticker = headline[0]
        text = headline[1]

        #TODO: Get score from classifier
        score = -1
        if ticker in sentiment.keys():
            sentiment[ticker] += score
        else:
            sentiment[ticker] = score

    # Long/Short stocks based on sentiment
    for ticker in sentiment.keys():

        #TODO: Order stocks
        if sentiment[ticker] > context.long_thresh:
            #long stocks
        else if: sentiment[ticker] < context.short_thresh:
            #short stocks
        else:
            continue
