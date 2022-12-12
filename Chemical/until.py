from bs4 import BeautifulSoup
from connetDB import Connect_Collection

import requests, re

# <------------------------------------------------------------>
def get_link(link):
    list_link =[]

    
    
    return list_link

#<------------------------------------------------------------>
def count_substance(link):
    equation = str(link).split("/phuong-trinh-hoa-hoc/")

    #get substances in the two side:
    two_side = equation[1].split("/")

    #get substances in the left side:
    left_side = two_side[0].split("+")

    return len(left_side)

#<------------------------------------------------------------>
def get_equation(link):

    # count number substance in left side
    number_left_side = count_substance(link = link)

    equation_link = "https://cunghocvui.com" + link

    req = requests.get(equation_link)

    soup = BeautifulSoup(req.text, "html.parser")

    substances = soup.find_all(attrs={"style": "white-space: pre-line;"})

    two_side = []

    for element in substances:  
        two_side.append(element.get_text().strip())

    #-----------------------------------------------------
    # get two side of equation
    left_side = two_side[:number_left_side]
    right_side = two_side[number_left_side:]

    #-----------------------------------------------------
    # get the state of substance

    state_soup = BeautifulSoup(str(soup.find("tr", class_ ="state")),"html.parser")

    state_class = state_soup.find_all("td", class_ ="px-md-2")

    state_list = []

    for item in state_class:
        state_list.append(item.get_text())
    

    #-----------------------------------------------------
    # get the color of substance
    color_soup = BeautifulSoup(str(soup.find("tr", class_ ="color-smell")),"html.parser")

    color_class = color_soup.find_all("td", class_ ="px-md-2")

    color_list = []

    for item in color_class:
        color_list.append(item.get_text())


    #-------------------------------------------------------------   
    # get the condition of substance
    condition_class = soup.find("p", class_ ="condition").get_text()
    condition = ""
    
    if len(condition_class) != 0:
        condition = condition_class.split("Điều kiện: ")[1]


    #-------------------------------------------------------------   
    
    # get classify
    classify = soup.find_all(attrs={"style": "text-decoration: none;"})

    classify_list =[]

    for item in classify:
        classify_list.append(item.get_text())

    #-------------------------------------------------------------   
    chemical_equation = {
        "left_side": left_side, #list
        "right_side": right_side, #list
        "state": state_list, #list
        "color": color_list, #list
        "condition": condition, #string
        "classify": classify_list #list
    }

    return chemical_equation


#<------------------------------------------------------------>
def check_equation_exists(chemical_equation):
    # chemical_equation = {
    #     'left_side': ['2Li ', '2NH3 '], 
    #     'right_side': ['H2 ', '2LiNH2 '], 
    #     'state': ['rắn', 'khí', 'khí', 'lỏng'], 
    #     'color': ['trắng bạc', 'không màu', 'không màu', 'trắng'], 
    #     'condition': 'Nhiệt độ: 400°C', 
    #     'classify': ['Phản ứng oxi-hoá khử']
    #     }

    collection_equation = Connect_Collection().connect_collect_Chemical_Equation()

    my_query = {
        "left_side": chemical_equation["left_side"],
        "right_side": chemical_equation["right_side"]
    }

    check = collection_equation.find_one(my_query)

    if check != None:
        # is exists
        return True
    else:
        #not exists
        return False  


#<------------------------------------------------------------>
def get_substance(chemical_equation):

    # chemical_equation = {
    #     'left_side': ['2Li ', '2NH3 '], 
    #     'right_side': ['H2 ', '2LiNH2 '], 
    #     'state': ['rắn', 'khí', 'khí', 'lỏng'], 
    #     'color': ['trắng bạc', 'không màu', 'không màu', 'trắng'], 
    #     'condition': 'Nhiệt độ: 400°C', 
    #     'classify': ['Phản ứng oxi-hoá khử']
    #     }

    equation = chemical_equation['left_side'] + chemical_equation['right_side']

    list_substances = []

    for index in range(len(equation)):
        
        location = re.search(r"^[1-9]*",equation[index]).span()
        formula = equation[index][location[1]:]

        substance = {
            "formula": formula.strip(),
            "state": chemical_equation['state'][index],
            "color": chemical_equation['color'][index],
        }

        list_substances.append(substance)

    return list_substances
    

#<------------------------------------------------------------>
def check_substance_exists(substance):

    collection_periodic_table = Connect_Collection().connect_collect_Periodic_Table()
    collection_compounds_table = Connect_Collection().connect_collect_Compounds_Table()

    my_query = {
        "formula": substance["formula"]
    }

    check_periodic = collection_periodic_table.find_one(my_query)
    check_compounds = collection_compounds_table.find_one(my_query)

    if check_periodic == None and check_compounds == None:
        # not exists
        return False
    else:
        # is exists
        return True


#<------------------------------------------------------------>
def add_chemical_equation(chemical_equation):

    collection_equation = Connect_Collection().connect_collect_Chemical_Equation()

    check = collection_equation.insert_one(chemical_equation)

    return check


#<------------------------------------------------------------>
def add_substance(substance):
    
    collection_compounds_table = Connect_Collection().connect_collect_Compounds_Table()

    check = collection_compounds_table.insert_one(substance)
    
    return check


