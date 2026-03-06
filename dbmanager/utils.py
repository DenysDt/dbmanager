class Utils:
    def populateList(self, list, callback):
        for item in list:
            callback(item)

    def sql2PythonTypes(self, text):
        if text == "INTEGER":
            return int
        elif text == "TEXT":
            return str
        elif text == "REAL":
            return float
        elif text == "BLOB":
            return bytes