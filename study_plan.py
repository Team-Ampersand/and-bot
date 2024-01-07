import discord

from discord.ext import tasks, commands
import datetime
import time
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

intents = discord.Intents.default()

intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='/', intents=intents)

@tasks.loop(minutes=1)
async def study_time_notification():
    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    if(now.hour == 9 and now.minute == 0):
        channel = bot.get.channel(CHANNEL_ID)
        role = discord.utils.get(channel.guild.roles, name ="6기-server")
        await channel.send(f"{role.mention} 스터디 데일리를 작성하실 시간입니다! 오늘 공부할 주제, 가장 궁금한 점, 어제 공부한 내용을 적어주세요")

@bot.event
async def on_ready():
    study_time_notification.start()

@bot.command()
async def plan(ctx):
    await ctx.send("오늘 공부할 주제를 입력해주세요!")
    try:
        today_task = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30.0)
    except asyncio.TimeoutError:
        return await ctx.send("입력 시간이 초과되었습니다.")
    
    await ctx.send("오늘 공부할 내용 중 가장 궁금한 점을 입력해주세요:")

    try:
        curious_point = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30.0)
    except asyncio.TimeoutError:
        return await ctx.send("입력 시간이 초과되었습니다.")

    await ctx.send("어제 공부한 주제를 간단히 입력해주세요")

    try:
        difficult_point = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30.0)
    except asyncio.TimeoutError:
        return await ctx.send("입력 시간이 초과되었습니다.")
    
    avatar_url = ctx.author.avatar_url  # 유저의 프로필 사진 URL
    embed = discord.Embed(title="Plan",
                          description=f"{ctx.author.mention} 할 일: {today_task.content}, "
                                      f"궁금한 점: {curious_point.content}, "
                                      f"어려운 점: {difficult_point.content}",
                          color=discord.Color.blue())
    embed.set_thumbnail(url=avatar_url)  # 프로필 사진을 썸네일로 추가

    await ctx.send(embed=embed)



bot.run(TOKEN)

