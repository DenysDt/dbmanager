from .connpull import ConnectionPull
from .models import Column
from .utils import Utils

class Database:
    def __init__(self, database, max_connections=6):
        self.database = database
        self.ConnectionPool = ConnectionPull(database, max_connections)
        self.Utils = Utils()

    def queryExec(self, query, args=()):
        output = ""
        with self.ConnectionPool.getConnection() as con:
            try:
                cursor = con.cursor()
                
                cursor.execute(query, args)
        
                con.commit()
                output = cursor.fetchall()
                if output == []:
                    return None
                else:
                    return output
            except Exception as e:
                con.rollback()
                raise e
            finally:
                cursor.close()


        
        
    def getTableNames(self):
        try:
            query = f"SELECT name FROM sqlite_master WHERE type='table'"
            resp = self.queryExec(query)
            return resp
        except Exception:
            return None
        

    def tableExists(self, tablename):
        tables = self.getTableNames()
        if not tables:
            return False
        if tablename in tables:
            return True
        else:
            return False

    def dropTable(self, tablename):
        try:
            self.queryExec(f"DROP TABLE {tablename}")
            return True, None
        except Exception as e:
            return False, str(e)

    
            


    def createTable(self, tablename, columns):
        itemslist = []

        for item in columns:
            type = self.Utils.python2sqlTypes(item.type)
            itemslist.append(f"{item.name} {type}")

        qrows = ", ".join(itemslist)

        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tablename}'; "
        res = self.queryExec(query)
        if res:
            return False, "table already exists"
        else:
            try: 
                query = f"CREATE TABLE {tablename} ({qrows});"
                self.queryExec(query)
                return True, None
            except Exception as e:
                return False, str(e)
