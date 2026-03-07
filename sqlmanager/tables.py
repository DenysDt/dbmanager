from .database import Database
from .models import Column
from .utils import Utils

class Table:
    def __init__(self, tablename, database):
        self.tablename = tablename
        self.database = database
        self.Utils = Utils()

    def getValues(self, searchName, searchCriteria):
        try:
            query = f"SELECT * FROM {self.tablename} WHERE {searchName}=?"
            resp = self.database.queryExec(query, (searchCriteria,))
            return resp
        except Exception:
            return None
        
    def getAllTableValues(self):
        try:
            query = f"SELECT * FROM {self.tablename}"
            resp = self.database.queryExec(query)
            return resp
        except Exception:
            return None
        
    def getTableColumns(self):
        pragmareturn = self.database.queryExec(f"PRAGMA table_info({self.tablename});")

        if not pragmareturn:
            return None
            
        datanames = []
        for namestuple in pragmareturn:
            datanames.append(Column(namestuple[1], self.Utils.sql2pythonTypes(namestuple[2])))
        return datanames
    
    def dropColumn(self, c):
        if isinstance(c, Column):
            name = c.name
        else:
            name = c
        try:
            self.database.queryExec(f"ALTER TABLE {self.tablename} DROP COLUMN {name}")
        except Exception as e:
            return False, str(e)
            
    def addColumn(self, c):
        try:
            self.database.queryExec(f"ALTER TABLE {self.tablename} ADD {c.name} {c.type}")
        except Exception as e:
            return False, str(e)

    
    def deleteRow(self, searchName, searchCriteria):
        try:
            self.database.queryExec(f"DELETE FROM {self.tablename} WHERE {searchName}=?", (searchCriteria,))
            return True, None
        except Exception as e:
            return False, str(e)
        
    def insertValues(self, data):
        try:
            datanames = self.getTableColumns()

            if not datanames:
                return False, "database doesn't exist"

            if len(data) != len(datanames):
                return False, "incorrect amount of values"

            nameslist = []
            for item in datanames:
                nameslist.append(item.name)
            names = ", ".join(nameslist)

            values = ", ".join(["?"] * len(data))

            query = f"INSERT INTO {self.tablename} ({names}) VALUES ({values})"
            
            self.database.queryExec(query, data)
            return True, None
            
        except Exception as e:
            return False, str(e)
        
    
