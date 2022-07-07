import asyncio
from unittest import result
from colorama import Cursor
import discord
from discord.ext import commands
import sqlite3

class Event(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(selkf, message):
        if message.author.bot:
            return

        author = message.author
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM main WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ('INSERT INTO main(user_id, masterclass, cringe) VALUES (? , ?, ?)')
            val = (author.id ,0 ,0)
            cursor.execute(sql, val)
        
        db.commit()
        cursor.close()
        db.close()
        