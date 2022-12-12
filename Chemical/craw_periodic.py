from bs4 import BeautifulSoup

from connetDB import Connect_Collection

import requests, re

link = "https://en.wikipedia.org/wiki/List_of_chemical_elements"

req = requests.get(link)

soup = BeautifulSoup(req.text, "html.parser")

substances = soup.find_all("tr", class_ = "anchor")


for element in substances:      
    element_soup = BeautifulSoup(str(element),"html.parser")

    # get the symbol of element
    symbol = element_soup.tr["id"]


    state_list =["solid", "gas", "liquid", "unknown phase"]
    index = 0

    state = None

    while state == None:
        state = element_soup.find(string=re.compile(str(state_list[index])))
        index = index + 1
    state = state.strip()

    if state == "gas":
        formula = str(symbol) + "2"
    else:
        formula = str(symbol)

    if state == "solid":
        state = "rắn"

    elif state == "gas":
        state = "khí"
    
    elif state == "liquid":
        state = "lỏng"
    else:
        state = "không xác định"

    print(symbol)
    print(state)
    print(formula)
    substance_element = {
        "symbol" : symbol,
        "formula" : formula,
        "state" : state     
    }
    
    collection_periodic = Connect_Collection().connect_collect_Periodic_Table()

    check = collection_periodic.insert_one(substance_element)

    if check != None:
        print("Done")

    print("--------------------")