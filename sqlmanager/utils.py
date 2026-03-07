class Utils:
    def populateList(self, list, callback):
        for item in list:
            callback(item)

    def sql2pythonTypes(self, text):
        if text == "INTEGER":
            return int
        elif text == "TEXT":
            return str
        elif text == "REAL":
            return float
        elif text == "BLOB":
            return bytes
        
    def python2sqlTypes(self, text):
        if text == int or text == bool:
            return "INTEGER"
        elif text == str:
            return "TEXT"
        elif text == float:
            return "REAL"
        else:
            return "BLOB"