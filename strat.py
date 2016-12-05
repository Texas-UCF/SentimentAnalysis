from zipline.api import order, record, symbol, get_datetime
import pandas as pd
from datetime import datetime
import

def initialize(context):
    headlines = pd.read_csv('data/headlines.csv').sort_values('date')
    headlines['date'] = pd.to_datetime(headlines['date'])
    context.headlines = headlines

def handle_data(context, data):
    sentiment = dict()
    now = get_datetime()
    today = datetime(now.year, now.month, now.day, 0, 0)
    current_headlines = []
    for i in range(0, len(context.headlines)):
        if(today == context.headlines.iloc[i]['date']):
            current_headlines.append((context.headlines.iloc[i]['ticker'], context.headlies.iloc[i]['text']
    for headline in current_headlines:

