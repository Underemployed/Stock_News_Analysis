import re
import csv
import time

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
ticker=input("Enter Ticker\n>")
driver = webdriver.Chrome()
driver.get('https://in.investing.com/search/?q='+ticker+'&tab=news')

time.sleep(3)
prev = driver.execute_script('return document.body.scrollHeight;')

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(0.5)
    new_height = driver.execute_script('return document.body.scrollHeight;')
    if new_height == prev:
        break
    prev = new_height

html_content = driver.page_source

driver.quit()

soup = BeautifulSoup(html_content, 'html.parser')
articles = soup.find_all('article')

data = []
pattern = r'<a class="js-category-item-link link" href="(.*?)">\s+<div class="content">\s+<h4 class="js-category-item-title title">(.*?)</h4>\s+<footer class="details">\s+<ul class="details-list">\s+<li class="js-category-item-provider details-item is-darker">(.*?)</li>\s+<li class="details-item">\s+<time class="js-category-item-time">(.*?)</time>'

matches = re.findall(pattern, str(soup), re.DOTALL)

for match in matches:
    url = "https://in.investing.com" + match[0]
    heading = match[1]
    provider = match[2]
    time_element = match[3]

    data.append([time_element, url, heading,ticker])



df = pd.DataFrame(data, columns=['Time', 'URL', 'Heading','Ticker'])

filename = "data.csv"
df.to_csv(filename, index=False)
print("Data has been written to", filename)
