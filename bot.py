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
            await ctx.send(f'{member_name} has been unbanned.')
            return

# !calc <number> <operator> <number>
@client.command(aliases=['calculate'])
async def calc(ctx, *, equation):
    try:
        list = equation.split(' ')
        if list[1] == '+':
            await ctx.send(f'{list[0]} + {list[2]} = {int(list[0]) + int(list[2])}')
        elif list[1] == '-':
            await ctx.send(f'{list[0]} - {list[2]} = {int(list[0]) - int(list[2])}')
        elif list[1].lower() == 'x' or list[1] == '*':
            await ctx.send(f'{list[0]} x {list[2]} = {int(list[0]) * int(list[2])}')
        elif list[1] == '/':
            await ctx.send(f'{list[0]} / {list[2]} = {int(list[0]) / int(list[2])}')
        elif list[1] == '^':
            await ctx.send(f'{list[0]} ^ {list[2]} = {int(list[0]) ** int(list[2])}')
        else:
            await ctx.send(f'Could not understand; incorrect format. Include a space between number and operator. Please make sure to perform !calc like this: <number> <operator> <number>.\nEx:\n- !calc 4 x 5\n- !calc 3345 + 123\n- !calc 54 / 3')
    except:
        await ctx.send(f'Could not understand; incorrect format. Include a space between number and operator. Please make sure to perform !calc like this: <number> <operator> <number>.\nEx:\n- !calc 4 x 5\n- !calc 3345 + 123\n- !calc 54 / 3')