import requests
import mechanize 
from bs4 import BeautifulSoup 
import csv
import numpy as np
import json
#Base URL 
url = "https://sset.ecoleaide.com"
new_url = requests.get(url)
print(new_url.url)

#Filtering Session ID from the base URL

session_filter = str(new_url.url)
session = session_filter.split(';')
session = ";" + session[1]
print(session)



#Inputs to submit form
username = "SEE/6993/16"
password = "69936993"

# username = input("Enter username :")
# password = input("Enter Password :")


username = "SSET_" + username 

# Ecoliade Login Action 

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]
sign_in = br.open(new_url.url)  #the login url
br.select_form(nr = 0) 
br.set_all_readonly(False)
br["username"] =username 
br["password"] =password  
logged_in = br.submit()  
logincheck = logged_in.read()  

#Scrapping Needed Data
new_url = br.geturl()
print(new_url)

def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())
def SimpleDecode(jsonDump):
    return np.array(json.loads(jsonDump))

def Attendance(session):
	new_url = br.open("https://sset.ecoleaide.com/search/subjAttendReport.htm" + session)
	details = new_url.read()
	# print(details)
	soup = BeautifulSoup(details, 'html5lib') 
	# print(soup.prettify()) 
	#Getting Attributes
	data=[]
	table = soup.find('table', attrs = {'class':'subj-attendance-table'})
	table_body = table.find('tbody')

	rows = table_body.find_all('tr')
	datas = np.array([], dtype=float, ndmin=2)
	i = 0
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    # print(cols)
	    data.append([ele for ele in cols if ele])
	    data[i] = cols
	    i= i+1

	return data

attendance = Attendance(session)
print(SimpleEncode(attendance))