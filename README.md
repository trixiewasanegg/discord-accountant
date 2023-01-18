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

!transaction *FROM TO TYPE DESC AMOUNT* - Actions a transaction, from and to must be the account's IDs (found in !summary)

Valid transaction codes are: 
["payroll", "transfer", "food", "transport", "rent", "gift", "frivolous", "services", "misc"]
```

Basically, it runs off the concept of a daily rate - you have $X to spend today.

Why this way? I have ADHD and can't think "okay, i have $200 to last me 3 days" i need to break it down by day and have it easily accessable so... discord

## **Configuration:**

Get your discord bot's token ready & the guild you wish to run it in. You can find this in the [Discord Developer Portal](https://discord.com/developers/applications)

The setup script will configure everything for you, just follow the prompts.

## **Table Documentation:**

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
desc - description of the calculation
date - days since Mon 01/01/2018,,,, that starting date works for me shut up and fight me
fromBefore - balance before transaction
toBefore - see fromBefore
fromAfter - balance after transaction
toAfter - balance after transaction
```

### varTable; for storing variables:
```
variable - variable to configure
value - value of variable
```

## Changelog
v1.0 - trixiewasanegg - Initial Release\
v1.01 - trixiewasanegg - Fixed issue with columns during creation, documented table creation\
v1.02 - trixiewasanegg - updated to fix broken discord.py update\
v1.1 - trixiewasanegg - added functionality to allow for different paydays & pay period, removed requirement for variables.config and stored variables in the sqlite DB which makes so much more sense in hindsight but -.-, built setup.py\
v1.11 - trixiewasanegg - updated documentation, added description column