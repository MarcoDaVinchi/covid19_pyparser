import json
from pathlib import Path
from time import sleep
from os import getenv

import html5lib
import lxml
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

basedir = Path.cwd()
dotenv_path = basedir.joinpath(".env")

if Path.exists(dotenv_path):
    load_dotenv(dotenv_path)

webdrivers_path = getenv("WEB_DRIVER")

webdriver_chrome_path = basedir.joinpath(webdrivers_path).resolve()
options = webdriver.ChromeOptions()
options.add_argument("headless")

url = "https://multimedia.scmp.com/widgets/china/wuhanvirus/"
viruscases_url = "https://interactive-static.scmp.com/sheet/wuhan/viruscases.json"

driver = webdriver.Chrome(executable_path=webdriver_chrome_path, options=options)
driver.get(url)
sleep(10)
# WebDriverWait(driver, timeout=10).until(lambda d: d.find_element_by_id("lastupdated"))

page = driver.page_source
driver.quit()

viruscases = requests.get(viruscases_url).json()

# print(page)
print('[LOG]Request status: %s' % requests.get(viruscases_url).status_code)
# print(viruscases)

with open(basedir.joinpath("viruscases.json"), "w") as outfile:
    json.dump(viruscases, outfile, indent=4)

soup = BeautifulSoup(page, "lxml")

# print(soup)

# total_cases = soup.find("div", class_="box cases")
