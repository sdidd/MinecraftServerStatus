import discord
from discord.ext import commands

class Example(commands.Cog):

    def _init_(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Example(bot))
