import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from codeforces import *
import pymongo

load_dotenv()
token = os.getenv('BOT_TOKEN')
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
dataBase = mongoClient["codeloopContestants"]
username = dataBase["usernames"]

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.command(name='handle')
async def respond(ctx, inst: str, value: str = 0):
    if inst == "add":
        query = {"discordUsername": ctx.message.author.name}
        query = username.find(query)
        lent = 0
        lk = ""
        for _ in query:
            lk = _
            print(_)
            lent += 1
        print(lent)
        if lent != 0:
            username.delete_one(lk)
        x = {"discordUsername": ctx.message.author.name, "codeforcesUsername": value}
        username.insert_one(x)
        await ctx.send(ctx.message.author.name + " : " + value)
    if inst == "list":
        allUser = username.find()
        for user in allUser:
            await ctx.send(user["discordUsername"] + " : " + user["codeforcesUsername"])

@bot.command(name='match')
async def challengeGenerate(ctx, challengee: str, baseRating: int):
    challengerName=ctx.message.author.name
    challengeeName=challengee
    challengerCFUsername=''
    query={'discordUsername':challengerName}
    query=username.find_one(query)
    challengerCFUsername=query['codeforcesUsername']
    challengeeCFUsername=''
    query={'discordUsername':challengeeName}
    query=username.find_one(query)
    challengeeCFUsername=query['codeforcesUsername']
    print(challengerCFUsername)
    print(challengeeCFUsername)
    await ctx.send(challengerCFUsername + ' has Challenged ' + challengeeCFUsername)
    challengeProblems=generateChallenge(challengerCFUsername, challengeeCFUsername, baseRating)
    for problem in challengeProblems:
        await ctx.send('https://codeforces.com/contest/'+problem[:-1]+'/problem/'+problem[-1:-2:-1]+'/')
bot.run(token)
