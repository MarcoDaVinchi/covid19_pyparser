from bs4 import BeautifulSoup
import requests
import html5lib
import lxml

url = "https://multimedia.scmp.com/widgets/china/wuhanvirus/"

page = requests.get(url)

print(page.status_code)

soup = BeautifulSoup(page.text, "html5lib")

print(soup)
