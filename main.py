import asyncio
from dis import dis, disco
from multiprocessing.connection import wait
import sqlite3
from turtle import color
from unicodedata import name
import discord
from discord.ext import commands
from event import Event
import datetime as dt
from discord.utils import get

bot = commands.Bot(command_prefix='!!')

bot.add_cog(Event(bot))

@bot.command()
async def recap(ctx, member:discord.Member = None):
    if member is None:
        member = ctx.author

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT masterclass, cringe FROM main WHERE user_id = {member.id}')
    bal = cursor.fetchone()
    try:
        masterclass = bal[0]
        cringe = bal[1]
    except:
        masterclass = 0
        cringe = 0
    
    em = discord.Embed(title = f'Resume de {member.name}')
    em.add_field(name='Masterclass', value=masterclass)
    em.add_field(name='Cringe', value=cringe)
    await ctx.send(embed = em)

@bot.command()
async def cringe(ctx, member:discord.Member = None):
    if member == None:
        await ctx.send("vous n'avez pas designer de membre du serveur")
    else:
        em = discord.Embed(title = f'est-ce que {member.name} est cringe ?')
        em.add_field(name='oui', value= '✅')
        em.add_field(name='non', value= '❌')
        sended = await ctx.send(embed = em)
        await sended.add_reaction('✅')
        await sended.add_reaction('❌')

        await asyncio.sleep(300)

        fetch_msg = await ctx.channel.fetch_message(sended.id)
        reactions = fetch_msg.reactions
        
        for element in reactions:
            if element.emoji == '✅':
                poss = element.count
            if element.emoji == '❌':
                neg = element.count
        
        if poss > neg :
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'UPDATE main SET cringe = cringe + 1 WHERE user_id = {member.id}')

            db.commit()
            cursor.close()
            db.close()

@bot.command()
async def masterclass(ctx, member:discord.Member = None):
    if member == None:
        await ctx.send("vous n'avez pas designer de membre du serveur")
    else:
        em = discord.Embed(title = f'est-ce que {member.name} est masterclass ?')
        em.add_field(name='oui', value= '✅')
        em.add_field(name='non', value= '❌')
        sended = await ctx.send(embed = em)
        await sended.add_reaction('✅')
        await sended.add_reaction('❌')

        await asyncio.sleep(300)

        fetch_msg = await ctx.channel.fetch_message(sended.id)
        reactions = fetch_msg.reactions
        
        for element in reactions:
            if element.emoji == '✅':
                poss = element.count
            if element.emoji == '❌':
                neg = element.count
        
        if poss > neg :
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'UPDATE main SET masterclass = masterclass + 1 WHERE user_id = {member.id}')

            db.commit()
            cursor.close()
            db.close()

@bot.command()
async def topcringe(ctx):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    cursor.execute('select user_id, cringe FROM main ORDER by cringe DESC')
    rank = cursor.fetchall()

    if len(rank) > 10:
        rank = rank[:9]

    em = discord.Embed(
        title = 'Plus gros cringelord du serv'
    )
    namelist = ''
    for element in rank:
        user = await bot.fetch_user(element[0])
        namelist = namelist + str(user.name) + ' -- ' + str(element[1]) +' point cringe\n'
    em.add_field(
        name='les pretendant au titre de cringelord',
        value= namelist
    )
    await ctx.send(embed = em)

@bot.command()
async def topmaster(ctx):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    cursor.execute('select user_id, masterclass FROM main ORDER by masterclass DESC')
    rank = cursor.fetchall()

    if len(rank) > 10:
        rank = rank[:9]

    em = discord.Embed(
        title = 'Plus gros masterclass du serv'
    )
    namelist = ''
    for element in rank:
        user = await bot.fetch_user(element[0])
        namelist = namelist + str(user.name) + ' -- ' + str(element[1]) +' point masterclass\n'
    em.add_field(
        name='les pretendant au titre de masterclass',
        value= namelist
    )
    await ctx.send(embed = em)

async def schedule_reset():
    while True:
        now = dt.datetime.now()
        then = now + dt.timedelta(days=1)
        then.replace(hour=0, minute=1)
        wait_time = (then - now).total_seconds()
        await asyncio.sleep(wait_time)

        await award_cringelord()
        await award_masterclass()

        if str(dt.datetime.date(dt.datetime.now())).split('-')[2] == '01':
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute('UPDATE main SET cringe = 0 ; UPDATE main SET masterclass = 0')

            db.commit()
            cursor.close()
            db.close()

async def award_masterclass():
    if get(discord.Guild.roles, name= 'Masterclass') == None:
        role = await discord.Guild.create_role(
            name = 'Masterclass',
            color = discord.Colour.blue
        )
    else:
        role = get(discord.Guild.roles, name='Masterclass')

    for member in discord.Guild.members:
        for role_ in member.roles:
            if role_.name == 'Masterclass':
                await member.remove_role(role_)

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    cursor.execute('select user_id FROM main ORDER by masterclass DESC')
    rank = cursor.fetchall()

    db.commit()
    cursor.close()
    db.close()

    user = await bot.fetch_user(rank[0])

    user.add_role(role)

async def award_cringelord():
    if get(discord.Guild.roles, name= 'Cringe lord') == None:
        role = await discord.Guild.create_role(
            name = 'Cringe lord',
            color = discord.Colour.red
        )
    else:
        role = get(discord.Guild.roles, name='Cringe lord')

    for member in discord.Guild.members:
        for role_ in member.roles:
            if role_.name == 'Cringe lord':
                await member.remove_role(role_)

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    cursor.execute('select user_id FROM main ORDER by cringe DESC')
    rank = cursor.fetchall()

    db.commit()
    cursor.close()
    db.close()

    user = await bot.fetch_user(rank[0])

    user.add_role(role)
    
@bot.event
async def on_ready():
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS main (
            user_id INTEGER, masterclass INTEGER, cringe INTEGER
        )''')
        print('Bot Is Online')
        await schedule_reset()

bot.run('OTk0MzE4NDcyNzU2NTk2ODA2.GIP5RB.wJW3Quq-dLmc_FWddGQRFaRdFXpGgEWxZ4Mpio')