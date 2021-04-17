from discord.ext.commands import Cog
from discord.ext import commands
from discord.ext.commands import command
import typing as t

import asyncio
from lib.db import db


class Main(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="assignment", invoke_without_command=True)
    async def assignment_group(self, ctx):
        pass

    # execute INSTER INTO (table name) (Columns) Values
    @assignment_group.command(name="add")
    async def assignment_add_command(self, ctx, name: str, due_date: str):
        db.execute(
            "INSERT INTO assignments (UserID, Name, DueDate) Values (?, ?, ?)",
            ctx.author.id,
            name,
            due_date,
        )

        print("Test")

        check = db.records(
            "SELECT DueDate FROM assignments WHERE UserID = ? AND Name = ?",
            ctx.author.id,
            name
        )

        await ctx.send(check)
    
    @assignment_group.command(name="delete")
    async def assignment_delete_command(self, ctx, *, name: str):
        pass

    @assignment_group.command(name="edit")
    async def assignment_edit_command(self, ctx, *, name: str):
        pass

    @command(name="ping")
    async def ping(self, ctx, name: str, subject: str, due_date: str):
        await ctx.send(f"Assignment: {name} is due on {due_date} and is in the subject: {subject}")
        print("pong")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("main")

def setup(bot):
    bot.add_cog(Main(bot))