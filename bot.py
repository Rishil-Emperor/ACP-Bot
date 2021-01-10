import discord
from discord.ext import commands
import rules
from rules import rules
import asyncio
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import random
import replies
from replies import replies

# Bot Prefix
client = commands.Bot(command_prefix='!')

# On Run
@client.event
async def on_ready():
    print('Bot is ready.')
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="Rishil_Emperor#0001"), )

# On Error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permission to perform this command.')
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'You are on cooldown for {str(error.retry_after)[:3]} seconds!')

# !hello
@client.command()
async def hello(ctx):
    await ctx.send('Hi!')

# !coinflip
@client.command(aliases = ['coinflip'])
async def flip(ctx):
    coin = ['Heads', 'Tails']
    await ctx.send(f':coin: | It\'s **{random.choice(coin)}**!')

# !8ball <question>
@client.command(aliases = ['8Ball', '8ball'])
async def fortune(ctx, *, statement):
    reply = random.choice(replies)
    await ctx.send(f'🎱 | {reply}')

# !rps <choice>
@client.command(aliases = ['rockpaperscissors', 'RPS'])
async def rps(ctx, *, choice):
    rps_choices = ['rock', 'paper', 'scissors']
    rps_choice = random.choice(rps_choices)
    if choice.lower() == rps_choice:
        await ctx.send(f'I chose `{rps_choice}` and you chose `{choice.lower()}`. **Tie!**')
    elif choice.lower() == 'rock' and rps_choice == 'scissors' or choice.lower() == 'scissors' and rps_choice == 'paper' or choice.lower() == 'paper' and rps_choice == 'rock':
        await ctx.send(f'I chose `{rps_choice}` and you chose `{choice.lower()}`. **You Win!**')
    elif choice.lower() == 'rock' and rps_choice == 'paper' or choice.lower() == 'paper' and rps_choice == 'scissors' or choice.lower() == 'scissors' and rps_choice == 'rock':
        await ctx.send(f'I chose `{rps_choice}` and you chose `{choice.lower()}`. **I Win!**')
    else:
        await ctx.send(f'Something went wrong. Please make sure your choice is either `rock`, `paper`, or `scissors`.')

# !choosenumber <number 1> <number 2>
@client.command(aliases = ['number'])
async def choosenumber(ctx, num1, *, num2):
    try:
        num_1 = int(num1)
        num_2 = int(num2)
        if num_1 > num_2:
            await ctx.send(f'Please make sure you are inputting two numbers. Make sure that the first number is less than the second number.')
        else:
            await ctx.send(f'Number: **{random.choice(range(num_1, num_2+1))}**')
    except:
        await ctx.send(f'Please make sure you are inputting two numbers. Make sure that the first number is less than the second number.')

# !rule <number>
@client.command()
async def rule(ctx, *, number):
    await ctx.send(rules[int(number) - 1])

# !purge <amount>
@client.command(aliases=['clear'])
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount):
    await ctx.channel.purge(limit=int(amount) + 1)

# !kick <user>
@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member,*, reason = 'No Reason Provided'):
        await ctx.send(f'**{member}** has been kicked from ACP Main for {reason}.')
        await member.kick(reason=reason)

# !ban <user>
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member,*, reason = 'No Reason Provided'):
    await ctx.send(f'**{member}** has been banned from ACP Main for {reason}.')
    await member.ban(reason=reason)

# !unban <user>
@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')
    for banned_entry in banned_users:
        user = banned_entry.user
        if(user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(f'**{member_name}** has been unbanned.')
            return

# !mute <user>
@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member : discord.Member, duration=0,*, unit = None):
    muted_role = ctx.guild.get_role(607034271990939658)
    await ctx.send(f'**{member.mention}** has been muted for *{duration}{unit}*.')
    await member.add_roles(muted_role)
    if unit.lower() == 's':
        wait = 1 * duration
        await asyncio.sleep(wait)
    elif unit.lower() == 'm':
        wait = 60 * duration
        await asyncio.sleep(wait)
    elif unit.lower() == 'h':
        wait = 3600 * duration
        await asyncio.sleep(wait)
    await member.remove_roles(muted_role)
    await ctx.send(f'**{member.mention}** has been unmuted.')

# !unmute <user>
@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(607034271990939658)
    await member.remove_roles(muted_role)
    await ctx.send(f'**{member.mention}** has been unmuted.')

# !warn <user> <reason>
@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member : discord.Member, *, reason = 'No Reason Provided'):
    await ctx.send(f'**{member}** has been warned for {reason}.')

# !ping
@client.command()
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def ping(ctx):
    latency = str(client.latency * 1000)
    decimal = latency.split('.')
    await ctx.send(f'🏓 | **Pong!** `{decimal[0]}ms`')

# !whois <user>
@client.command(aliases = ['user', 'info'])
async def whois(ctx, member : discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title = member.name, description = member.mention, color = discord.Colour.purple())
    embed.add_field(name = 'ID', value = member.id , inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Requested By: {ctx.author.name}')
    await ctx.send(embed = embed)

# !calc <number> <operator> <number>
@client.command(aliases=['calculate'])
async def calc(ctx, *, equation):
    try:
        list = equation.split(' ')
        digits1 = 0
        digits2 = 0
        for x in list[0]:
          if x != '.':
            digits1 += 1
          else:
            continue
        for x in list[2]:
          if x != '.':
            digits2 += 1
          else:
            continue
        if digits1 <= 10 and digits2 <= 10:
          if list[1] == '+':
             await ctx.send(f'{list[0]} + {list[2]} = {float(list[0]) + float(list[2])}')
          elif list[1] == '-':
             await ctx.send(f'{list[0]} - {list[2]} = {float(list[0]) - float(list[2])}')
          elif list[1].lower() == 'x' or list[1] == '*':
             await ctx.send(f'{list[0]} x {list[2]} = {float(list[0]) * float(list[2])}')
          elif list[1] == '/':
            await ctx.send(f'{list[0]} / {list[2]} = {float(list[0]) / float(list[2])}')
          else:
              await ctx.send(f'Could not understand; incorrect format. Include a space between number and operator. Please make sure to perform !calc like this: <number> <operator> <number>.\nEx:\n- !calc 4 x 5\n- !calc 3345 + 123\n- !calc 54 / 3')
        else:
            await ctx.send(f'Numbers must only contain 10 or less digits.')
    except:
          await ctx.send(f'Could not understand; incorrect format. Include a space between number and operator. Please make sure to perform !calc like this: <number> <operator> <number>.\nEx:\n- !calc 4 x 5\n- !calc 3345 + 123\n- !calc 54 / 3')

