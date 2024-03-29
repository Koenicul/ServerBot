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
        if ctx.author.id == int(os.getenv("Owner_id")) or container == "minecraft":
            con = client.containers.get(container)
            con.start()
            await ctx.send(f"{con.name} started")

    @commands.command(name="Stop", help="Stop a docker container")
    async def Stop(self, ctx, container):
        if ctx.author.id == int(os.getenv("Owner_id")):
            con = client.containers.get(container)
            con.stop()
            await ctx.send(f"{con.name} stopped")

    @commands.command(name="ListContainers", help="List all containers")
    async def ListContainers(self, ctx):
        string = ""
        if ctx.author.id == int(os.getenv("Owner_id")):
            for i in client.containers.list(all=True):
                string += f"{i.name}\n"
            await ctx.send(string)

async def setup(bot):
    await bot.add_cog(Server(bot))