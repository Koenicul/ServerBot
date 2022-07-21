from discord.ext import commands, tasks
import discord
import db
from sqlalchemy.orm import sessionmaker
import os

Session = sessionmaker(bind=db.engine)
session = Session()

class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_server.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="--help"))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        server = session.query(db.Server).filter(db.Server.server_id == guild.id).first()
        if server is None:
            server = db.Server(guild.name, guild.id)
            session.add(server)
            session.commit()
            channel = self.bot.get_channel(int(os.getenv("Log_channel")))
            await channel.send(f"{guild.name} has been added\n{guild.id}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = session.query(db.Server).filter(db.Server.server_id == member.guild.id).first()
        if server.welcome_message_bool and server.welcome_message_channel != None:
            channel = self.bot.get_channel(server.welcome_message_channel)
            await channel.send(server.welcome_message)

    @tasks.loop(minutes=5)
    async def check_server(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(int(os.getenv("Log_channel")))
        await channel.send("Checking servers")
        for guild in self.bot.guilds:
            server = session.query(db.Server).filter(db.Server.server_id == guild.id).first()
            if server == None:
                server = db.Server(guild.name, guild.id)
                session.add(server)
                session.commit()
                await channel.send(f"{guild.name} has been added\n{guild.id}")

        for server in session.query(db.Server).all():
            if server.server_id not in [guild.id for guild in self.bot.guilds]:
                session.delete(server)
                session.commit()
                await channel.send(f"{server.server_name} has been removed")

def setup(bot):
    bot.add_cog(Start(bot))