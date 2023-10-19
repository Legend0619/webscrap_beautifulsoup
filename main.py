from bs4 import BeautifulSoup
import requests
import time

def find_products():
    html_text = requests.get('https://boxfox.com/collections/all').text
    soup = BeautifulSoup(html_text, 'lxml')
    products = soup.find_all('product-grid-item')
    
    with open('product.txt', 'w') as f:
        for product in products:
            title = product.find('p', class_ = 'product__grid__title').text.replace(' ', '').replace('\n', '')
            price = product.find('span', class_ = 'price').text.replace(' ', '').replace('\n', '')

            if 'From' not in price:
                f.write(f'Title: {title}')
                f.write(f'Price:  {price}')
                f.write('\n')

if __name__ == '__main__':
    while True:
        find_products()
        time_wait = 10
        print(f'Waiting {time_wait} seconds...')
        time.sleep(time_wait * 60)

