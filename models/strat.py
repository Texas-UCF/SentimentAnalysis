from zipline.api import order, record, symbol, get_datetime
import pandas as pd
from datetime import datetime

def initialize(context):
    context.headlines = pd.read_csv('data/headlines.csv')
    context.headlines['date'] = pd.to_datetime(context.headlines['date'])

def handle_data(context, data):
    sentiment = dict()
    now = get_datetime()
    today = datetime(now.year, now.month, now.day, 0, 0)
    print list(context.headlines['date'])[0]
    print today
    for headline in list(context.headlines[context.headlines['date'] == today]):
        print headline
