import urllib2
from bs4 import BeautifulSoup
import lxml.html as html1
from goose import Goose
import re
import json
import feedfinder
import requests
from lxml.html.clean import Cleaner
# import sys
# sys.setdefaultencoding('utf-8')
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
job=re.compile('.*rss.*|.*feeds.*|.*rssfeeds.|.*source=feedburner.*|.*feed.*',re.IGNORECASE)
r1=re.compile('.*live.*|.*google.*|.*yahoo.*|.*subscription.*|.*login.*|.*signup.*|.*twitter.*|.*facebook.*|.*pdf.*',re.IGNORECASE)


urls=[]# add url

l=[]
#print url
#html = requests.get(url)
#soup = BeautifulSoup(html.content)
#print "d"
blogs = []
crawledLink = []
d={}
v = {}
fin={}
ill=50
count = 0
def crawl(link1):
    try:
        global depth
        depth=depth+1
        if depth < 10:
        #count=count+1
            html=requests.get(link1)
            soup1=BeautifulSoup(html.content)
            #print soup1
            # print '##########'
            # print soup1.find_all('link')
            # print soup1.find_all('link/')
            # listOfLinks = []
            # listOfLinks.extend(soup1.find_all('a'))
            #listOfLinks.extend()
            for l in soup1.find_all('a'):              
                l1=str(l.get('href')).encode("utf-8")

                if not l1 in crawledLink and job.match(l1) and not r1.match(l1):
                    #print '222222'
                    crawledLink.append(l1)
                    if not linkPattern.match(l1):
                        if l1[0]!='/':
                            l1=url+'/'+l1
                        else:
                            l1=url+l1
                  
                #print l1
                    if not l1 in blogs:
                        blogs.append(l1)
                    
                
                    a=crawl(l1)
    except:
        pass

            #else:
                #count=0
           
for url in urls:
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.content)
        name=soup.title.string
        fr=feedfinder.feeds(url)
        print (fr)




        ill=ill+1
        # filname=url.replace('http://' or 'https://','')
        # filname=filname.replace('.*www.','')
        # filname=filname.replace('.com','')
        # filname=filname.replace('.org.*','')
        # print filname
        blogs=[]
        with open('link%i.json'%ill,"w") as outfile:
            
                html = requests.get(url)
                soup = BeautifulSoup(html.content)
                title=soup.title.string
                for link in soup.find_all('a'):
                    #print "111111111111111111"
                    link1 = str(link.get('href')).encode('ascii','ignore')
                    flag=0
                    if job.match(link1) and not r1.match(link1):
                        # flag=1
                        # if flag=='0':
                        #     blogs.append(fr)
                        # else:
                        #print '333333'
                            if not link1 in crawledLink:
                                #print '4444444'
                                crawledLink.append(link1)
                                if not linkPattern.match(link1):
                                    #print '5555555555'
                                    if link1[0]!='/':
                                        link1=url+'/'+link1
                                    else:
                                        link1=url+link1
                            
                                depth = 0
                                #blogs.append(link1)
                                #print '666666666'
                                print link1
                                if len(fr)>0:
                                    #print"QqQQQQqqqQQQQ"
                                    blogs.append(link1)
                                else:
                                    a=crawl(link1)    
                     
                    else:
                        blogs=fr       
    except:
        pass


print "project -------->>>>> ",blogs
l=[]
li=[]
for a in blogs:
    try:
    
        html = requests.get(a)
        soup = BeautifulSoup(html.content)
        html45 = html1.parse(a).xpath('//pubdate//text()')
        print html45
        
        
        if soup.find_all('guid'):
            for link in soup.find_all('guid'):
                #print '@@@@@@@@@@@@@@@@@@@@@@'
                az = str(link.get_text()).encode('ascii','ignore')
                #az = str(link.get('href')).encode('ascii','ignore')
                
                #print az
                if az not in l:
                    l.append(az)
        else:
            for link in soup.find_all('comments'):

                az = str(link.get_text()).encode('ascii','ignore')

                if az not in l:
                    l.append(az)
        print l
    except:
        pass
i=0
for al in l:
    try:
        # print "11111111111"
        #print al
        #html = html1.parse(al).xpath("//h5[@class='itemposttime']")
        #print "$$$$$$$$$$$" 
        #print html
        d={}
        g = Goose({'browser_user_agent': 'Mozilla'})
        g=Goose()
        art=g.extract(al)
        #print art.title
        title = art.title
        text=art.cleaned_text.encode('ascii','ignore')
        #print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
        #print text
        d["title"] = title
        d["description"] = text
        d["rss link"] = al
        #print "222222222222222222"
        d["updatedDate"]=html45[i]
        i=i+1
        #print html45[1]
        li.append(d.copy())
        
    except:
        pass
#print li
v["company_name"] = name
v["blogs"]=li
print v

