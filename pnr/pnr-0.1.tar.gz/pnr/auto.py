import requests
import sys
from BeautifulSoup import BeautifulSoup

num = sys.argv[1]
def main():
	data = {'lccp_pnrno1':num}
	a=requests.post('http://www.trainspnrstatus.com/pnrformcheck.php',data=data)
	content=a.text
	soup=BeautifulSoup(content)
	table = soup.findAll("table", {"class":"table table-striped table-bordered"})
	for rows in table:
		cols = rows.findAll("b")
		if len(cols)>1:
			if cols[2].text=="CNF":
				print "Current Status\0" + cols[2].text
				print "Booking Status\0" + cols[1].text.replace(" ", "")
			else:
				print "Current Status \0" + cols[2].text