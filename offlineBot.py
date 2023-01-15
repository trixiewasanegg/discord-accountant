import modules

validTransCodes = ""
for trans in modules.types:
    validTransCodes = "\t\t\t" + trans + "\n" + validTransCodes

variable = []
variableVal = []

config = open("variables.config", "r")
for line in config:
    split = line.split(':')
    variable.append(split[0])
    variableVal.append(split[1])
config.close()

while True:
    command = input("Command: ")
    com = command.split(" ")

    transac = com[0]

    if transac == "accountinghelp":
            output = """Brief summary of each command:
    _!config VARIABLE VALUE_ - used to configure variables. Call this without any varables to get list of variables
    _!rate_ - prints current daily rate and days until payday
    _!summary_ *TYPE* - Gives a summary of either *accounts* or *transactions*
    _!addaccount DESC TYPE BALANCE_ - Adds a new account, type must be either save or spend
    _!transaction_ *FROM TO TYPE AMOUNT* - Actions a transaction, from and to must be the account's IDs (found in !summary)
    Valid transaction codes are: \n""" + validTransCodes

    if transac == "transaction":
        try:
            take = com[1]
            add = com[2]
            cat = com[3]
            amount = float(amount)*100
            output = modules.transaction(take, add, cat, amount)
        except:
            output = "too few variables"
    
    if transac == "summary":
        try:
            type = com[1]
        except:
            type = "accounts"
        
        output = modules.summaryGen(type)

    if transac == "rate":
        rate = modules.currRateCalc()
        days = modules.daysLeft()

        output = "Your daily rate is $" + str(rate) + " with " + str(days) + " days left."

    if transac == "addacc":
        desc = com[1]
        typ = com[2]
        balance = com[3]

        output = modules.addAccount(desc, typ, balance)
    
    if transac == "config":
        try:
            var = com[1]
            val = com[2]
        except:
            var = 0
            val = 0
        output = modules.config(var,val)

    if transac == "exit":
        break

    print(output)