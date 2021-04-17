from discord.ext.commands import Cog
from discord.ext import commands
from discord.ext.commands import command
from discord import Embed
import typing as t

import asyncio
from lib.db import db


class Main(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="assignment", invoke_without_command=True)
    async def assignment_group(self, ctx):
        pass

    @assignment_group.command(name="add")
    async def assignment_add_command(self, ctx, name: str, due_date: str):
        db.execute(
            "INSERT INTO assignments (UserID, Name, DueDate) Values (?, ?, ?)",
            ctx.author.id,
            name,
            due_date,
        )

        embed = self.display_assignment("Added Assignment", ctx.author.id, name)   

        await ctx.send(embed=embed)

    @assignment_group.command(name="delete")
    async def assignment_delete_command(self, ctx, name: str):
        embed = self.display_assignment("Deleted Assignment", ctx.author.id, name)
        db.execute(
            "DELETE FROM assignments WHERE UserID = ? AND Name = ?",
           ctx.author.id,
           name
        )

        await ctx.send(embed=embed)

    @assignment_group.command(name="edit")
    async def assignment_edit_command(self, ctx, *, name: str):
        pass

    @assignment_group.command(name="display", aliases=["view", "see"])
    async def assignment_display_command(self, ctx, *, name: str):
        embed = self.display_assignment("Displaying an Assignment", ctx.author.id, name)

        await ctx.send(embed=embed)

    
    @assignment_group.command(name="display-all", aliases=["view-all", "see-all", "all"])
    async def assignment_display_all_command(self, ctx):
        assignments = db.record("SELECT Name, DueDate FROM assignments WHERE UserID GLOB ?",
                      ctx.author.id
        )

        await ctx.send(assignments)

    def display_assignment(self, title: str, UserID: int, name: str):
        due_date = db.record("SELECT DueDate FROM assignments WHERE UserID = ? AND Name = ?",
                            UserID,
                            name
        )
        if due_date == None:
            print("This ran")
            return Embed(title="No Assignment Found")

        embed = Embed(title=title,)
        embed.add_field(name=f"**__{name}__**", value=f"Due on {due_date[0]}", inline=True)

        return embed

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("main")

def setup(bot):
    bot.add_cog(Main(bot))