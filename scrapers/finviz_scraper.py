import pandas as pd 
import urllib2 as url
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import re
import calendar
import datetime as dt

month_abbrs = {abbr:month_num for month_num, abbr in enumerate(calendar.month_abbr)}
stop = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

base_url = "http://finviz.com/quote.ashx?t="
get_tickers = lambda: [ticker[:-1] for ticker in open('../SP500_Tickers.txt').read().split('\n')]
headlines_to_df = lambda headline_data: pd.DataFrame(headline_data)


def clean_sentence(sentence):
	sentence = re.sub(r'\[(.*?)\]', '', sentence)
	return ' '.join([word.lower() for word in re.split('\W+', sentence) if word not in stop and len(word) > 0])


def parse_headlines(tickers, clean=True):
	headline_data = []
	for i, ticker in enumerate(tickers):
		print i, ticker
		html = url.urlopen(base_url + ticker).read()
		soup = BeautifulSoup(html, 'xml')
		table = soup.find('table', attrs={'id': 'news-table'})
		rows = table.find_all('tr')
		headline_data += parse_rows(rows, ticker)
	if clean: clean_headlines(headline_data)
	return headline_data


def parse_rows(rows, ticker):
	mon, day, year = None, None, None
	headline_data = []
	for row in rows:
		headline_row = dict()
		cols = row.find_all('td')
		
		# Get Date
		ts = cols[0].text.split()
		if len(ts) == 2: mon, day, year = tuple(ts[0].split('-'))
		headline_row['date'] = dt.datetime(int(year), month_abbrs[mon], int(day))

		# Get Headline and Ticker
		headline_row['text'] = cols[1].find('a').text 
		headline_row['ticker'] = ticker

		headline_data.append(headline_row)

	return headline_data


def clean_headlines(headline_data):
	for headline_row in headline_data: 
		headline_row['text'] = clean_sentence(headline_row['text']) 


if __name__ == '__main__':
	tickers = get_tickers()[:4]
	df = headlines_to_df(parse_headlines(tickers))
	df.to_csv('../headlines.csv', index=False)
