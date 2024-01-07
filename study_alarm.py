import discord

from discord.ext import tasks
import datetime
import time
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

@tasks.loop(minutes=1)
async def study_time_notification():
    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    if(now.hour == 9 and now.minute == 0):
        channel = client.get.channel(CHANNEL_ID)
        role = discord.utils.get(channel.guild.roles, name ="6기-server")
        await channel.send(f"{role.mention} 스터디 데일리를 작성하실 시간입니다! 오늘 공부할 주제, 가장 궁금한 점, 어제 공부한 내용을 적어주세요")

@client.event
async def on_ready():
    study_time_notification.start()

client.run(TOKEN)

