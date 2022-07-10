from discord.ext import commands, tasks
import discord
import db
from sqlalchemy.orm import sessionmaker
import docker
import os

Session = sessionmaker(bind=db.engine)
session = Session()

client = docker.from_env()

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.minecraft_status.start()
        self.last_status = "exited"

    @tasks.loop(minutes=5)
    async def minecraft_status(self):
        await self.bot.wait_until_ready()
        con = client.containers.get("minecraft")
        if con.status != self.last_status:
            self.last_status = con.status
            channel = self.bot.get_channel(int(os.getenv("Log_channel")))
            await channel.send(f"Minecraft server is now {con.status}")

def setup(bot):
    bot.add_cog(Minecraft(bot))