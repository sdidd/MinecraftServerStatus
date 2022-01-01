import discord
import random
import os
import asyncio
from discord.ext import tasks
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
from mcstatus import MinecraftServer
# line_plot.py

import matplotlib.pyplot as plt

def line_plot(numbers):
    plt.plot(numbers)
    plt.ylabel('Random numbers')
    plt.show()

if __name__ == '__main__':
    numbers = [2, 4, 1, 6]
    line_plot(numbers)
