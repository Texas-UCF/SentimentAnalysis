import pandas as pd 
import datetime as dt 
from pandas_datareader import data, wb

get_tickers = lambda: [ticker[:-1] for ticker in open('SP500_Tickers.txt').read().split('\n')]
get_text_data = lambda: pd.read_csv('text_data.csv')

def get_data(tickers, text_data):
	df = pd.DataFrame()
	start = min(text_data['date'])
	end = max(text_data['date'])
	for ticker in tickers: 
		df = pd.append(df, wb.DataReader(ticker, 'yahoo', start, end))
	return df 

def label_data(df, day_interval):

def label_data_eod(df):


if __name__ == '__main__':
	print get_tickers()
