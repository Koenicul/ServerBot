from discord.ext import commands
import discord
import db
from sqlalchemy.orm import sessionmaker
import docker
import os

Session = sessionmaker(bind=db.engine)
session = Session()

client = docker.from_env()

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="Start", help="Start a docker container")
    async def Start(self, ctx, container):
        if ctx.author.id == os.getenv("Owner_id"):
            con = client.containers.get(container)
            con.start()
            await ctx.send(f"{con.name} started")

    @commands.command(name="Stop", help="Stop a docker container")
    async def Stop(self, ctx, container):
        if ctx.author.id == os.getenv("Owner_id"):
            con = client.containers.get(container)
            con.stop()
            await ctx.send(f"{con.name} stopped")

    @commands.command(name="ListContainers", help="List all containers")
    async def ListContainers(self, ctx):
        if ctx.author.id == os.getenv("Owner_id"):
            for i in client.containers.list(all=True):
                await ctx.send(f"{i.name}")

def setup(bot):
    bot.add_cog(Server(bot))