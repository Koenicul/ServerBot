from discord.ext import commands
import discord
import db
from sqlalchemy.orm import sessionmaker
import docker

Session = sessionmaker(bind=db.engine)
session = Session()

client = docker.from_env()

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="Start", help="Start a docker container")
    async def Start(self, ctx, container):
        print(client.containers.list)
        