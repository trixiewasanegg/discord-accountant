import sqlite3
import os

# Introduction
print("Discord Accountant - Config Script")
print("This software is available under the MIT License and is provided without warranty, to the extent permitted by law.")
print("This script should be run in the working directory.")

transactions = []

transactions.append("""CREATE TABLE transactionTable (
    id INTEGER PRIMARY KEY,
    sen TEXT,
    rec TEXT,
    type TEXT,
    amount INTEGER,
    date INTEGER,
    fromBefore INTEGER,
    toBefore INTEGER,
    fromAfter INTEGER,
    toAfter INTEGER)
;""")
transactions.append("""CREATE TABLE accTable (
    id INTEGER PRIMARY KEY,
    description TEXT,
    type TEXT,
    balance INTEGER)
;""")
transactions.append("""CREATE TABLE varTable (
    variable TEXT,
    value TEXT)
;""")

variables = ["DISCORD_TOKEN", "DISCORD_GUILD", "LOGFILE", "PAYPERIOD", "OFFSET"]

dbName = "mainDB.db"

if os.path.exists(dbName) == False:
    os.system("touch " + dbName)
    print(dbName + " created.")
else:
    print(dbName + " already exists")

#opens mainDB.db file
connection = sqlite3.connect(dbName)
cursor = connection.cursor()
print("Connected to " + dbName + " database")

for trans in transactions:
    try:
        cursor.execute(trans)
        print(trans)
    except:
        print("Transaction failed:\n" + trans)

for var in variables:
    val = input("Please define " + var + ":\n")
    command = "INSERT INTO \'varTable\' (\'variable\', \'value\') VALUES (\'" + var + "\', \'" + val + "\');"
    print(command)
    print(cursor.execute(command))

connection.commit()
print("Setup complete.")