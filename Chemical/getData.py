from crawData import get_chemical_equation

from connetDB import Connect_Collection

import until

elements = []

collection_periodic = Connect_Collection().connect_collect_Periodic_Table()

list_collection = collection_periodic.find()

done_list = ["H2", "He2", "Li", "Be", "B", "C"]

for item_collection in list_collection:

    if item_collection["formula"] in done_list:
        print(item_collection["formula"] + " done")

    else:
        elements.append(item_collection["formula"])



list_substances = []

for item in elements:

    link = "https://cunghocvui.com/phuong-trinh?chat_tham_gia={0}&page=1".format(item)

    print(link)
    print("-------------------------------")

    chemical_equation_list = get_chemical_equation(link)

    for chemical_equation in chemical_equation_list:
        
        if until.check_equation_exists(chemical_equation):
            continue
        else:
            check_equation = until.add_chemical_equation(chemical_equation)
            if check_equation == None:
                print("Add Error Equation")
            else:
                print("Add To Success Equation")
                list_substances = until.get_substance(chemical_equation)

                for substance in list_substances:
                    if until.check_substance_exists(substance):
                        continue
                    else:
                        check_substance = until.add_substance(substance)
                        if check_substance == None:
                            print("Add Error Substance")
                        else:
                            print("Add To Success Substance")

        