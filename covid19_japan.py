# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 09:26:38 2020

@author: Johnny Tsai
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

url = 'https://www3.nhk.or.jp/news/special/coronavirus/data-all/'
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.implicitly_wait(20)
driver.get(url = url)
html_source = driver.page_source
driver.quit()
    
soup = BeautifulSoup(html_source, 'lxml')
data = soup.find_all('td')[0].text.replace('\n','').replace('万','').replace('          前日比 ','').replace('人','').rstrip()
data = data.split('+', 1)

time.sleep(3)

url_tk = 'https://www3.nhk.or.jp/news/special/coronavirus/data/'
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.implicitly_wait(20)
driver.get(url = url_tk)
html_source_tk = driver.page_source
driver.quit()
    
soup_tk = BeautifulSoup(html_source_tk, 'lxml')
data_tk = soup_tk.find_all('td', class_='area-color_03 border-point-dotted-left')[0].text

#LINE NOTIFY

infected = format(int(data[0]),',')
add = format(int(data[1]),',')

def lineNotifyMessage(token, msg):
   headers = {
       "Authorization": "Bearer " + token, 
   }
	
   payload = {'message': msg}
   r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
   return r.status_code
	
message = '\n' + '全國確診人數總計：' + infected + '人' + '\n' + '昨日全國新增確診：' + add + '人' + '\n' + '昨日東京新增確診：' + data_tk + '人'
token = 'please input Line notify token'

lineNotifyMessage(token, message)




