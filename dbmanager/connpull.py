import sqlite3
import queue
from contextlib import contextmanager

class ConnectionPull:
    def __init__(self, database, max_connections=6):
        self.max_connections = max_connections
        self.database = database
        self.q = queue.Queue()

        for i in range(max_connections):
            tempcon = self.createConnection(database)
            self.q.put(tempcon)



    def createConnection(self, dbname):
        con = sqlite3.connect(dbname, check_same_thread=False)
        return con
    
    def checkConnValidity(self, conn):
        try: 
            conn.execute("SELECT 1")
            return conn
        except:
            return None
    
    def retrieveConnection(self, timeout):
        try:
            return self.q.get(timeout=timeout)
        except queue.Empty:
            raise RuntimeError("Error: no connections left in the pool!")
    @contextmanager
    def getConnection(self):
        try:
            conn = self.retrieveConnection(0.1)
            yield conn
        finally:
            if not self.checkConnValidity(conn):
                conn.close()
                self.q.put(self.createConnection(self.database))
            else:
                conn.rollback()
                self.q.put(conn)
        