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
	join_df = join_df[['Date_start', 'ticker', 'sentiment']]
	join_df.columns = ['date', 'ticker', 'sentiment']
	return join_df


def label_data_eod(stock_df, threshold=0.0):
	return_calc = lambda row: (row['Close'] - row['Open']) / row['Open']
	stock_df['sentiment'] = stock_df.apply(return_calc, axis=1) > threshold
	stock_df = stock_df[['Date','ticker','sentiment']]
	stock_df.columns = ['date', 'ticker', 'sentiment']
	return stock_df


def join_to_text(text_df, label_df):
	text_df['date'] = pd.to_datetime(text_df['date'])
	label_df['date'] = pd.to_datetime(label_df['date'])
	return text_df.merge(label_df, on=['date', 'ticker'])


if __name__ == '__main__':
	# df = get_data(get_tickers(), get_text_data())
	# df.to_csv('../data/stock_data.csv')
	df = pd.read_csv('../data/stock_data.csv')
	text_df = get_text_data()
	label_df = label_data_eod(df)
	labeled_text = join_to_text(text_df, label_df)
	labeled_text.to_csv('../data/text_sentiment.csv')