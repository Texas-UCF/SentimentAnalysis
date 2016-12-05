from zipline.api import order, record, symbol, get_datetime
import pandas as pd
from datetime import datetime

def initialize(context):
    headlines = pd.read_csv('data/headlines.csv').sort_values('date')
    headlines['date'] = pd.to_datetime(headlines['date'])
    context.headlines = headlines

def handle_data(context, data):
    sentiment = dict()
    print list(context.headlines['date'])[0]
    now = get_datetime()
    today = datetime(now.year, now.month, now.day, 0, 0)
    print today
    for headline in list(context.headlines[context.headlines['date'] == today]):
        print headline
