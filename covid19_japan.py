# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 09:26:38 2020

@author: Johnny Tsai
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
from PIL import Image
from io import BytesIO

url = 'https://www3.nhk.or.jp/news/special/coronavirus/data-all/'
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.implicitly_wait(20)
driver.get(url = url)
html_source = driver.page_source
driver.quit()
    
soup = BeautifulSoup(html_source, 'lxml')
data = soup.find_all('td')[0].text.replace('\n','').replace('万','').replace('          前日比 ','').replace('人','').rstrip()
data = data.split('+', 1)

time.sleep(1)

img_url = 'https://www3.nhk.or.jp/news/special/coronavirus/data/'

driver = webdriver.Chrome(executable_path='./chromedriver')
driver.implicitly_wait(20)
driver.get(url = img_url)
html_source_img = driver.page_source
driver.quit()

soup_img = BeautifulSoup(html_source_img, 'lxml')
link_img = soup_img.select('.c-slideimage figure img')[0].get('src').split('/')

link = 'https://www3.nhk.or.jp/news/special/coronavirus/still/' + link_img[5]

response = requests.get(link)
image = Image.open(BytesIO(response.content))
image.save('C:/Users/ultsai/Desktop/PYTHON/IMG/' + link_img[5])

infected = format(int(data[0]),',')

#LINE NOTIFY
def lineNotifyMessage(token, msg, picURI):
   headers = {
       "Authorization": "Bearer " + token, 
   }
	
   payload = {'message': msg}
   files = {'imageFile': open(picURI, 'rb')}
   r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload, files = files)
   return r.status_code
	
message = '\n' + '全國確診人數總計：' + infected + '; \n' + '昨日新增請參閱下圖：'
token = ['*******']
picURI ='C:*****/IMG/'

lineNotifyMessage(token, message, picURI)
