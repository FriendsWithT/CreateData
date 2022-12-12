from connetDB import Connect_Collection
from bs4 import BeautifulSoup
from until import get_equation
import requests

link = "https://cunghocvui.com/phuong-trinh?chat_tham_gia=K&page=1"

req = requests.get(link)

soup = BeautifulSoup(req.text, "html.parser")

# get all the page links of a substance and add it to the list link_page
link_page = []
link_page.append(link)

list_equations = []
chemical_equation = {}

page_link = soup.find_all("a",class_ = "page-link")

for link in page_link:
    item = link.get('href')
    link_page.append(item)

if len(link_page) > 2:
    link_page = link_page[:len(link_page)-1]

for link_item in link_page:
    print(link_item)
