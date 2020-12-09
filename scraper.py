import scraperwiki
import mechanize
import cookielib
import re
from bs4 import BeautifulSoup
from datetime import datetime, date, time
# generate random integer values
import time    
#from random import seed, randint
#import pytz


#if 1==1:

url = 'http://www.shareprices.com/ftseallshare'
  

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# sometimes the server is sensitive to this information
br.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')]

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]



#scraperwiki.sqlite.execute("drop table if exists company")  
scraperwiki.sqlite.execute("create table company (`TIDM` string, `Company` string, `Price` real, `Volume` real, `Date` date NOT NULL)")

#scraperwiki.sqlite.execute("insert into company values ('test', 'test', 'test', date('2015-12-07'), 'Y')")
scraperwiki.sqlite.execute("delete from company")
scraperwiki.sqlite.commit()



page = br.open(url)
htmlcontent = page.read()
soup = BeautifulSoup(htmlcontent, features="lxml")



test1 = re.search(r'Day\'s Volume(.*?)<br \/><\/div>', soup).group()
tuples = re.findall(r'(\">|\'>)(.*?)<\/', str(test1.replace(" ", "")).replace("><", ""))
count = 0
tidm = ""
company = ""
price = 0
poscnt = 0
for tuple in tuples:
	if poscnt == 1:
		company = tuple[1].replace("amp;", "")

	if poscnt == 2:
		price = tuple[1].replace(",", "").replace("p", "")
	if poscnt == 4:
		scraperwiki.sqlite.save(["TIDM"], data={"TIDM":tidm+'.L', "Company":company, "Price":price, "Volume":tuple[1].replace(",", ""), "Date":datetime.date.today()}, table_name='company')
		scraperwiki.sqlite.commit()
	if len(tuple[1]) <= 4 and tuple[1][-1:].isalpha() and tuple[1][-1:].isupper() and tuple[1]!=tidm and poscnt!=1:
		count = count+1

		tidm = tuple[1]
		poscnt = 1
	else:
		poscnt = poscnt + 1    
		
		
	print(count)
		#print re.search('', (.*?)', match).group()
