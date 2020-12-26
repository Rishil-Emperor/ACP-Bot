import discord
from discord.ext import commands
import rules
from rules import rules

# Bot Prefix
client = commands.Bot(command_prefix='!')

# On Run
@client.event
async def on_ready():
    print('Bot is ready.')

# !hello
@client.command()
async def hello(ctx):
    await ctx.send('Hi!')

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
    await ctx.send(f'{member} has been kicked from ACP Main for {reason}.')
    await member.kick(reason=reason)

# !ban <user>
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member,*, reason = 'No Reason Provided'):
    await ctx.send(f'{member} has been banned from ACP Main for {reason}.')
    await member.ban(reason=reason)

# Token
import os
client.run(os.getenv('TOKEN'))