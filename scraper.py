import scraperwiki
import mechanize
import re
import csv
import time
from datetime import datetime, date
import datetime
#import sqlite3


#scraperwiki.sqlite.execute("create table Company_Performance (`TIDM` varchar2(8) NOT NULL, `1D` real, `3D` real, `1W` real, '1M' real, '6M' real,  `Date` date, UNIQUE (`TIDM`, `Date`))")
#if 1==1:
 
 #    complist = scraperwiki.sqlite.execute("select `TIDM`, `Price` from Signal_History")

#Tmp1=0.0
        
  #   for x in complist["data"]:
   #      tidm=x[0]
    #     price = x[1].replace(",", "")
         
     #    scraperwiki.sqlite.execute("update Signal_History set `Price` = %f where tidm = '%s' and Date = '%s'" % (tidm, tdate))

if 1==1: 
 
   complist = scraperwiki.sqlite.execute("select `TIDM`, `Price`, `Date` from company where TIDM in (select distinct TIDM from Signal_History)")
   #complist = scraperwiki.sqlite.execute("select `TIDM`, `Price`, `Date` from company where tidm = 'SIG.L'")
   #complist = scraperwiki.sqlite.execute("select `TIDM`, `Price`, `Date` from company")

#Tmp1=0.0
        
   for x in complist["data"]:
       #Tmp1=tmp1+x[1]
       #tidm=x[0]
       tidm=x[0]
       print(tidm)
       nprice=x[1]
       tdate=datetime.datetime.strptime(x[2], "%Y-%m-%d").date()
      # ndate=dt.datetime.today().strftime("%Y/%m/%d")
       todaydate=datetime.date.today()
       #ndate=datetime.datetime(ndate.year, ndate.month, ndate.day)
       
       Commission=0.994

# Find Today GDP100

       ldata = scraperwiki.sqlite.execute("select `Price` from Signal_History where tidm = '%s' and Date = '%s'" % (tidm, tdate))
       if len(ldata["data"]) != 0:
           for c in d1mindate["data"]:
               tprice = c[0]
           
       else:
        
           ldata = scraperwiki.sqlite.execute("select `Date`, `GBP 100`, `Price`, `Signal` from Signal_History where tidm = '%s' and Date in (select max(`Date`) from Signal_History where tidm = '%s')" % (tidm, tidm))
           if len(ldata["data"]) == 0:
               tprice = 0
    
           else: 
               for b in ldata["data"]:
                   #LatestDate = datetime.datetime.strptime(b[0], "%Y-%m-%d").date()
                   LatestGDP100 = b[1]
                   LatestPrice = b[2]
                   LatestSignal = b[3]
       
                   #print nprice
                   #print 'LatestPrice %s' % (LatestPrice) 
                   ldiff = (nprice - LatestPrice) / LatestPrice
           
                   if LatestSignal == 'BUY':
                       tprice = (LatestGDP100 + (LatestGDP100*ldiff))*Commission
                       #print 'nprice %f' % (nprice)
                       #print 'LatestPrice %f' % (LatestPrice)
                       #print 'LatestGDP100 %f' % (LatestGDP100)
                       #print 'ldiff %f' % (ldiff)
                       #print 'Commission %f' % (Commission)
                   elif LatestSignal == 'SHORT':
                       tprice = (LatestGDP100 + (LatestGDP100*(ldiff*-1)))*Commission
                   #SELL etc
                   else:
                       tprice = LatestGDP100*.994
               #print 'Current Calc GDP 100:'
               #print tdate
               print("Latest: %s: $%s" % (tdate, round(tprice,2)))
               #print tprice
               #print "Latest Date %s" % (tdate)
#------------------------------------------------------------

#D-1   


       d1date=todaydate - datetime.timedelta(days=10)
       #d1list = scraperwiki.sqlite.execute("select `Price` from Signal_History where tidm = '" + tidm + "' and strftime('%Y', date) = '" + str(d1date.year) + "' and	strftime('%-m', date) = '" + str(d1date.month) + "' and	strftime('%-d', date) = '" + str(d1date.day) + "'")
       #d1list = scraperwiki.sqlite.execute("select `TIDM`, `Price`, `Date` from Signal_History where tidm = '" + tidm + "' and CAST(strftime('%m', Datde) AS INTEGER) > 1")
       #d1list = scraperwiki.sqlite.execute("select `TIDM`, `Price`, `Date` from Signal_History where tidm = '" + tidm + "' and strftime('%Y-%m-%d',Date) = '2016-02-15'")
       #d1list = scraperwiki.sqlite.execute("select `TIDM`, `Price`, `Date` from Signal_History where tidm = '" + tidm + "' and strftime('%%Y',date,'unixepoch') = '%s'"%(str(d1date.year)))
       #d1list = scraperwiki.sqlite.execute("select `TIDM`, `Price`, `Date` from Signal_History where tidm = '" + tidm + "' and substr(Date, 1, 2) = '%s' and substr(Date, 4, 2) = '%s' and substr(Date, 7, 4) = '%s'" % (d1date.strftime('%d'), d1date.strftime('%m'), d1date.strftime('%Y')))
       
       d1list = scraperwiki.sqlite.execute("select `GBP 100` from Signal_History where tidm = '%s' and Date = '%s'" % (tidm, d1date))
       
       if len(d1list["data"]) != 0:
           for a in d1list["data"]: 
               #MatchDate = a[0]
               CalcPrice = a[0]
               #print MatchDate
               #print MatchPrice 
       else:        
           #d1maxdate = scraperwiki.sqlite.execute("select max(`Date`) from Signal_History where tidm = '%s' and Date < '%s'" % (tidm, d1date))
           d1mindate = scraperwiki.sqlite.execute("select `Date`, `GBP 100` from Signal_History where tidm = '%s' and Date in (select max(`Date`) from Signal_History where tidm = '%s' and Date < '%s')" % (tidm, tidm, d1date))
           
           if len(d1mindate["data"]) == 0:
               MinDate = '1900-01-01' #datetime.datetime.strptime(y[0], "%Y-%m-%d").date()
               MinPrice = 0.0
           else: 
               for y in d1mindate["data"]:
                    MinDate = datetime.datetime.strptime(y[0], "%Y-%m-%d").date()
                    MinPrice = y[1]
           
               d1maxdate = scraperwiki.sqlite.execute("select `Date`, `GBP 100` from Signal_History where tidm = '%s' and Date in (select min(`Date`) from Signal_History where tidm = '%s' and Date > '%s')" % (tidm, tidm, d1date))
               
               if len(d1maxdate["data"]) == 0:
                   MaxDate=tdate
                   MaxPrice=tprice
               else:
                   for z in d1maxdate["data"]:
                        MaxDate = datetime.datetime.strptime(z[0], "%Y-%m-%d").date()
                        MaxPrice = z[1]
           #print MinDate
           #print MinPrice
           #print MaxDate
           #print MaxPrice
           #delta = Date(MaxDate) - Date(MinDate)
           #print d1date
           Abovedelta = MaxDate - d1date
           Belowdelta = d1date - MinDate
           
           MinMaxDelta = MaxDate - MinDate
           PriceDelta = MaxPrice - MinPrice
           if PriceDelta == 0:
               PriceInterval=0
           else:
               PriceInterval = PriceDelta / MinMaxDelta.days
           
           if abs(Abovedelta.days) >= Belowdelta.days:
               #print "below"
               CalcPrice = MinPrice+Belowdelta.days*PriceInterval
           else:
               #print "above"
               CalcPrice = MaxPrice-Abovedelta.days*PriceInterval
               
       D1PC = (tprice - CalcPrice) / CalcPrice
           
           #print "mindate %s" % (MinDate)
           #print "MaxDate %s" % (MaxDate)
           #print "MinPrice %f" % (MinPrice)
           #print "PriceInterval %f" % (PriceInterval)
           #print "Belowdelta %f" % (Belowdelta.days)
           #print "CalcPrice %f" % (CalcPrice)
           #print tprice
       print("Latest - 10: %s: $%s %s" % (d1date, round(CalcPrice,2), round(D1PC*100,1)))
       print(" ")
           #print "d1date %s" % (d1date)
           #print "D1PC %f" % (D1PC) 
           #print 'Delta: %d' % (delta.days)


                
           #    print MinDate
           #print "Value : %s" %  d1maxdate.keys()
           #print str(d1maxdate["data"])
           #print "Value : %s" %  d1maxdate.get('data')

           #for y in d1maxdate["data"]:
               #print y[0]
       #break
       #d1list = scraperwiki.sqlite.execute("select `TIDM`, `Price`, `Date` from Signal_History where tidm = '" + tidm + "' and Date = '%d'" % (d1date))
       #print  "%s-%s-%s" % (d1date.strftime('%Y'), d1date.strftime('%m'), d1date.strftime('%d'))
       #print " "
       #d1list = scraperwiki.sqlite.execute("select `TIDM`, `Date`, strftime('%m',Date,'unixepoch') from Signal_History where tidm = '" + tidm + "' and Date > '%s-%s-%s'" % (d1date.strftime('%Y'), d1date.strftime('%m'), d1date.strftime('%d')))
       #d1list = scraperwiki.sqlite.execute("select `TIDM`, `Date`, strftime('%%m',Date) from Signal_History where tidm = '%s' and Date > '%s'" % (tidm, d1date))
       
       #d1list = scraperwiki.sqlite.execute("select `TIDM`, `Date`, strftime('%m',SH.Date) from Signal_History as SH where tidm = '" + tidm + "' and SH.Date > '2015-01-15'") # '%s-%s-%s' group by `TIDM`" % (d1date.year, d1date.month, d1date.day))
       #for y in d1list["data"]:
       #    print y[0]
       #    print y[1]
       #    print y[2]
       #break   
       
       
if 1==0:
     tidm = "test"
     ndate=datetime.date.today()
     datetime.date.today()
     d1date=ndate - datetime.timedelta(days=10)
     print(d1date)
     print("select `TIDM`, strftime('%m',Date,'unixepoch') from Signal_History where tidm = '" + tidm + "' and Date < '%s-%s-%s'" % (d1date.strftime('%Y'), d1date.strftime('%m'), d1date.strftime('%d')))
     #ndate=datetime.date.today()
     #print ndate.year
     #strftime('%Y', ndate)
#------------------------------------------------
#------------------------------------------------

if 1==0:

    url = 'http://www.shareprices.com/ftseallshare'
    
    
        #print str(asxlist["data"][x])[3:-2]
    
    #for x in asxlist:
    #    print asxlist
    
    #data = scraperwiki.scrape("http://www.asx.com.au/asx/research/ASXListedCompanies.csv")
    #url2 = 'https://www.aussiebulls.com/SignalPage.aspx?lang=en&Ticker=WOW.AX'
    br = mechanize.Browser()
    
        # sometimes the server is sensitive to this information
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    #####reader = csv.DictReader(data.splitlines()[2:10])
    
    #scraperwiki.sqlite.execute("alter table companies add `Date Added` date")
    #scraperwiki.sqlite.execute("alter table companies rename to company")
    #scraperwiki.sqlite.execute("alter table company rename column `Date Added` to `Last Refreshed`")
    #scraperwiki.sqlite.execute("alter table company add `Top 500` char(1)")
    
    #scraperwiki.sqlite.execute("drop table if exists company")  
    #scraperwiki.sqlite.execute("create table company (`TIDM` string, `Company` string, `Price` real, `Volume` real, `Date` date NOT NULL)")
    #scraperwiki.sqlite.execute("drop table if exists Signal_History")  
    #scraperwiki.sqlite.execute("create table Signal_History (`ASX code` varchar2(8) NOT NULL, `Date` date NOT NULL, `Price` real NOT NULL, `Signal` varchar2(15) NOT NULL, `Confirmation` char(1) NOT NULL, `AUD 100` real NOT NULL, UNIQUE (`ASX code`, `Date`))")
    
    #scraperwiki.sqlite.execute("insert into company values ('test', 'test', 'test', date('2015-12-07'), 'Y')")
    scraperwiki.sqlite.execute("delete from company")
    scraperwiki.sqlite.commit()
    
    #@@@scraperwiki.sqlite.save(['GICS industry group', 'ASX code', 'Company name'], list(csv.DictReader(scraperwiki.scrape('http://www.asx.com.au/asx/research/ASXListedCompanies.csv').splitlines()[2:])), table_name='company')
    #scraperwiki.sqlite.save(['industry', 'code', 'company'], list(csv.DictReader(scraperwiki.scrape('http://www.asx.com.au/asx/research/ASXListedCompanies.csv').splitlines()[2:10])), table_name="companies")
    
    #@@@scraperwiki.sqlite.execute("update company set `Last Refreshed` = date('now') where `Last Refreshed` is null")
    
    #@@@scraperwiki.sqlite.execute("update company set `Top 500` = 'Y' where `Last Refreshed` = date('now')")
    #@@@scraperwiki.sqlite.execute("update company set `Top 500` = 'N' where `Last Refreshed` <> date('now')")
    
    
    #scraperwiki.sqlite.commit()
    #scraperwiki.sqlite.execute(".schema companies")
    #scraperwiki.sqlite.execute("select * from company") 
    
    #####for record in reader:
    #####        print record
    
    response = br.open(url)
    
    
    for pagenum in range(1):
        html = response.read()
        #print html
    #comp = re.search(r'MainContent_CompanyTicker(\w{3,}\.AX)span', html).group(0)
    #ASX_Code = '3PL.AX'
      
    #print re.findall(r'MainContent_signalpagehistory_PatternHistory24((.)+)\<\\table\>', html) 
        #test1 = re.findall(r'Day\'s Volume(.*)>(.*)<(.*)endcol', html)
        #test1 = re.findall('(Day\'s Volume)(.*?)>(.*?)<(.*?)(endcol)', html)
        test1 = re.search(r'Day\'s Volume(.*?)<br \/><\/div>', html).group()
        #for match in re.findall(r'(\">|\'>)(.*?)<\/', str(test1.replace(" ", "")).replace("><", "")):
        tuples = re.findall(r'(\">|\'>)(.*?)<\/', str(test1.replace(" ", "")).replace("><", ""))
        count = 0
        tidm = ""
        company = ""
        price = 0
        poscnt = 0
        for tuple in tuples:
            if poscnt == 1:
                #scraperwiki.sqlite.save(["TIDM"], data={"TIDM":tidm, "Company":tuple[1].replace("amp;", "")}, table_name='company')
                company = tuple[1].replace("amp;", "")
                #scraperwiki.sqlite.commit()
            if poscnt == 2:
                price = tuple[1].replace(",", "").replace("p", "")
            if poscnt == 4:
                scraperwiki.sqlite.save(["TIDM"], data={"TIDM":tidm+'.L', "Company":company, "Price":price, "Volume":tuple[1].replace(",", ""), "Date":datetime.date.today()}, table_name='company')
                scraperwiki.sqlite.commit()
            if len(tuple[1]) <= 4 and tuple[1][-1:].isalpha() and tuple[1][-1:].isupper() and tuple[1]!=tidm and poscnt!=1:
                count = count+1
                #print tuple[1]
                #scraperwiki.sqlite.save(["TIDM"], data={"TIDM":tuple[1]}, table_name='company')
                tidm = tuple[1]
                poscnt = 1
            else:
                poscnt = poscnt + 1    
            
            
        print(count)
            #print re.search('', (.*?)', match).group()
            #print re.search(r'(\">|\'>)(.*?)', match).group(1)
            #print re.search(r'', (\.*\?)', match)
           # ("'>", 'III') 
    # ('">', '3iGroup')
            
        #test3 = re.findall(r'>(.*)<', test2)
        #print test3
    
     #       if test1:
       #         test1 = test1.group(0)
        
    
    # test2 = re.findall(r'(\"\>|img\/)((.)+)\<\/td\>\<td', test1)
    #test2 = re.findall('\">(.*)<\/', test1)
    #test2 = re.findall('\">(.*?)<\/', test1)
    #test2 re.search(r'\"\>(.*)\<\/?', test1)
    #test2 = re.findall('\">(.*?)<\/', test1) GOOD
    #test2 = re.findall('(\">|img\/)(.*?)(<\/|\.gif)', test1) BETTER
    
    #test2 = re.findall('(\">|img\/)(.*?)(<\/|\.gif)', test1.replace("\B", ""))
    
    #test3 = re.findall('\', \'(.*?)\', \'', test2)
         #       test3 = re.findall('(\">|img\/)(.*?)(<\/|\.gif)', test1.replace("\B", ""))
    #print "".join(test3[0].split)
    #test4 = [x.replace(" ", "") for x in test3]
    
    
    
    #print re.search(r"\',\'(.*)\',\'", str(test3[0]).replace(" ", "")).group(0)
    #print len(test3)
    #print ""
    
    
    
     #           while len(test3) >= 5:
        
                    #print ASX_Code
      #              sh_Date = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "")).group(0)
    #

#------------------------------------------------
#------------------------------------------------

if 1==0:

    url = 'https://www.britishbulls.com/SignalPage.aspx?lang=en&Ticker='
    
    # ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
    # Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
    # which you have to simulate in the mechanize form handling library
    
    # This example shows how to follow the Next page link
    
    #scraperwiki.sqlite.execute("delete from Signal_History")
    #scraperwiki.sqlite.commit()
    
    scraperwiki.sqlite.execute("drop table if exists Signal_History")  
    scraperwiki.sqlite.execute("create table Signal_History (`TIDM` varchar2(8) NOT NULL, `Date` date NOT NULL, `Price` real NOT NULL, `Signal` varchar2(15) NOT NULL, `Confirmation` char(1) NOT NULL, `GBP 100` real NOT NULL, UNIQUE (`TIDM`, `Date`))")
    
    
    lselist = scraperwiki.sqlite.execute("select `TIDM` from company")
    
    for x in lselist["data"]:
        lsecode = str(x)[3:-2] #+ '.L'
        #print lsecode
        #print str(asxlist["data"][x])[3:-2]
    
    #for x in asxlist:
    #    print asxlist
    
    #data = scraperwiki.scrape("http://www.asx.com.au/asx/research/ASXListedCompanies.csv")
    #url2 = 'https://www.aussiebulls.com/SignalPage.aspx?lang=en&Ticker=WOW.AX'
        br = mechanize.Browser()
    
        # sometimes the server is sensitive to this information
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    #####reader = csv.DictReader(data.splitlines()[2:10])
    
    #scraperwiki.sqlite.execute("alter table companies add `Date Added` date")
    #scraperwiki.sqlite.execute("alter table companies rename to company")
    #scraperwiki.sqlite.execute("alter table company rename column `Date Added` to `Last Refreshed`")
    #scraperwiki.sqlite.execute("alter table company add `Top 500` char(1)")
    
    #scraperwiki.sqlite.execute("drop table if exists company")  
    #scraperwiki.sqlite.execute("create table company (`GICS industry group` string, `ASX code` string, `Company name` string, `Last Refreshed` date, `Top 500` char(1))")
        #scraperwiki.sqlite.execute("drop table if exists Signal_History")  
        #scraperwiki.sqlite.execute("create table Signal_History (`TIDM` varchar2(8) NOT NULL, `Date` date NOT NULL, `Price` real NOT NULL, `Signal` varchar2(15) NOT NULL, `Confirmation` char(1) NOT NULL, `GBP 100` real NOT NULL, UNIQUE (`TIDM`, `Date`))")
    
    #scraperwiki.sqlite.execute("insert into company values ('test', 'test', 'test', date('2015-12-07'), 'Y')")
    #scraperwiki.sqlite.execute("delete from company where `ASX code` = 'test'")
    
    
    #scraperwiki.sqlite.commit()
    
    #@@@scraperwiki.sqlite.save(['GICS industry group', 'ASX code', 'Company name'], list(csv.DictReader(scraperwiki.scrape('http://www.asx.com.au/asx/research/ASXListedCompanies.csv').splitlines()[2:])), table_name='company')
    #scraperwiki.sqlite.save(['industry', 'code', 'company'], list(csv.DictReader(scraperwiki.scrape('http://www.asx.com.au/asx/research/ASXListedCompanies.csv').splitlines()[2:10])), table_name="companies")
    
    #@@@scraperwiki.sqlite.execute("update company set `Last Refreshed` = date('now') where `Last Refreshed` is null")
    
    #@@@scraperwiki.sqlite.execute("update company set `Top 500` = 'Y' where `Last Refreshed` = date('now')")
    #@@@scraperwiki.sqlite.execute("update company set `Top 500` = 'N' where `Last Refreshed` <> date('now')")
    
    
    #scraperwiki.sqlite.commit()
    #scraperwiki.sqlite.execute(".schema companies")
    #scraperwiki.sqlite.execute("select * from company") 
    
    #####for record in reader:
    #####        print record
    
        response = br.open(url + lsecode)
    
        for pagenum in range(1):
            html = response.read()
        
    #comp = re.search(r'MainContent_CompanyTicker(\w{3,}\.AX)span', html).group(0)
    #ASX_Code = '3PL.AX'
      
    #print re.findall(r'MainContent_signalpagehistory_PatternHistory24((.)+)\<\\table\>', html) 
            test1 = re.search(r'MainContent_signalpagehistory_PatternHistory24_DXDataRow0((.|\n)+)MainContent_signalpagehistory_PatternHistory24_IADD', html)
    
            if test1:
                test1 = test1.group(0)
        
    
    # test2 = re.findall(r'(\"\>|img\/)((.)+)\<\/td\>\<td', test1)
    #test2 = re.findall('\">(.*)<\/', test1)
    #test2 = re.findall('\">(.*?)<\/', test1)
    #test2 re.search(r'\"\>(.*)\<\/?', test1)
    #test2 = re.findall('\">(.*?)<\/', test1) GOOD
    #test2 = re.findall('(\">|img\/)(.*?)(<\/|\.gif)', test1) BETTER
    
    #test2 = re.findall('(\">|img\/)(.*?)(<\/|\.gif)', test1.replace("\B", ""))
    
    #test3 = re.findall('\', \'(.*?)\', \'', test2)
                test3 = re.findall('(\">|img\/)(.*?)(<\/|\.gif)', test1.replace("\B", ""))
    #print "".join(test3[0].split)
    #test4 = [x.replace(" ", "") for x in test3]
    
    
    
    #print re.search(r"\',\'(.*)\',\'", str(test3[0]).replace(" ", "")).group(0)
    #print len(test3)
    #print ""
    
                while len(test3) >= 5:
        
                #print ASX_Code
                    sh_Date = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "")).group(0)
                    #sh_Date = substr(sh_Date, 7,4) + '-' + substr(sh_Date, 4,2) + '-' + substr(sh_Date, 1,2)
                    #sh_Date = sh_Date[6:10] + '-' + sh_Date[3:5] + '-' + sh_Date[:2]
                    sh_Date = date(int(sh_Date[6:10]),int(sh_Date[3:5]),int(sh_Date[:2]))
                    sh_Price = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "").replace(",", "")).group(0)
                    sh_Signal = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "")).group(0)
                    sh_Confirmation = ((re.search("[Unc|C]heck", str(test3.pop(0)).replace(" ", "")).group(0).lower()).replace("uncheck","N")).replace("check", "Y")
                    sh_GBP100 = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "").replace(",", "")).group(0)
            
            #scraperwiki.sqlite.execute("insert or replace into Signal_History values (:`ASX code`, :Date, :Price, :Signal, :Confirmation, :`AUD 100`)",  {"ASX code":ASX_Code, "Date":sh_Date, "Price":sh_Price, "Signal":sh_Signal, "Confirmation":sh_Confirmation, "AUD 100":sh_AUD100})
    
                    scraperwiki.sqlite.execute("insert or ignore into Signal_History values (?, ?, ?, ?, ?, ?)",  [lsecode, sh_Date, sh_Price, sh_Signal, sh_Confirmation, sh_GBP100]) 
    
                    scraperwiki.sqlite.commit()    
    
       
      # print re.search(r'\w{3}\.AX', re.search(r'MainContent_CompanyTicker((.)+)span', html).group(0)).group(0)
    
