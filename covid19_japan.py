# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 09:26:38 2020

@author: Johnny Tsai
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import requests


url = 'https://www3.nhk.or.jp/news/special/coronavirus/data-all/'
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.implicitly_wait(20)
driver.get(url = url)
html_source = driver.page_source
driver.quit()
    
soup = BeautifulSoup(html_source, 'lxml')
data = soup.find('td', class_='tbody-td-infection-total').text.replace('\n','').replace('          前日比','').replace('人','').strip()
data = data.split('+', 1)
infected_total = data[0].strip().split('万', 1)
infected_yesterday = data[1]

if len(infected_total[1]) <= (len(infected_total[0])+2):
    infected_total = infected_total[0] + '0' * (4-len(infected_total[1])) + infected_total[1]
    
else:
    infected_total = infected_total[0] + infected_total[1]
    
infected_total = format(int(infected_total),',')
infected_yesterday = format(int(infected_yesterday),',')

#LINE NOTIFY
def lineNotifyMessage(token, msg):
   headers = {
       "Authorization": "Bearer " + token, 
   }
	
   payload = {'message': msg}
   r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
   return r.status_code

link = 'https://www3.nhk.or.jp/news/special/coronavirus/data/'
token = 'add your token'	
message = '\n' + '全國確診人數總計：' + infected_total + ' 😷 \n' + '昨日新增確診人數：' + infected_yesterday + ' 😷 \n' + link

lineNotifyMessage(token, message)
