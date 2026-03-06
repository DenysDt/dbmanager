from .connpull import ConnectionPull
from .models import Column

class Database:
    def __init__(self, database, max_connections=6):
        self.database = database
        self.ConnectionPool = ConnectionPull(database, max_connections)

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
        

    def dropTable(self, tablename):
        try:
            self.queryExec(f"DROP TABLE {tablename}")
            return True, None
        except Exception as e:
            return False, str(e)

    
            


    def createTable(self, tablename, rows):
        itemslist = []

        for item in rows:
            if item.type == int or item.type == bool:
                type = "INTEGER"
            elif item.type == str:
                type = "TEXT"
            elif item.type == float:
                type = "REAL"
            else:
                type = "BLOB"
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
