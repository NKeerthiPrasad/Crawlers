import requests
import json
import re
from bs4 import BeautifulSoup
import lxml.html as html1
from lxml.html.clean import Cleaner
from goose import Goose
from commonregex import CommonRegex
urls=[]

ill = 0
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

job=re.compile('.*team.*|.*contact.*|.*about.*|.*management.*|.*director.*|.*board.*',re.IGNORECASE)
job_okok=re.compile('.*team.*|.*contact.*|.*about.*|.*management.*|.*director.*|.*governance.*|.*exec.*|.*board.*',re.IGNORECASE)
unwanted=re.compile('.*join.*|.*project.*|.*blog.*|.*mailto.*|.*pdf.*|.*recruit.*|.*events?.*|.*facts.*|.*mission.*|.*values.*|.*faq.*|.*news.?r?.*|.*career.*|.*updates.*|.*history.*|.*vision.*|.*award.*|.*products.*|.*polic(y|ies).*|.*capabilities.*|.*feedback.*|.*support.*|.*innovaitons.*',re.IGNORECASE)

lang=re.compile('.*japanese.*|.*mandarin.*|.*portuguese.*|.*germen.*|.*french.*|.*twitter.*|.*linkedin.*|.*google.*',re.IGNORECASE)
err=re.compile('.*runtime.?error.*|.*403.?.?forbidden.*|.*not.?found.*',re.IGNORECASE)
noname=re.compile('.*region.*|.*information.*|.*recent.*|.*viewed.*|.*security.*|.*who.we.are.*|.*relat.*|.*our .*',re.IGNORECASE)
about=re.compile('.*about.*',re.IGNORECASE)
management=re.compile('.*management.*|.*directors.*|.*team.*|.*exec.*|.*bod.*|.*leadership.*|.*staff.*|.*board.*',re.IGNORECASE)
contact=re.compile('.*contact.*',re.IGNORECASE)
members={}
boo=True
name=re.compile('([A-Z]. )?[A-Z][a-z]* ([A-Z]. )?[A-Z][a-z]*')
desig=re.compile('.*chief.*|.*executive.*|.*officer.*|.*(corporate)?..?secretary.*|.*accounting.*|.*operating.*|.*general.*|.*counsel.*|.*vice.*|.*president.*|.*senior.*|.chairman.*|.*director.*|.*treasurer.*|.*principal.*|.*financial.*|.*accountant.*|.*assistant.*',re.IGNORECASE)
desc_link=[]
crawledLink=[]
word_pattern = re.compile('([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+[a-z]+)?(?:\s+[A-Z][a-z]+)+)')
 
depth_level=0
for url in urls:
	ill=ill+1
	filname=url.replace('http://','')
	filname=filname.replace( 'https://','')
	filname=filname.replace('www.','')
	filname=filname.replace('.com','') 
	filname=filname.replace( '.org','')
	filname=filname.replace( '.gov','')
	print filname

	with open('%s.json'%filname,"w") as outfile:
		def crawl(link1):
			
			try:
				global depth_level
				depth_level=depth_level+1
				if depth_level<=10:
					html=requests.get(link1)
					soup1=BeautifulSoup(html.content)
					for l in soup1.find_all('a'):
						l1=str(l.get('href'))
						
						if not linkPattern.match(l1):
							if l1[0]!='/':
								l1=url+'/'+l1
							else:
								l1=url+l1

						if (job_okok.match(l1) or job_okok.match(l.get_text())) and  not ( unwanted.match(l1) or unwanted.match(l.get_text())) and not lang.match(l1) and not l1 in crawledLink:
							crawledLink.append(l1)								
							
							if not l1 in desc_link:
								desc_link.append(l1)
							a=crawl(l1)

			except:
				print "ERROR with " + link1


		try:
			shtml=requests.get(url)

			desc_link=[]
			career_links=[]
			soup = BeautifulSoup(shtml.content)
			for link in soup.find_all('a'):
				link1=link.get('href')
				#print link1
				if (job_okok.match(str(link.get('href'))) or job_okok.match(link.get_text()))and not (unwanted.match(link1) or unwanted.match(link.get_text())) and not lang.match(link1):
					#print "tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
					if not linkPattern.match(link1) :
						if link1[0]!='/':
							link1=url+'/'+link1
						else:
							link1=url+link1
					if not link1 in crawledLink:
						crawledLink.append(link1)
						depth_level=0
						desc_link.append(link1)
						a=crawl(link1)
		except:
			pass
		print desc_link
		if len(desc_link)==0:
			desc_link.append(url)
		import urllib
		text=[]
		mem=[]
		new=0
		for link in desc_link:
			try:
				g=Goose()
				text=[]
				html = requests.get(link)    
				raw = BeautifulSoup(html.content)
				if err.match(str(raw('title'))) or err.match(str(raw('text'))):
					print "server error with "+link
					continue
				if about.match(link) and not management.match(link) and not contact.match(link) and not unwanted.match(link) and boo:
					print link
					about1={}
					about1['name']=g.extract(url=url).title						
					art=g.extract(url=link)

				 	soup=BeautifulSoup(requests.get(link).content)
					for s in soup('style'):
						s.extract()
					for s in soup('script'):
						s.extract()
					for s in soup('input'):
						s.extract()	
					licount=len(soup.find_all('li'))
					pcount=len(soup.find_all('p'))
					tdcount=len(soup.find_all('td'))
					divcount=len(soup.find_all('div'))
					print str(licount) + " " + str(pcount) + " " + str(tdcount)
						
					if pcount>licount and pcount>tdcount:
						for p in soup.find_all('p'):
							if len(p.get_text())>100:
								text.append(p.get_text())
					
					else:
						text=art.cleaned_text
					about1['about']=text
					boo=False
					if not text:
						boo=True
					else:
						print about1

				if management.match(link) and not contact.match(link):
					try:
						soup=BeautifulSoup(requests.get(link).content)
						print link
						for s in soup('style'):
							s.extract()
						for s in soup('script'):
							s.extract()
						for s in soup('input'):
							s.extract()
						for s in soup('a'):
							s.extract()
						members={}
						
						added_dena=[]
						para=[]
						li=[]
						for p in soup.find_all('p'):
							para.append(p.get_text())
						for word in soup.find_all(['b','strong','h1','h2','h3','h6','p','span']):
							f=0
							txt=word.get_text()
							if len(txt)<20:								
								if desig.match(txt):
									f=1

								if f==0 and name.match(txt) and not noname.match(txt) and not job.match(txt) and not txt in added_dena:
									members['name']=txt
									members['description']=''

									added_dena.append(txt)

									if len(members['name'])<25:

										li=members['name'].split(' ')
										li1='|'.join(li)
														
										li1=re.compile(li1)

										for para in soup.find_all('p'):
											para=para.get_text()
			
											if len(para)>50 and re.search( li[-1], para,re.IGNORECASE):
	
												members['description']=members['description']+ ' '+para
										# if members['description']:
										# 	text2=members['description']
										# 	members['designation']=''
										# 	for t in text2.split(' '):
										# 		if t.lower() in desig:
										# 			members['designation']=members['designation']+t+' '
										# 		elif t.lower() in ['and',',']:
										# 			members['designation']=members['designation']+t+' '
									
									txt=members['name']
									if name.match(txt) and not noname.match(txt) and not job_okok.match(txt) and not unwanted.match(txt) and txt:	
										new= new + 1
										f=1
										#print 'listttttttttttttttttttttttttttttttttt'
										#print len(mem)
										#print 'dict==================='
										#print members
										if len(mem):
											for i in range(len(mem)):
												#print i
												#print mem[i]['name'] 
												if mem[i]['name']==members['name']:
													f=0
													if len(mem[i]['description'])<=len(members['description']):
														mem[i]['description']=members['description']
													else:
														pass
													break
										#else:
											#mem[0]=members
										if f:
											#print 'abc'
											mem.append(members)
											
											members={}
								
							elif len(txt)<100:
								pass
					except:
						print "ERROR1 with " + link
				
			except:
				print "ERROR2 with " + link
		print mem
		for i in range(len(mem)):
			if mem[i]['description']:
				mem[i]['designation']=''
				w=mem[i]['description'].split('.')
				print w[0]
				f=0
				for word in w[0].split(' '):
					
					if desig.match(word):

						f=1
						mem[i]['designation']=mem[i]['designation']+word+' '
					elif f==1:

						if re.compile('.?.?of.?.?|.?.?for.?.?').match(word):
							f=0
							break
						else:
							mem[i]['designation']=mem[i]['designation']+word+' '

		try:
			about1['members']=mem
			json.dump(about1,outfile)

		except:
			print "json ERROR"
