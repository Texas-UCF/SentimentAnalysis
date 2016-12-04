import pandas as pd 
from pandas_datareader import data


get_tickers = lambda: [ticker[:-1] for ticker in open('../data/SP500_Tickers.txt').read().split('\n')]
get_text_data = lambda: pd.read_csv('../data/headlines.csv')


def get_data(tickers, text_data):
	start = min(text_data['date'])
	end = max(text_data['date'])

	df = pd.DataFrame()
	for i, ticker in enumerate(tickers): 
		print i, ticker 
		try:
			stock_data = data.DataReader(ticker, 'yahoo', start, end)
			stock_data['ticker'] = ticker
			df = df.append(stock_data)
		except:
			continue
	return df 


def label_data(end_df, day_interval, threshold=0.0):
	return_calc = lambda row: (row['Close_end'] - row['Close_start']) / row['Close_start']
	
	start_df = end_df.copy()
	start_df['ind'] = start_df.index
	end_df['ind'] = start_df.index + day_interval

	join_df = start_df.merge(end_df, on=['ind', 'ticker'], suffixes=['_end','_start'])
	join_df['sentiment'] = join_df.apply(return_calc, axis=1) > threshold
	return join_df[['Date_start', 'ticker', 'sentiment']]


def label_data_eod(stock_df, threshold=0.0):
	return_calc = lambda row: (row['Close'] - row['Open']) / row['Open']
	stock_df['sentiment'] = stock_df.apply(return_calc, axis=1) > threshold
	return stock_df


if __name__ == '__main__':
	# df = get_data(get_tickers(), get_text_data())
	# df.to_csv('../data/stock_data.csv')
	df = pd.read_csv('../data/stock_data.csv')
	print label_data(df, 7)