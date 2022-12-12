from bs4 import BeautifulSoup
from until import get_equation
import requests


def get_chemical_equation(original_link):
    #original_link = "https://cunghocvui.com/phuong-trinh?chat_tham_gia=H2&page=1"

    req = requests.get(original_link)

    soup = BeautifulSoup(req.text, "html.parser")

    # get all the page links of a substance and add it to the list link_page
    link_page = []
    link_page.append(original_link)

    list_equations = []
    chemical_equation = {}

    page_link = soup.find_all("a",class_ = "page-link")

    for link in page_link:
        item = link.get('href')
        link_page.append(item)

    if len(link_page) > 2:
        link_page = link_page[:len(link_page)-1]

    for link in link_page:
        request = requests.get(url = link)

        soup = BeautifulSoup(request.text, "html.parser")

        print(link)
        print("-------------------------------")

        # get equation 
        list_link_equation = []

        card_deck = soup.find_all("a",class_ = "card card-equation mt-0")

        for card in card_deck:
            item = card.get('href')
            list_link_equation.append(item)     
        

        for link_equation in list_link_equation:
            print(link_equation)
            print("-------------------------------")
            chemical_equation = get_equation(link_equation)
            list_equations.append(chemical_equation)
            

    return list_equations
