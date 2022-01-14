from lib2to3.pgen2 import driver
import driver as driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telnetlib import EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager import manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
import time
import requests
from bs4 import BeautifulSoup

global text
global result
global acc_id


headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.9"
           }

id_octo = input("Введите ключевое слово для аккаунтов: ")
url = "https://app.octobrowser.net/api/v2/automation/profiles?search={}".format(id_octo)

payload = {}
headers_octo = {
    'X-Octo-Api-Token': '79556756b1b64c6e84d51d18570dac99'
}

data_uuid = {}

response_octo = requests.request("GET", url, headers=headers_octo, data=payload)
data_uuid = response_octo.json()
uuid = data_uuid.get('data')
newuuid = dict()
for ud in uuid:
    newuuid[ud.pop('uuid')] = ud

octo = str(newuuid)
octo_str = octo.replace("}", '')
octo_str = octo_str.replace("{", '')
octo_str = octo_str.replace(" ", '')
octo_str = octo_str.replace(":", '')
octo_str = octo_str.replace("'", '')

octo_id = octo_str.split(",")
print(octo_id)

while len(octo_id) > 0:
    PROFILE_ID = octo_id.pop(0)
    CHROME_DRIVER = '/Users/mac/PycharmProjects/check_octo/1/chromedriver'
    LOCAL_API = 'http://localhost:58888/api/profiles'

    def get_webdriver(port):
        chrome_options = Options()
        chrome_options.add_experimental_option('debuggerAddress', f'127.0.0.1:{port}')
        # Change chrome driver path accordingly
        driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)
        return driver


    def get_debug_port(profile_id):
        data = requests.post(
            f'{LOCAL_API}/start', json={'uuid': profile_id, 'headless': False, 'debug_port': True}
        ).json()
        return data['debug_port']


    def main():
        global driver
        global response
        port = get_debug_port(PROFILE_ID)
        driver = get_webdriver(port)
        driver.get('https://www.facebook.com/help/contact/2026068680760273')
        time.sleep(2)
        try:
            # находим 2 чекбокса, жмем на первый
            checkbox = WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "uiInputLabelInput")))
            checkbox[0].click()
            time.sleep(2)

            # жмем на выбрать рекламный аккаунт
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"SupportFormRow"
                                                                                        ".1602434910016280\"]/div["
                                                                                        "2]/div/div/div/a"))).click()
            time.sleep(1)

            #кликаем на первый в списке
            account = WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "__MenuItem")))
            account[1].click()
            time.sleep(2)

            # находим чекбоксы с полиси, жмем на первую причину сверху
            policy = WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "uiInputLabelInput")))
            policy[2].click()
            time.sleep(2)

            # жмем Отправить
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "_4jy1"))).click()
            time.sleep(10)
            print("Tiket success")
            driver.close()
        except Exception as e:
            print(e)
            driver.close()

    if __name__ == '__main__':
        main()

