import discord
import random
import os
import asyncio
from discord.ext import tasks
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
from mcstatus import MinecraftServer



global bot
global msg
load_dotenv('token.env')
token = os.getenv('DISCORD_TOKEN')
print(token)



#Prefix for BOT
load_dotenv('prefix.env')
default_prefix = os.getenv('default_prefix')
new_prefix = os.getenv('new_prefix')

#bot = commands.Bot(command_prefix = [default_prefix, new_prefix])
def update_prefix():
    load_dotenv('prefix.env')
    default_prefix = os.getenv('default_prefix')
    new_prefix = os.getenv('new_prefix')
    return commands.Bot(command_prefix = [default_prefix, new_prefix])

bot = update_prefix()

#load and unload cogs
#@bot.command()
#async def load(ctx, extension):
#    bot.load_extension(f'cogs.{extension}')

#@bot.command()
#async def unload(ctx, extension):
#    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#REACTION EMOJI
emoji = '\N{Black Universal Recycling Symbol}'

@bot.event
async def on_ready():
        activity = discord.Activity(type=discord.ActivityType.watching, name="villagers DIE")
        await bot.change_presence(status=discord.Status.online, activity=activity)
        print('Logged in as {0.user}'.format(bot))
    #print(f'Bot is ready logged in as:{bot.user.name}')

#@bot.event
#async def on_member_join(member):
    #print(f'{member} has joined a server.')

#@bot.event
#async def on_member_remove(member):
   # print(f'{member} has left the server')


@bot.command()
async def ping(ctx):
    #emoji = '\N{Black Universal Recycling Symbol}'
    print("Invoking ping command")
    pingvalue = bot.latency * 1000
    embed=discord.Embed(title="Sample Embed", url="", description=f'Pong!' + "%.2f" % pingvalue + 'ms', color=0xFF5733)
    await ctx.send(embed=embed)
    #await ctx.embed(f'Pong!' + "%.2f" % pingvalue + 'ms')
    #await msg.add_reaction(emoji)

@bot.command(name='random')
async def _randomNumber(ctx,a:int, b:int):
    #ranNumber = random.randrange(no1,no2)
    number = random.randint(a,b)
    await ctx.send(number)

@bot.event
async def on_message(message):
    replies = [
    'You are gay!!',
    'SHUTUP BITCH',
    'DIES DUMB',
    'Your MOM is bad',
    ]
    if message.author == bot.user:
        return
    else:
        if message.content == 'ZTI is bad':
            response  = random.choice(replies)
            await message.channel.send(response)
        if message.content == 'Good Night' or message.content == 'good night' or message.content == 'gn':
            await message.channel.send('Good Night vro')
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.reply(error)

#Minecraft Server Connection
@bot.command(name = 'server')
async def _minecraftserverinfo(ctx, ip:str, port:str, servername:str):
    if servername == "survival":
        svname = "Survival"
    elif servername == "lobby":
        svname = "Lobby"

    while True:
        server = MinecraftServer.lookup(ip+':'+port)
            # 'status' is supported by all Minecraft servers that are version 1.7 or higher.
        status = server.status()
        latency = server.ping()
        query = server.query()
        serverembed = discord.Embed(title = ip, url = "https://www.zer02infinity.com/",description = f"Zero To Infinity Minecraft {svname} Server", color =  discord.Color.from_rgb(100,100,100))#\nThe server has the following players online: {','.join(query.players.names)}")
        serverembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/833829693588373534/920017091325747220/2021-12-13_11.png")
        serverembed.add_field(name="Players Count", value=f"{status.players.online}/{query.players.max}", inline=True)
        serverembed.add_field(name="Direct Connect:", value=f"```mc.zer02infinity.com```", inline=True)
        #serverembed.add_field(name="Names:", value=f"{latency} ms", inline=True)
        #nl = '\n'

        serverembed.add_field(name="Names:", value={','.join(query.players.names)}, inline=False)
        #file = discord.File("./foo.png", filename="foo.png")
        serverembed.set_image(url="http://graph1.gamestatus.xyz:8080/821765352307294298/graph_image.png?id=1640195422327")
        embed = await ctx.send(embed = serverembed)
        #await embed.add_reaction(emoji)
        await asyncio.sleep(5)
        await embed.delete()
        pass

#TAKE CHANNEL ID AND MESSAGEID
@bot.event
async def on_raw_reaction_add(payload):
    #refreshemoji = bot.get_emoji(920740685966086184)
    #await ctx.send(refreshemoji)
    load_dotenv('channelID.env')
    channel_id = os.getenv('channelID')
    #channel = bot.get_channel(channel_id)
    guild = bot.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if payload.user_id == bot.user.id:
        return
    if payload.emoji.name == '\N{Black Universal Recycling Symbol}':
        print("in if statement")
        print(payload.message_id)
        print(channel_id)
           # wait(4)
        #await asyncio.sleep(2)
        await message.remove_reaction('\N{Black Universal Recycling Symbol}', payload.member)
        #await message.edit(embed=serverembed)
    else:
        await message.remove_reaction(payload.emoji.name, payload.member)
    return

bot.run(token)
