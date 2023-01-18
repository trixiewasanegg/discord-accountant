import modules
import discord
import sqlite3
from discord.ext import commands

validTransCodes = ""
for trans in modules.types:
    validTransCodes = "\t\t\t" + trans + "\n" + validTransCodes

dbLocn = "mainDB.db"
connection = sqlite3.connect(dbLocn)
cursor = connection.cursor()

TOKEN = modules.varFind("DISCORD_TOKEN")
GUILD = modules.varFind("DISCORD_GUILD")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

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
    _!config VARIABLE VALUE_ - used to configure variables. Call this without any varables to get list that can be configured
    _!rate_ - prints current daily rate and days until payday
    _!summary_ *TYPE* - Gives a summary of either *accounts* or *transactions*
    _!addaccount DESC TYPE BALANCE_ - Adds a new account, type must be either save or spend
    _!transaction_ *FROM TO TYPE DESC AMOUNT* - Actions a transaction, from and to must be the account's IDs (found in !summary)
    Valid transaction codes are: \n""" + validTransCodes
    await ctx.send(output)

@bot.command(name='transaction', help='Will generate a transaction')
async def trans(ctx, take, add, cat, desc, amount):
    if amount == "":
        await ctx.send("Too few arguments")
    else:
        amountInCents = float(amount)*100
        output = modules.transaction(take, add, cat, desc, amountInCents)
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

@bot.command(name='config', help='configures variables')
async def config(ctx, var=0, val=0):
    output = modules.config(var,val)
    await ctx.send(output)

bot.run(TOKEN)