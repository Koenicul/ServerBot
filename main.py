from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
load_dotenv()
import os
import db
from sqlalchemy.orm import sessionmaker
import asyncio

Session = sessionmaker(bind=db.engine)
session = Session()

DISCORD_TOKEN = os.getenv("Discord_Token")
PREFIX = os.getenv("Prefix")

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

intents = Intents.all()

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, help_command=help_command, intents=intents)

@bot.command(name="Load", help="Loads a cog")
async def Load(ctx, extention):
    if ctx.author.id == int(os.getenv("Owner_id")):
        await bot.load_extension(f'cogs.{extention}')
        await ctx.send(f'Loaded {extention}')

@bot.command(name="Unload", help="Unloads a cog")
async def Unload(ctx, extention):
    if ctx.author.id == int(os.getenv("Owner_id")):
        await bot.unload_extension(f'cogs.{extention}')
        await ctx.send(f'Unloaded {extention}')

@bot.command(name="Reload", help="Reloads a cog or all cogs")
async def Reload(ctx, extention):
    if ctx.author.id == int(os.getenv("Owner_id")):
        if extention == "all":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    await bot.unload_extension(f'cogs.{filename[:-3]}')
                    await bot.load_extension(f'cogs.{filename[:-3]}')
            return await ctx.send("Reloaded all cogs")
        await bot.unload_extension(f'cogs.{extention}')
        await bot.load_extension(f'cogs.{extention}')
        await ctx.send(f'Reloaded {extention}')

@bot.command(name="Ping", help="Pong!")
async def Ping(ctx):
    for s in session.query(db.Server).all():
        print(s.server_name)
        print(s.server_id)
        print(s.welcome_message_bool)
        print(s.welcome_message)
        print(s.welcome_message_channel)
        print("\n")

async def LoadExtentions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await LoadExtentions()
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())