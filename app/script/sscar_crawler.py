import requests
from bs4 import BeautifulSoup
import json


def sscar_crawler(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='title-wrapper')
    result = []
    seen_urls = set()  # 用於去重複的集合

    for product in products:
        product_name = product.find(
            'a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').text
        product_url = product.find(
            'a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')['href']

        # 檢查 URL 是否已經處理過，避免資料重複
        if product_url not in seen_urls:
            seen_urls.add(product_url)  # 將 URL 添加到集合中
            result.append({'name': product_name, 'url': product_url})

    return result


def get_yahoo_link(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 網頁結構中第二個 h4 標籤下的 a 標籤包含我們需要的連結
        link = soup.find_all('h4')[1].find('a')['href']
        return link
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    url = "https://sscars.com.tw/car/page/2/"
    cars_list = sscar_crawler(url)

    # 爬完的小施汽車獲得name和url後，再由url獲得yahoo短網址
    for car in cars_list:
        car_url = car['url']
        if car_url:
            car['short_link'] = get_yahoo_link(car_url)

    # 存為json檔
    with open("app/script/car_list.json", 'w', encoding='utf-8') as f:
        json.dump(cars_list, f)


if __name__ == "__main__":
    main()
