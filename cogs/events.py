from discord.ext import commands
import discord
import db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()

class Start(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="--help"))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        server = db.Server(guild.name, guild.id)
        session.add(server)
        session.commit()

    # @commands.Cog.listener()
    # async def on_guild_remove(self, guild):
    #     server = session.query(db.Server).filter(db.Server.server_id == guild.id).first()
    #     session.delete(server)
    #     session.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = session.query(db.Server).filter(db.Server.server_id == member.guild.id).first()
        if server.welcome_message_bool and server.welcome_message_channel != None:
            channel = self.bot.get_channel(server.welcome_message_channel)
            await channel.send(server.welcome_message)

def setup(bot):
    bot.add_cog(Start(bot))