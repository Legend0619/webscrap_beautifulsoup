from requests import get
from bs4 import BeautifulSoup
from warnings import warn
from time import sleep
from random import randint
import numpy as np, pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pages = np.arange(1, 200, 50)
headers = {'Accept-Language': 'en-US,en;q=0.8'}

#initialize empty lists to store the variables scraped
titles = []
years = []
ratings = []
genres = []
runtimes = []
imdb_ratings = []
imdb_ratings_standardized = []
metascores = []
votes = []

for page in pages:

    #get request for sci-fi
    response = get('https://www.imdb.com/search/title?genres=sci-fi&' + 'start=' + str(page) + '&explore=title_type,genres&ref_=adv_prv', headers=headers)
    sleep(randint(8, 15))

    #throw warning for status codes that are not 200
    if response.status_code != 200:
        warn('request: {}; Status code: {}'.format(page, response.status_code))

    #parse the content of current iteration of request
    page_html = BeautifulSoup(response.content, 'html.parser')

    movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

    #extract the 50 movies for that page
    for container in movie_containers:

        #conditional for all with metascore
        if container.find('div', class_ = 'ratings-metascore') is not None:

            #title
            title = container.h3.a.text
            titles.append(title)

            if container.h3.find('span', class_ = 'lister-item-year text-muted unbold') is not None:

                #year
                year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
                years.append(year)

            else:
                years.append(None)

            if container.p.find('span', class_ = 'certificate') is not None:

                #rating
                rating = container.p.find('span', class_ = 'certificate').text
                ratings.append(rating)

            else:
                ratings.append('')

            if container.p.find('span', class_ = 'runtime') is not None:

                #runtime
                time = int(container.p.find('span', class_ = 'runtime').text.replace(' min', ''))
                runtimes.append(time)

            else:
                runtimes.append(None)

            if float(container.strong.text) is not None:

                #IMDB ratings
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

            else:
                imdb_ratings.append(None)

            if container.find('span', class_ = 'metascore').text is not None:

                #Metascore
                m_score = int(container.find('span', class_ = 'metascore').text)
                metascores.append(m_score)

            else:
                metascores.append(None)

            if container.find('span', attrs = {'name':'nv'})['data-value'] is not None:

                #Number of votes
                vote = int(container.find('span', attrs = {'name':'nv'})['data-value'])
                votes.append(vote)

            else:
                votes.append(None)

sci_fi_df = pd.DataFrame({
    'movie': titles,
    'year': years,
    'rating': ratings,
    'runtime_min': runtimes,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes
})

sci_fi_df.loc[:, 'year'] = sci_fi_df['year'].str[-5:-1] # two more data transformation after scraping
# Drop 'ovie' bug
# Make year an int
sci_fi_df['n_imdb'] = sci_fi_df['imdb'] * 10
final_df = sci_fi_df.loc[sci_fi_df['year'] != 'ovie'] # One small issue with the scrape on these two movies so just dropping those ones.
final_df.loc[:, 'year'] = pd.to_numeric(final_df['year'])

x = final_df['n_imdb']
y = final_df['votes']
plt.scatter(x, y, alpha=0.5)
plt.xlabel('IMDB Rating Standardized')
plt.ylabel("Number of Votes")
plt.title("Number of Votes vs IMDB Rating")
plt.ticklabel_format(style='plain')
plt.show()

ax = final_df['rating'].value_counts().plot(kind='bar', figsize=(14, 8), title='Number of Movies by Rating')
ax.set_xlabel('Rating')
ax.set_ylabel('Number of Movies')
ax.plot()