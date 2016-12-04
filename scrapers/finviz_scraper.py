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
get_tickers = lambda: [ticker[:-1] for ticker in open('../data/SP500_Tickers.txt').read().split('\n')]
headlines_to_df = lambda headline_data: pd.DataFrame(headline_data)


def clean_sentence(sentence):
	sentence = re.sub(r'\[(.*?)\]', '', sentence)
	sentence = re.sub(r'[^A-Za-z ]', ' ', sentence)
	return ' '.join([lemmatizer.lemmatize(word.lower()) 
		for word in re.split('\W+', sentence) 
		if word not in stop and len(word) > 1])


def parse_headlines(tickers, clean=True):
	headline_data = []
	for i, ticker in enumerate(tickers):
		try:
			print i, ticker
			html = url.urlopen(base_url + ticker).read()
			soup = BeautifulSoup(html, 'xml')
			table = soup.find('table', attrs={'id': 'news-table'})
			rows = table.find_all('tr')
			headline_data += parse_rows(rows, ticker)
		except:
			continue
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
		headline_row['date'] = dt.datetime(2000 + int(year), month_abbrs[mon], int(day))

		# Get Headline and Ticker
		headline_row['text'] = cols[1].find('a').text
		headline_row['ticker'] = ticker

		headline_data.append(headline_row)

	return headline_data


def clean_headlines(headline_data):
	for headline_row in headline_data:
		headline_row['text'] = clean_sentence(headline_row['text'])


if __name__ == '__main__':
	tickers = get_tickers()
	df = headlines_to_df(parse_headlines(tickers))
	df.to_csv('../data/headlines.csv', index=False)
