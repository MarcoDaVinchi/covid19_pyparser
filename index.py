import gzip
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


def convert_case_entry(entry, entrykey):
    """[summary]
    Convert entry from comma separated string to integer.
    ( "111,111" -> 111111)
    Used to count summary statistics.
    Args:
        entry ([list])
        entrykey ([str]): key to which is this entry referred.
        e.g. "cases","deaths","recovered"
    Returns:
        [int]: converted integer.
    """
    try:
        converted_entry = int(entry[entrykey].replace(",", ""))
    except Exception as e:
        print(
            "[EXCEPTION] There is wrong value in entry {} {}".format(
                entry["country"], entrykey, entry[entrykey]
            ),
            e,
        )
        converted_entry = 0
    return converted_entry


for entry in entries:
    total_cases += convert_case_entry(entry, "cases")
    total_deceased += convert_case_entry(entry, "deaths")
    total_recovered += convert_case_entry(entry, "recovered")

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

with gzip.GzipFile(dump_path.joinpath("viruscases.gz"), "wb") as f:
    f.write(json.dumps(viruscases).encode("utf-8"))

soup = BeautifulSoup(page, "lxml")
with open(dump_path.joinpath("wuhanvirus.html"), "w", encoding="utf-8") as outfile:
    outfile.write(str(soup))

with gzip.open(dump_path.joinpath("viruscases.gz"), "rb") as f:
    unzipped = f.read()

unzipped_json = json.loads(unzipped)
print("FIN!")
