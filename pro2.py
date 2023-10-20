import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://your.url/here?yes=brilliant')
results = []
other_results = []
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

for a in soup.find_all(attrs={'class': 'title'}):
    name = a.find('a')
    if name not in results:
        results.append(name.text)

for b in soup.find_all(attrs={'class': 'otherclass'}):
    name2 = b.find('span')
    if name2 not in other_results:
        other_results.append(name2.text)

series1 = pd.Series(results, name="Names")
series2 = pd.Series(other_results, name='Categories')
df = pd.DataFrame({'Names': series1, 'Categories': series2})
df.to_csv('names.csv', index=False, encoding='utf-8')