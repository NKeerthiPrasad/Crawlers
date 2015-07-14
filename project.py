import urllib2
from bs4 import BeautifulSoup
import lxml.html as html1
from goose import Goose
import re
import json
import requests
from lxml.html.clean import Cleaner
# import sys
# sys.setdefaultencoding('utf-8')
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
job=re.compile('.*operations.*|.*innovations.*|.*products.*|.*technology.*|.*project.*|.*solution.*|.*What we do.*|.*businesses.*|.*service.*|.*vehicles.*|.*station.*|.*activities.*|.*segments.*',re.IGNORECASE)
r1=re.compile('.*live.*|.*google.*|.*yahoo.*|.*subscription.*|.*login.*|.*signup.*|.*facebook.*|.*twitter.*|.*linkedin.*|.*rss.*|.*blog.*',re.IGNORECASE)
techno=re.compile('.*technolog.*',re.IGNORECASE)
services=re.compile('.*service.*',re.IGNORECASE)
operations=re.compile('.*operation.*',re.IGNORECASE)
activities=re.compile('.*activit.*',re.IGNORECASE)
innovations=re.compile('.*innovation.*',re.IGNORECASE)

urls=[]# List of urls
l=[]
project = []
crawledLink = []
d={}
v = {}
fin={}
ill=0
count = 0
def crawl(link1):
    try:
        global depth
        depth=depth+1
        if depth < 10:
        #count=count+1
            html=requests.get(link1)
            soup1=BeautifulSoup(html.content)
            for l in soup1.find_all('a'):
                l1=str(l.get('href')).encode("utf-8")
                print l1
                if not l1 in crawledLink and job.match(l1) and not r1.match(l1):

                    crawledLink.append(l1)
                    if not linkPattern.match(l1):
                        if l1[0]!='/':
                            l1=url+'/'+l1
                        else:
                            l1=url+l1
                  
                #print l1
                    if not l1 in project:
                        project.append(l1)
                    
                
                    a=crawl(l1)
    except:
        pass

            #else:
                #count=0
           
for url in urls:
    try:

        ill=ill+1
        # filname=url.replace('http://' or 'https://','') # if you want name of the company as the file name
        # filname=filname.replace('.*www.','')
        # filname=filname.replace('.com','')
        # filname=filname.replace('.org.*','')
        # print filname
        project=[]
        with open('link%i.json'%ill,"w") as outfile:
            try:
                html = requests.get(url)
                soup = BeautifulSoup(html.content)
                title=soup.title.string
                for link in soup.find_all('a'):
                    link1 = str(link.get('href')).encode('ascii','ignore')
                    print link1
                    if job.match(link1) and not r1.match(link1):
                        if not link1 in crawledLink:
                            crawledLink.append(link1)
                            if not linkPattern.match(link1):
                                if link1[0]!='/':
                                    link1=url+'/'+link1
                                else:
                                    link1=url+link1
                        
                            depth = 0
                            project.append(link1)
                            a=crawl(link1)

                print "project -------->>>>> ",project
                for every in project:
                    flag=0
                    try:
                        a = every.split('/')
                        print "URL paths ------>>>> ",a
                        for each in a:
                            if techno.match(each):
                                flag=1
                            elif services.match(each):
                                flag=2
                            elif operations.match(each):
                                flag=3
                            elif activities.match(each):
                                flag=4
                            elif innovations.match(each):
                                flag=5
                        print "flag ------>>>>> ",flag

                        print every
                        html = requests.get(every)
                        soup = BeautifulSoup(html.content)
                        for elem in soup.findAll(['script', 'style']):
                            elem.extract()
                        g=Goose()
                        art=g.extract(every)
                        text=art.cleaned_text.encode('ascii','ignore')
                        qw = re.sub(r'\n\n\n','',str(text))
                        d["title"] = art.title
                        d["description"] = text

                        if flag == 0:
                            d["tag"] = "Products"
                        elif flag == 1:
                            d["tag"] = "Technology"
                        elif flag == 2:
                            d["tag"] = "Services"
                        elif flag == 3:
                            d["tag"] = "Operations"
                        elif flag == 4:
                            d["tag"] = "Activities"
                        elif flag == 5:
                            d["tag"] = "Innovations"
                        print d
                        if d not in l:
                            l.append(d.copy())
                    except:
                        pass 
                v["company_nme"]= title  
                v["project"] = l
                l=[]
                print v
                json.dump(v,outfile)
                
            finally:
                outfile.close()

    except:
        pass



