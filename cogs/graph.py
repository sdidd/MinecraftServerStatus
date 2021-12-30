import discord
from discord.ext import commands
import matplotlib.pyplot as plt


class Equations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def plotlineareq(self, a, b, clr):
        x = [0, 10]
        y = [(a * i + b) for i in x]
        plt.figure(figsize=(10, 10))  # #Size of Graph
        plt.xlim(x)  # #X Range [-6,6]
        plt.ylim(x)  # #Y Range [-6,6]
        axis = plt.gca()  # #Get Current Axis
        plt.plot(axis.get_xlim(), [0, 0], 'k--')  # #X Axis Plots Line Across
        plt.plot([0, 0], axis.get_ylim(), 'k--')  # #Y Axis Plots Line Across
        plt.locator_params(axis="x", nbins=20)
        plt.locator_params(axis="y", nbins=20)
        plt.plot(x, y, label='linear', linestyle='solid', color=clr)
        plt.ylabel('Players')
        plt.xlabel('Time')
        mm = str(a)
        bb = str(b)
        plt.title('Live Status')
        #plt.grid()
        plt.savefig("foo.png")

    @commands.command()
    async def linear(self, ctx, equation):
        try:
            equation = equation.replace(" ", "")
            mx = equation.split("x")[0]
            mx = equation.replace("x", "").replace("y=", "")
            bx = equation.split("+")[1]
            self.plotlineareq(mx, bx, 'b')
            file = discord.File("foo.png", filename='foo.png')
            embed = discord.Embed(color=0xff0000)
            embed = embed.set_image(url="attachment://foo.png")
            await ctx.send(file=file, embed=embed)

        except Exception as e:
            await ctx.send(f"An error occured: {e}")

    def serialize(self):
        return {}

def setup(bot):
    bot.add_cog(Equations(bot))
