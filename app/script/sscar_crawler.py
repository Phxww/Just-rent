import requests
from bs4 import BeautifulSoup
import json

# 爬取汽車列表
def sscar_crawler(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='title-wrapper')
    result = []
    for product in products:
        name = product.find(
            'a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').text
        url = product.find(
            'a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')['href']
        result.append({'name': name, 'url': url})
    return result

# 獲得短網址
def get_yahoo_link(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find_all('h4')[1].find('a')['href']
        return link
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# 使用範例
url = "https://sscars.com.tw/car/"
cars_list = sscar_crawler(url)

# 爬完的小施汽車獲得name和url後，再由url獲得yahoo短網址
for car in cars_list:
    url = car['url']
    if url is not None:
        car['short_link'] = get_yahoo_link(url)

car_list_json = json.dumps(cars_list)

# 存為json檔
with open("app/script/car_list.json", 'w', encoding='utf-8') as f:
    json.dump(cars_list, f)  # Write the list to a file
