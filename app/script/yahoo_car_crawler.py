from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup
import os
import shutil
import json
from tqdm import tqdm


def init_driver(headless=True):
    # 初始化 WebDriver，並設置無頭模式
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    # 初始化 WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def yahoo_car_crawler(driver, url):
    try:
        driver.get(url)
        # 等待頁面loading完成
        time.sleep(3)

        current_url = driver.current_url
        print("get current url:", current_url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        spec_wrapper = soup.find('div', {'class': 'spec-wrapper'})
        if spec_wrapper is None:
            return None
        cars_table_dict = {
            'body': '車身型式',
            'door': '車門數',
            'seat': '座位數',
            'car_length': '車長',
            'wheelbase': '軸距',
            'power_type': '動力型式',
            'displacement': '排氣量',
        }

        info_dict = {}
        # 將網頁的標題添加到車輛資訊中，並只取 '|' 前的部分
        # 'Ford 2020 Focus 4D EcoBoost 182佛心版 | 規格配備 - Yahoo奇摩汽車機車'
        title = soup.find('title').text

        # 處理字串，分別為 廠牌、年份、車款
        car_name = title.split('|')[0].strip().split(" ")
        info_dict['name'] = ' '.join(car_name)
        info_dict['brand'] = car_name[0]
        info_dict['year'] = car_name[1]
        info_dict['model'] = " ".join(car_name[2:-1])
        jpg_folder_name = ' '.join(car_name)

        # 下載儲存圖片
        # save_images(soup, jpg_folder_name)

        # 將爬取的規格資訊存於info_dict
        for field_key, field in cars_table_dict.items():
            field_info = spec_wrapper.find('span', string=field)
            if field_info is not None:
                field_value = field_info.find_next_sibling('span').text
                info_dict[field_key] = field_value
            else:
                info_dict[field_key] = None
        print(info_dict)
        return info_dict

    except Exception as e:
        print(f"發生錯誤：{e}")


def save_images(soup, title):
    # Create a directory path
    base_directory = "app/static/crawler"
    directory = os.path.join(base_directory, title)

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Find all image tags in the carousel
    image_tags = soup.find_all('img', {'class': 'gabtn'})

    # Download and save each image
    for i, img in tqdm(enumerate(image_tags[:5]), desc="Downloading images", total=min(5, len(image_tags))):
        img_url = img['src']
        # stream = True 可用於處理大量數據，有效管理內存使用的方法
        response = requests.get(img_url, stream=True)

        # Check if the image was retrieved successfully
        if response.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            response.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission and write the image into the file
            # shutil使用複製的方式，讀取後存到目標文件中。可以提高效率，尤其時對於大型文件。
            with open(directory + '/img_'+str(i)+'.jpg', 'wb') as f:
                shutil.copyfileobj(response.raw, f)


def main():
    driver = init_driver()
    # 從 JSON 文件讀取車輛 URL 列表
    try:
        with open("app/script/car_list.json", "r") as file:
            car_list = json.load(file)

        cars_info = []  # 用於儲存每個車輛頁面爬取的資訊
        for car in car_list:
            car_url = car['short_link']
            car_info = yahoo_car_crawler(driver, car_url)
            if car_info:
                cars_info.append(car_info)
        # 將爬取的資訊存儲到 cars.json 文件中
        with open("app/script/cars.json", "w") as file:
            json.dump(cars_info, file)

    except Exception as e:
        print(f"發生錯誤：{e}")
    finally:
        driver.quit()  # 確保在所有操作完成後才關閉 WebDriver


if __name__ == "__main__":
    main()
