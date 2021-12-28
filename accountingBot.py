import modules
from discord.ext import commands

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

TOKEN = variableVal[variable.index('DISCORD_TOKEN')]
GUILD = variableVal[variable.index('DISCORD_GUILD')]

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected.'
    )

@bot.command(name='accountinghelp', help='Detailed Help Text')
async def help(ctx):
    output = """Brief summary of each command:
    _!rate_ - prints current daily rate and days until payday
    _!summary_ *TYPE* - Gives a summary of either *accounts* or *transactions*
    _!addaccount DESC TYPE BALANCE_ - Adds a new account, type must be either save or spend
    _!transaction_ *FROM TO TYPE AMOUNT* - Actions a transaction, from and to must be the account's IDs (found in !summary)
    Valid transaction codes are: \n""" + validTransCodes
    await ctx.send(output)

@bot.command(name='transaction', help='Will generate a transaction')
async def trans(ctx, take, add, cat, amount):
    if amount == "":
        await ctx.send("Too few arguments")
    else:
        amountInCents = float(amount)*100
        output = modules.transaction(take, add, cat, amountInCents)
        await ctx.send(output)

@bot.command(name='summary', help='Gives a summary of either *accounts* or *transactions*')
async def summary(ctx, type="accounts"):
    output = modules.summaryGen(type)
    await ctx.send(output)

@bot.command(name='rate', help='Gives a summary of your daily rate')
async def rate(ctx):
    rate = modules.currRateCalc()
    days = modules.daysLeft()

    output = "Your daily rate is $" + str(rate) + " with " + str(days) + " days left."

    await ctx.send(output)

@bot.command(name='addaccount', help='adds new account')
async def addacc(ctx, desc, typ, balance):
    output = modules.addAccount(desc, typ, balance)
    await ctx.send(output)

bot.run(TOKEN)