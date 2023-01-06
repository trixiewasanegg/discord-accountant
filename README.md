# discord-accountant-lol
Yep... it's a discord accountant... fight me

## **Dependencies:** 
> - discord.py
> - SQLite...
> suprised there isn't more but i'm just that good.

**TL;DR:**
Brief summary of each command:
```
!rate - prints current daily rate and days until payday

!summary *TYPE* - Gives a summary of either *accounts* or *transactions*

!addaccount DESC TYPE BALANCE - Adds a new account, type must be either save or spend

!transaction *FROM TO TYPE AMOUNT* - Actions a transaction, from and to must be the account's IDs (found in !summary)

Valid transaction codes are: 
["payroll", "transfer", "food", "transport", "rent", "gift", "frivolous", "misc"]
```

Basically, it runs off the concept of a daily rate - you have $X to spend today.

Why this way? I have ADHD and can't think "okay, i have $200 to last me 3 days" i need to break it down by day and have it easily accessable so... discord

## **Configuration:**

sample.config gives an idea of what your config file should be. Copy and paste it as variable.config for all the files to read.

You will need a SQLite database stored at mainDB.db with the following tables:

### accTable; for storing accounts:
```
id - primary key
description - human readable description for the account
type - **must be either save or spend**
balance - self explanatory, will be stored in cents bc fuck floating points
```

### transactionTable; for storing transactions:
```
id - primary key
from - the account being deducted
to - the account being added
type - see transaction codes
amount - the amount
date - days since I started at my workplace, bc it's easier for me to calculate
fromBefore - balance before transaction
toBefore - see fromBefore
fromAfter - balance after transaction
toAfter - balance after transaction
```

### Example table creation transactions
```
CREATE TABLE transactionTable (
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
;
```

```
CREATE TABLE accTable 
    (id INTEGER PRIMARY KEY,
    description TEXT,
    type TEXT,
    balance INTEGER)
;
```

## Changelog
v1.0 - trixiewasanegg - Initial Release\
v1.01 - trixiewasanegg - Fixed issue with columns during creation, documented table creation

TO DO:

build table creation into initial runs