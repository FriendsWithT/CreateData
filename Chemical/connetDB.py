from pymongo import MongoClient
from pymongo.database import Database

class Connect:
    def connect():
        client = MongoClient("mongodb+srv://thanhthan:Thanhthan1@cluster0.yp1bmpd.mongodb.net/?retryWrites=true&w=majority")
        # get database Chemical
        db : Database = client.get_database("Chemical")
        return db

class Connect_Collection(Connect):
    def __init__(self):
        self.conn : Database = Connect.connect()
    
    # connect collecttion Periodic_Table
    def connect_collect_Periodic_Table(self):
        collect = self.conn.get_collection("Periodic_Table")
        return collect
    # connect collecttion Chemical_Equation
    def connect_collect_Chemical_Equation(self):
        collect = self.conn.get_collection("Chemical_Equation")
        return collect

    # connect collecttion Compounds_Table
    def connect_collect_Compounds_Table(self):
        collect = self.conn.get_collection("Compounds_Table")
        return collect