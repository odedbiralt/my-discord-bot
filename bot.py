import discord
from discord.ext import commands
from discord.utils import get
import json
from discord.voice_client import VoiceClient
import time
import youtube_dl
import os
from discord import FFmpegPCMAudio
client = commands.Bot(command_prefix="?")
ID = 710428290455699517
id = client.get_guild(ID)
players = {}

client.remove_command('help')

@client.event
async def on_ready():
    print("Bot Ready")
    await client.change_presence(activity=discord.Game(name='with your life'))








@client.command()
async def ping(ctx):

    await ctx.send(f"Ping: {round(client.latency * 1000)}ms")
@client.command()
async def report(ctx, user, reason):
    try:
        await ctx.channel.purge(limit=1)
        await ctx.author.send(f" {user} תודה לך שדווחת על   ")
        channel = client.get_channel(726447967686492240)
        await channel.send(f"user: <@!{ctx.author.id}> reported: {user} reason: {reason}")
    except:
        await ctx.channel.purge(limit=1)
        await ctx.send("שימוש לא נכון בפקודה")
@client.command()
async def bal(ctx):
    with open("bank.json", "r") as f:
        users = json.load(f)
    if str(ctx.author.id) in users:
        print("user all ready exists")
    else:
        users[str(ctx.author.id)] = []
        users[str(ctx.author.id)].append({
            "coin":500

        })
    with open("bank.json", "w") as f:
        json.dump(users, f)

    await ctx.send(f"<@{ctx.author.id}> {check_bal(ctx.author)}")

def check_bal(user):
    with open("bank.json", "r") as f:
        users = json.load(f)
    for coin in users[str(user.id)]:
        return coin["coin"]
@client.command()
async def help(ctx):
    embedhelp = discord.Embed(title="  ", description="help", color=0x3500f5)
    embedhelp.set_author(name="Help")
    embedhelp.add_field(name="ping", value="כמות הדילי בינך ובין הבוט ב מילישניות", inline=False)
    embedhelp.add_field(name="report", value="לדווח על מישהוא", inline=False)
    embedhelp.add_field(name="bal", value="כמות הכסף שלך", inline=False)
    embedhelp.add_field(name="play [URL]", value="לנגן שיר, מסויים אתה צריך להוסיף URL לפקודה", inline=False)
    embedhelp.add_field(name="stop", value="לעצור את השיר המתנגן", inline=False)
    embedhelp.add_field(name="resume", value="להמשיך את השיר המתנגן", inline=False)
    embedhelp.add_field(name="pause", value="להפסיק את הנגינה של השיר", inline=False)
    embedhelp.set_footer(text="By Odedbir")
    await ctx.send(embed=embedhelp)
@client.command()
async def shop(ctx):
    embed = discord.Embed(title="     ", description="אפשר לקנות דברים", color=0xffae00)
    embed.set_author(name="חנות")
    embed.add_field(name=":money_with_wings:  :תחון", value="5000", inline=False)
    embed.add_field(name=":moneybag:  :עשיר", value="1000", inline=False)
    embed.add_field(name=":computer:  :אומר את השם שלכם בסרטון", value="1500", inline=True)
    embed.set_footer(text="By Odedbir")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("💸")
    await msg.add_reaction("💰")
    await msg.add_reaction("💻")
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id

    if message_id == 743905978059325631:
        with open("bank.json","r") as f:
            data = json.load(f)
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = client.get_user(payload.user_id)
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        if payload.emoji.name == '💸':
            await message.remove_reaction('💸', user)
            for coin in data[str(payload.user_id)]:
                 bal = coin["coin"]
            if bal >= 5000:
                role = discord.utils.get(guild.roles, name="תחון")
                for item in data[str(payload.user_id)]:
                    item["coin"] -= 5000
            else:
                await member.send("אין לך מספיק כסף!")
        if payload.emoji.name == '💻':
            await message.remove_reaction('💻', user)
            for coin in data[str(payload.user_id)]:
                 bal = coin["coin"]
            if bal >= 1500:
                role = discord.utils.get(guild.roles, name="סרטון הבא")
                for item in data[str(payload.user_id)]:
                    item["coin"] -= 1500
            else:
                await member.send("אין לך מספיק כסף!")
        if payload.emoji.name == '💰':
            await message.remove_reaction('💰', user)
            for coin in data[str(payload.user_id)]:
                 bal = coin["coin"]
            if bal >= 1000:
                role = discord.utils.get(guild.roles, name="עשיר")
                for item in data[str(payload.user_id)]:
                    item["coin"] -= 1000
            else:
                await member.send("אין לך מספיק כסף!")
        if role is not None:
            if member is not None:
                await member.add_roles(role)
                await member.send("תודה שקנית")
                with open("bank.json", "w") as f:
                    json.dump(data, f)
@client.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("אתה לא בשיחה!")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send( f"נכנסתי ל  {channel} ")
@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("חכה שהשיר שכרגע מתנגן יסיים או שתשתמש ב stop?")
        return
    await ctx.send("מפעיל את השיר אנא המתן....")
    print("Someone wants to play music let me get that ready for them...")
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()
@client.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(( f"יצאתי מ  {channel} "))
    else:
        await ctx.send("אני לא נמצא בשיחה!")
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.stop()
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.resume()
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.pause()
@client.command()
async def give_bal(ctx, user, amount):
    owner = discord.utils.get(ctx.guild.roles, name="👑Owner👑")
    mod = discord.utils.get(ctx.guild.roles, name="👨‍⚖️Mod👨‍⚖️")
    bot = discord.utils.get(ctx.guild.roles, name="🤖Bot🤖")
    userid = user[3:21]
    if owner or mod or bot in ctx.author.roles:
        with open("bank.json","r") as f:
            data = json.load(f)
        for coin in data[str(userid)]:
            bal = coin["coin"]
        for item in data[str(userid)]:
            item["coin"] += int(amount)
        with open("bank.json", "w") as f:
            json.dump(data, f)
    else:
        ctx.send("אין לך גישה לפקודה זו!")
@client.command()
async def pay(ctx,user,amount):
    if int(amount) > 0:
        userid = user[3:21]
        with open("bank.json", "r") as f:
            data = json.load(f)
        for coin in data[str(userid)]:
            bal = coin["coin"]
        for item in data[str(userid)]:
            item["coin"] += int(amount)
        for item in data[str(ctx.author.id)]:
            item["coin"] -= int(amount)
        with open("bank.json", "w") as f:
            json.dump(data, f)
    else:
        await ctx.send("אתה לא יכול לעשות את זה.....")
client.run("NzM0ODA5MzIxODU4MjY5Mjc0.XxXGgg.5LmH5kwoQDMwp703uKKu6c9rMUQ")
