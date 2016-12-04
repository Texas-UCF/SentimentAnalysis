import urllib2 as url
from bs4 import BeautifulSoup
import os
from csv import DictReader
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import re
import datetime as dt

stop = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
reports_to_df = lambda reports: pd.DataFrame(reports)

def scraper_run(data_path):
    # Run scraper for each row in the dataset
    reader = DictReader(open(data_path, 'rb'), delimiter='\t')
    data = []
    for row in reader:
        data += filing_scrape(row['Quote'], row['CIK'], '10-K', row['priorto(YYYYMMDD)'], row['Count'])
    df = data_to_df(data)
    df.to_csv('../data/sec_filings.csv', index=False)

def clean_sentence(sentence):
	sentence = re.sub(r'[^a-zA-Z\-\' ]', '', sentence)
	return ' '.join([word.lower() for word in re.split('\W+', sentence) if word not in stop and len(word) > 1])

def filing_scrape(ticker, cik, filing_type, priorto, count):
    # Get filing results from SEC edgar API
    base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type="+str(filing_type)+"&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
    #print(company_code + ' Base: ' + base_url)
    r = url.urlopen(base_url)
    edgar_result = r.read()

    filings = []
    # Get links to the annual reports
    links = get_report_links(edgar_result)
    for link in links:
        filings.append(get_filing_link(ticker, link, filing_type))
    return filings

def get_report_links(edgar_doc):
    # XML parse for all report hyperlinks
    soup = BeautifulSoup(edgar_doc, 'xml')
    filing_links = []
    for link in soup.find_all('filingHREF'):
        filing_links += [link.get_text()]
    return filing_links


def get_filing_link(ticker, report_link, filing_type):
    filing = dict()
    filing['ticker'] = ticker

    # html parse the report for the actual filing
    report_html = url.urlopen(report_link).read()
    soup = BeautifulSoup(report_html, 'html.parser')

    # parse the filing date
    date = soup.select("body .formGrouping .info")[0].get_text()
    year, month, day = tuple(date.split('-'))
    filing['date'] = dt.datetime(int(year), int(month), int(day))
    #print(soup.select("body .formGrouping .info")[0].get_text())

    # Query the table for the relevant filing
    # NOTE: works for 10-K, haven't tested other filing types
    table = soup.find('table', attrs={'class': 'tableFile'})
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        text_cols = [ele.text for ele in cols]

        # Return the FIRST link with the document type that matches the one we're looking for
        if len(text_cols) > 3 and unicode(filing_type) in text_cols[3]:
            filing_link = "http://www.sec.gov" + str(cols[2].find('a').get('href'))
            filing['text'] = clean_sentence(download(ticker, filing_link, 'sec_filings/'))
            return filing

def download(ticker, filing_link, root_dir):
    print(filing_link)

    # Create directory for all filings
    if not os.path.exists('sec_filings'):
            os.mkdir('sec_filings')

    # Create the company directory
    if not os.path.exists(root_dir + ticker):
        os.mkdir(root_dir + ticker)

    # Use the same file name as the one on edgar
    file_name = filing_link[filing_link.rindex('/')+1:]
    file_text = url.urlopen(filing_link).read()
    soup = BeautifulSoup(file_text, 'html.parser')
    data = clean_sentence(" ".join(soup.stripped_strings))

    # Create, write, and close out the file
    f = open(root_dir + ticker + '/' + file_name, 'w')
    f.write(data)
    f.close()

    return data

if __name__ == '__main__':
    # Example run
    scraper_run('../data/WMTdata.txt')
