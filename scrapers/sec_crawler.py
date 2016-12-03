import urllib2 as url 
from bs4 import BeautifulSoup
import os 
from csv import DictReader

def scraper_run(data_path):
	# Run scraper for each row in the dataset
	reader = DictReader(open(data_path, 'rb'), delimiter='\t')
	for row in reader:
		print row 
		filing_scrape(row['Quote'], row['CIK'], '10-K', row['priorto(YYYYMMDD)'], row['Count'])

def filing_scrape(company_code, cik, filing_type, priorto, count):
    # Get filing results from SEC edgar API  
    base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type="+str(filing_type)+"&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
    print company_code + ' Base: ' + base_url
    r = url.urlopen(base_url)
    edgar_result = r.read()

    # Get links to the annual reports 
    links = get_report_links(edgar_result)
    for link in links:
    	# Save the SEC filing locally 
	    download(company_code, get_filing_link(link, filing_type))


def get_report_links(edgar_doc):
	# XML parse for all report hyperlinks 
	soup = BeautifulSoup(edgar_doc, 'xml')
	filing_links = []
	for link in soup.find_all('filingHREF'):
		filing_links += [link.get_text()]
	return filing_links

def get_filing_link(report_link, filing_type):
	# html parse the report for the actual filing
	report_html = url.urlopen(report_link).read()
	soup = BeautifulSoup(report_html, 'html.parser')

	# Query the table for the relevant filing 
	# NOTE: works for 10-K, haven't tested other filing types
	table = soup.find('table', attrs={'class': 'tableFile'})
	rows = table.find_all('tr')
	for row in rows: 
		cols = row.find_all('td')
		text_cols = [ele.text for ele in cols]

		# Return the FIRST link with the document type that matches the one we're looking for 
		if len(text_cols) > 3 and unicode(filing_type) in text_cols[3]:
			return "http://www.sec.gov" + str(cols[2].find('a').get('href'))

def download(company_code, filing_link):
	print filing_link 

	# Create the company directory 
	if not os.path.exists(company_code):
		os.mkdir(company_code)

	# Use the same file name as the one on edgar
	file_name = filing_link[filing_link.rindex('/')+1:]
	file_text = url.urlopen(filing_link).read()

	# Create, write, and close out the file 
	f = open(company_code + '/' + file_name, 'w')
	f.write(file_text)
	f.close()

if __name__ == '__main__':
	# Example run 
	scraper_run('WMTdata.txt')
	