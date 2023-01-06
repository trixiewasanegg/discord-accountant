import sqlite3
import datetime

variable = []
variableVal = []

types = ["payroll", "transfer", "food", "transport", "rent", "gift", "frivolous", "misc"]

config = open("variables.config", "r")
for line in config:
    split = line.split(':')
    variable.append(split[0])
    variableVal.append(split[1])
config.close()

dbLocn = variableVal[variable.index('DATABASE')]
connection = sqlite3.connect(dbLocn)
cursor = connection.cursor()

#Generates Timestamp
def timestamp():
    dateTimeObj = datetime.datetime.now()
    timecode = dateTimeObj.strftime("%Y-%m-%d_%H%M%S")
    return timecode

#Documents transactions
def document(array):
    #Finds LogFile Location from config file and opens it
    logfile = variableVal[variable.index('LOGFILE')]
    log = open(logfile, "a")
    #runs through array and appends new lines
    for trans in array:
        line = timestamp() + " - " + trans + "\n"
        log.write(line)
    log.close()

#Calculates days left in entitlement period
def daysLeft():
    #Defines first ever date of pay cycle with Probe
    startDate = datetime.date(2020, 12, 9)

    #Gets today's date
    current = datetime.date.today()
    
    #Gets difference in days
    delta = (current - startDate).days

    #Gets remainder after dividing by 14 then gets remainder
    modulo = delta % 14
    remain = 14-modulo

    return remain

#Calculates current day
def currToday():
    #Defines first ever date of pay cycle with Probe
    startDate = datetime.date(2020, 12, 9)

    #Gets today's date
    current = datetime.date.today()
    
    #Gets difference in days
    delta = (current - startDate).days

    return delta

#Calculates current daily rate
def currRateCalc():
    transactions = []
    #runs SQL query against database, gets values of all spending accounts
    command = "SELECT \"balance\" FROM  \"accTable\" WHERE \"type\" LIKE \'%spend%\'"
    transactions.append(command)
    query = cursor.execute(command).fetchall()

    #runs through result of query, adding them all together (had to do it this way bc query returns tuples)
    funds = 0
    for item in query:
        funds = funds + int(item[0])
    
    #calculates daily rate
    rate = funds / daysLeft()
    rateInDol = rate/100
    document(transactions)
    return rateInDol

#Records Transaction
def transaction(take, add, cat, amount):
    #defines empty array to write to transactions
    transactions = []
    transType = ""

    if cat in types:    
        #checks if take accID is 99, if so it skips
        if str(take) != str(99):
            #gets account desc for later
            command = "SELECT \"description\" FROM \"accTable\" WHERE \"ID\" = " + str(take)
            transactions.append(command)
            query = cursor.execute(command).fetchall()
            tmp = query[0]
            takeAccountDesc = tmp[0]  

            #Gets current accounts balance
            command = "SELECT \"balance\" FROM \"accTable\" WHERE \"ID\" = " + str(take)
            transactions.append(command)
            query = cursor.execute(command).fetchall()
            tmp = query[0]
            takeInBalance = tmp[0]
            
            #determines new account balance
            takeOutBalance = int(takeInBalance) - int(amount)

            #Generates SQL command, appends transactions and then executes
            command = "UPDATE \"accTable\" SET \"balance\" = '" + str(takeOutBalance) + "' WHERE \"id\" = " + str(take)
            transactions.append(command)
            cursor.execute(command)
        else:
            takeInBalance = 0
            takeOutBalance = 0
            transType = "deposit"
        
        #checks if add accID is 99, if so it skips
        if str(add) != str(99):
            #gets account desc for later
            command = "SELECT \"description\" FROM \"accTable\" WHERE \"ID\" = " + str(add)
            transactions.append(command)
            query = cursor.execute(command).fetchall()
            tmp = query[0]
            addAccountDesc = tmp[0]        
            
            #gets current account balance
            command = "SELECT \"balance\" FROM \"accTable\" WHERE \"ID\" = " + str(add)
            transactions.append(command)
            query = cursor.execute(command).fetchall()
            tmp = query[0]
            addInBalance = tmp[0]

            #determines new account balance
            addOutBalance = int(addInBalance) + int(amount)
            
            #Generates SQL command, appends transactions and then executes
            command = "UPDATE \"accTable\" SET \"balance\" = '" + str(addOutBalance) + "' WHERE \"id\" = " + str(add)
            transactions.append(command)
            cursor.execute(command)
        else:
            addInBalance = 0
            addOutBalance = 0
            transType = "spend"

        #gets today's date code
        today = currToday()

        # generates SQL command to insert to transactionTable, appends transactions[], then executes
        # TL;DR: this fuck off long command pulls the variables from the previous 20 fucking lines and appends them all.
        # I know this command isn't rly human readable, eat my ass
        command = "INSERT INTO  \"transactionTable\" (\"sen\", \"rec\", \"type\", \"amount\", \"date\", \"fromBefore\", \"toBefore\", \"fromAfter\", \"toAfter\") VALUES ('" + str(take) + "', '" + str(add) + "', '" + str(cat) + "', '" + str(amount) + "', '" + str(today) + "', '" + str(takeInBalance) + "', '" + str(addInBalance) + "', '" + str(takeOutBalance) + "', '" + str(addOutBalance) + "');"
        transactions.append(command)
        cursor.execute(command)

        #appends log file with all transactions executed during this function
        document(transactions)

        #commits changes to database
        connection.commit()

        rate = currRateCalc()
        remaining = daysLeft()

        #Generates human readable output 
        if transType == "":
            output = """Actioned Successfully. Summary below:
                Transfer FROM = """ + str(takeAccountDesc) + """
                    Balance before = $""" + str(takeInBalance/100) + """
                    Balance after = $""" + str(takeOutBalance/100) + """
                Transfer TO = """ + str(addAccountDesc) + """
                    Balance before = $""" + str(addInBalance/100) + """
                    Balance after = $""" + str(addOutBalance/100) + """
                Your current daily rate is $""" + str(rate) + """ with """ + str(remaining) + """ days left"""
        elif transType == "spend":
            output = """Actioned Successfully. Summary below:
                Spent FROM = """ + str(takeAccountDesc) + """
                    Balance before = $""" + str(takeInBalance/100) + """
                    Balance after = $""" + str(takeOutBalance/100) + """
                Your current daily rate is $""" + str(rate) + """ with """ + str(remaining) + """ days left"""
        elif transType == "deposit":
            output = """Actioned Successfully. Summary below:
                Deposited TO = """ + str(addAccountDesc) + """
                    Balance before = $""" + str(addInBalance/100) + """
                    Balance after = $""" + str(addOutBalance/100) + """
                Your current daily rate is $""" + str(rate) + """ with """ + str(remaining) + """ days left"""
        else:
            output = "An error occurred, check logs"

    else:
        output = "Catagory not recognised, valid responses are " + types
    return output

#Generates summary
def summaryGen(cat="accounts"):
    transactions = []
    rate = currRateCalc()
    days = daysLeft()
    output = "Your current daily rate is $" + str(rate) + " with " + str(days) + " days left. \n"
    if cat == "accounts":
        command = "SELECT * FROM  \"accTable\""
        transactions.append(command)
        query = cursor.execute(command).fetchall()
        tmp = cursor.description
        tmp2 = []
        for row in tmp:
            tmp2.append(row[0])
        idInx = tmp2.index('id')
        descInx = tmp2.index('description')
        typeInx = tmp2.index('type')
        balInx = tmp2.index('balance')
        for item in query:
                key = item[idInx]
                desc = item[descInx]
                typ = item[typeInx]
                bal = item[balInx]
                append = "Account " + str(desc) + " (" + str(typ) + ", ID = " + str(key) + ") is currently at $" + str(bal/100)
                output = output + append  + "\n"
    elif cat == "transactions":
        limit = currToday()-(14+daysLeft())
        for item in types:
            command = "SELECT \"amount\" FROM  \"transactionTable\" WHERE (\"date\" > '" + str(limit) + "') AND (\"type\" LIKE '%" + item + "%');"
            transactions.append(command)
            query = cursor.execute(command).fetchall()
            itemspend = 0
            count = 0
            for subitem in query:
                itemspend = itemspend + int(subitem[0])
                count = count + 1
            output = output + "Spending so far on " + str(item) + " is $" + str(itemspend/100) + " in " + str(count) + " transactions.\n"
        command = "SELECT COUNT(*) FROM  \"transactionTable\" WHERE (\"date\" > '" + str(limit) + "');"
        transactions.append(command)
        query = cursor.execute(command).fetchall()
        transquickTotal = query[0]
        transTotal = transquickTotal[0]
        output = output + "You have executed " + str(transTotal) + " transactions this period. \n"
    return output

def addAccount(desc, typ, balance):
    transactions = []
    balInCent = float(balance) * 100
    command = "INSERT INTO  \"accTable\" (\"type\", \"balance\", \"description\") VALUES ('" + str(typ) + "', '" + str(balInCent) + "', '" + desc + "')"
    transactions.append(command)
    cursor.execute(command)
    connection.commit()

    command = "SELECT id FROM  \"accTable\" WHERE \"description\" LIKE '" + desc + "'"
    transactions.append(command)
    id = cursor.execute(command).fetchall()
    count = id[0]
    output = "Generated new account " + str(desc) + " of ID " + str(count[0]) + ". Balance = $" + str(balance) + "."
    return output