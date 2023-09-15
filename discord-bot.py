import discord
import requests
from discord.ext import commands, tasks
import datetime
import asyncio
utc = datetime.timezone.utc

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.tree.command(name="iotd", description ="Shows the NASA Image of the Day")
async def iotd(ctx: discord.Interaction):
    response = requests.get("https://api.nasa.gov/planetary/apod", params={"api_key": "2D1xuvyksKFdFHCa8a4cUPHl5q0O8YKDhvSL7CUO"})
    iurl = response.json()['url']
    exp = response.json()['explanation']
    img = discord.Embed().set_image(url=iurl)
    await ctx.response.send_message(content=exp, embed=img)

@tasks.loop(time=datetime.time(hour=1, minute=1))
async def called_once_a_day():
    response = requests.get("https://api.nasa.gov/planetary/apod", params={"api_key": "2D1xuvyksKFdFHCa8a4cUPHl5q0O8YKDhvSL7CUO"})
    iurl = response.json()['url']
    exp = response.json()['explanation']
    img = discord.Embed().set_image(url=iurl)
    message_channel = bot.get_channel(1151160051193626725)
    await message_channel.send(content=exp, embed=img)

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

@bot.event
async def on_ready():
    called_once_a_day.start()
    await bot.tree.sync()


bot.run('MTE0Mjg4NTg2MzY0MzE3MzA0NA.GfxvFX.xti1nMbQd4-Zbg9kPfKxE8xbcYTo5smJA-mNM4')