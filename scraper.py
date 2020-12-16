import scraperwiki
import mechanize
import cookielib
import re
from bs4 import BeautifulSoup
from datetime import datetime, date, time
# generate random integer values
import time    
#from random import seed, randint
import pytz


au_tz = pytz.timezone('Australia/Perth')

if 1==1:

    urllist = ["https://shareprices.com/indices/ftse100"]
    for url in urllist:
    
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
            # sometimes the server is sensitive to this information
        br.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')]



        scraperwiki.sqlite.execute("drop table if exists company")  
        scraperwiki.sqlite.execute("create table company (`Code` string NOT NULL, `Company` string, `Price` real, `Change` real, `Perc_Change` real,  `Days_Volume` integer, `EOD_Date` string NOT NULL, UNIQUE (`Code`, `EOD_Date`))")
        #scraperwiki.sqlite.execute("delete from company")  


        page = br.open(url)
        htmlcontent = page.read()
        soup = BeautifulSoup(htmlcontent, features="lxml")


        #eoddate = soup.findAll("div", {"class": "header-timestamp"})[0].text[-11:].replace(" ", "-")
        #date_obj = datetime.strptime(eoddate, '%d-%b-%Y')
        
        eoddate = datetime.now(tz=au_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        #eoddateint = int(date_obj.strftime('%Y%m%d'))

        table = soup.find( "table", {"id":"indices__constituents-table sortable"} )
        
        print table

        output_rows = []
        for table_row in table.findAll('tr'):
            columns = table_row.findAll('td')
            output_row = []
            for column in columns:
                output_row.append(column.text + ",")
            output_rows.append(output_row)


        for sublst in output_rows:
            if len(sublst) > 0:
                #rank = sublst[0].replace(",", "")
                tidm = sublst[0].replace(",", "") 
                company = sublst[1].replace(",", "") 
                price = sublst[2].replace(",", "").replace("$", "") 
                change = sublst[3].replace(",", "").replace("+", "")    
                perchg = round(float(sublst[4].replace(",", "").replace("+", "").replace("%", "").strip('"'))/100.0, 4)
                daysvolume = sublst[5].replace(",", "")              
                
                #yrperchg = round(float(sublst[8].replace(",", "").replace("+", "").replace("%", "").strip('"'))/100.0, 4)                                                                                                 
                #marketcap = sublst[7].replace(",", "").replace("$", "").replace(".", "").replace(" B", "0000000").replace(" M", "0000").replace(" TH", "0")    

                scraperwiki.sqlite.execute("insert or ignore into company values (?, ?, ?, ?, ?, ?, ?, ?, ?)",  [tidm, company, price, change, perchg, daysvolume, eoddate]) 

    
        scraperwiki.sqlite.commit() 
    
    #scraperwiki.sqlite.execute("drop table if exists Company_List") 
    #scraperwiki.sqlite.execute("create table Company_List (`Code` varchar2(8) NOT NULL, `Company` varchar2(100) NOT NULL, `Date_Added` date NOT NULL, UNIQUE (`Code`))")  
    #scraperwiki.sqlite.execute("insert or ignore into Company_List SELECT DISTINCT code, company, ? from company where rank <= 300", [eoddate])


    #scraperwiki.sqlite.commit()  

