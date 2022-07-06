from discord.ext import commands
import discord
import db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ToggleWelcome", help="Toggles welcome messages")
    async def ToggleWelcome(self, ctx):
        server = session.query(db.Server).filter(db.Server.server_id == ctx.guild.id).first()
        if server.welcome_message_bool:
            server.welcome_message_bool = False
            await ctx.send("Welcome messages disabled")
        else:
            server.welcome_message_bool = True
            await ctx.send("Welcome messages enabled")
        session.commit()
    
    @commands.command(name="SetWelcome", help="Sets welcome messages")
    async def SetWelcome(self, ctx, *, message):
        server = session.query(db.Server).filter(db.Server.server_id == ctx.guild.id).first()
        server.welcome_message = message
        await ctx.send("Welcome message set")
        session.commit()
    
    @commands.command(name="SetWelcomeChannel", help="Sets welcome messages channel")
    async def SetWelcomeChannel(self, ctx, channel: int):
        server = session.query(db.Server).filter(db.Server.server_id == ctx.guild.id).first()
        server.welcome_message_channel = channel
        await ctx.send("Welcome message channel set")
        session.commit()

def setup(bot):
    bot.add_cog(Welcome(bot))