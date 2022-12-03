from selenium import webdriver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pandas as pd

names = []
category = []
ratings = []
chrome_options = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
chrome_options.add_argument("--headless")
chrome_options.add_argument(f'user-agent={user_agent}')
driver = uc.Chrome(options=chrome_options)

for i in range(1, 5):
    if i == 1:
        driver.get('https://www.myntra.com/shoes')
    else:
        driver.get('https://www.myntra.com/shoes?p={}'.format(i))
    content = driver.page_source
    soup = BeautifulSoup(content, 'html5lib')
    products = soup.find_all('li', class_='product-base')
    for product in products:
        try:
            ratings.append(product.find('div', class_='product-ratingsContainer').find('span').get_text())
        except AttributeError:
            ratings.append(None)
        names.append(product.find('h3', class_='product-brand').get_text() + ' : ' + product.find('h4', class_='product-product').get_text())
driver.close()

df = pd.DataFrame(names, columns=['product_name'])
df['ratings'] = ratings
df['category'] = ['Sneakers'] * len(df)
df = df[df['product_name'].apply(func=lambda string : string.lower()).str.contains('sneakers')]
df.to_csv('products.csv')