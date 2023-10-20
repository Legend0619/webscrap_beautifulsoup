import requests
from bs4 import BeautifulSoup

website = 'https://subslikescript.com/movie/Titanic-120338'

result = requests.get(website)
if result.ok:
    soup = BeautifulSoup(result.content, 'lxml')
    box = soup.find('article', class_ = 'main-article')
    title = box.find('h1').get_text()
    transcript = box.find('div', class_ = 'full-script').get_text(strip=True, separator=' ')
    with open(f'{title}.txt', 'w') as file:
        file.write(transcript)
else:
    print('error')