from dbmanager import Database, Table, Column

#connect to database
db = Database("example.db")

#create table if doesn't exist 
if not db.tableExists("extable"):
    columns = (
        Column("col1", int),
        Column("col2", str)
    )
    db.createTable("extable", columns)

#table variable
exampleTable = Table("extable", db)

#add record into table if doesn't exist
if not exampleTable.getValues("col1", 1):   #(first column here acts like a primary key)
    row = [1, "hello"]
    exampleTable.insertValues(row)

print(exampleTable.getValues("col1", 1))    #(always returns a list)
