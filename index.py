from bs4 import BeautifulSoup
import requests
import html5lib
import lxml

url = "https://multimedia.scmp.com/widgets/china/wuhanvirus/"
url1 = "https://interactive-static.scmp.com/sheet/wuhan/viruscases.json"

page = requests.get(url)
viruscases = requests.get(url1)

print(page.status_code)
print(viruscases.status_code)

soup = BeautifulSoup(page.text, "html5lib")

# print(soup)
