from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
load_dotenv()
import os
import db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()

DISCORD_TOKEN = os.getenv("Discord_Token")
PREFIX = os.getenv("Prefix")

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, help_command=help_command, intents=intents)

@bot.command(name="Load", help="Loads a cog")
async def Load(ctx, extention):
    if ctx.author.id == os.getenv("Owner_id"):
        bot.load_extension(f'cogs.{extention}')
        await ctx.send(f'Loaded {extention}')

@bot.command(name="Unload", help="Unloads a cog")
async def Unload(ctx, extention):
    if ctx.author.id == os.getenv("Owner_id"):
        bot.unload_extension(f'cogs.{extention}')
        await ctx.send(f'Unloaded {extention}')

@bot.command(name="Reload", help="Reloads a cog or all cogs")
async def Reload(ctx, extention):
    if ctx.author.id == os.getenv("Owner_id"):
        if extention == "all":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    bot.unload_extension(f'cogs.{filename[:-3]}')
                    bot.load_extension(f'cogs.{filename[:-3]}')
            return await ctx.send("Reloaded all cogs")
        bot.unload_extension(f'cogs.{extention}')
        bot.load_extension(f'cogs.{extention}')
        await ctx.send(f'Reloaded {extention}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(name="Ping", help="Pong!")
async def Ping(ctx):
    for s in session.query(db.Server).all():
        print(s.server_name)
        print(s.server_id)
        print(s.welcome_message_bool)
        print(s.welcome_message)
        print(s.welcome_message_channel)

bot.run(DISCORD_TOKEN)