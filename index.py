import json
from os import getenv
from pathlib import Path
from time import sleep

import lxml
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver

basedir = Path.cwd()
dotenv_path = basedir.joinpath(".env")
dump_path = basedir.joinpath("dumps/")

if not Path.exists(dump_path):
    dump_path.mkdir(exist_ok=True)

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
sleep(15)

page = driver.page_source
driver.quit()

requested_cases = requests.get(viruscases_url)
viruscases = requested_cases.json()
entries = viruscases["entries"]

total_cases = 0
total_deceased = 0
total_recovered = 0

for entry in entries:
    total_cases += int(entry["cases"].replace(",", ""))
    total_deceased += int(entry["deaths"].replace(",", ""))
    total_recovered += int(entry["recovered"].replace(",", ""))

total = total_cases, total_deceased, total_recovered
viruscases["summary"] = {
    "total cases": total_cases,
    "total deceased": total_deceased,
    "total recovered": total_recovered,
}

print("Total cases: {}, Totally deceased: {}, Totally recovered: {}".format(*total))
print("[LOG] Request status: %s" % requested_cases.status_code)

with open(dump_path.joinpath("viruscases.json"), "w") as outfile:
    json.dump(viruscases, outfile, indent=4)

soup = BeautifulSoup(page, "lxml")
with open(dump_path.joinpath("wuhanvirus.html"), "w", encoding="utf-8") as outfile:
    outfile.write(str(soup))
