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

import numpy as np
import matplotlib.pyplot as plt



class grapher(commands.Cog):
    
    @commands.command()
    async def line_plot():
        # this sets up the Matplotlib interactive windows:
        #%matplotlib widget

        # this changes the default date converter for better interactive plotting of dates:
        plt.rcParams['date.converter'] = 'concise'

        #   Note the use of datetimes in the file complicate loading a bit.
        #   We recommend using pandas or xarray for more elegant solutions
        #   to handling complex timeseries data. 
        with open('data/small.txt', 'r') as f:
            data = np.genfromtxt(f, dtype='datetime64[s],f,f,f', 
                                 names=['date', 'doy', 'temp', 'solar'])
        datetime = data['date']
        dayofyear = data['doy']
        temperature = data['temp']
        solar = data['solar']

        # make two-day smoothed versions:
        temp_low = np.convolve(temperature, np.ones(48)/48, mode='same')
        solar_low = np.convolve(solar, np.ones(48)/48, mode='same')

        fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True, constrained_layout=True)

        # temperature:
        ax0.plot(datetime, temperature, label='hourly')
        ax0.plot(datetime, temp_low, label='smoothed')
        ax0.legend(loc='upper right')
        ax0.set_ylabel('Temperature $[^oC]$')  # note the use of TeX math formatting

        # solar-radiation:
        ax1.plot(datetime, solar, label='hourly')
        ax1.plot(datetime, solar_low, label='smoothed')
        ax1.legend(loc='upper right')
        ax1.set_ylabel('Solar radiation $[W\,m^{-2}]$')   # note the use of TeX math formatting

        ax0.set_title('Observations: Dinosaur, Colorado', loc='left')
        ax0.text(0.03, 0.03, 'https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/', 
                 fontsize='small', fontstyle='italic', transform=ax0.transAxes)

    def __init__(self, bot):
            self.bot = bot
        def serialize(self):
            return {}

def setup(bot):
    bot.add_cog(grapher(bot))
