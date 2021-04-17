from discord.ext.commands import Cog
from discord.ext import commands
from discord.ext.commands import command
from discord import Embed
import discord
import typing as t

import asyncio
from lib.db import db


class Assignments(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="assignment", invoke_without_command=True)
    async def assignment_group(self, ctx):
        pass
    

    @assignment_group.command(name="help")
    async def assignment_help_command(self, ctx):
        await ctx.send("Please use **quotations** around multi-word input\n\nSample: `.assignment add \"Math Homework\" <Date>`\n\nThe format for dates is **month/day/year Hour:Minutes**. Please use military time for the hours\n\nSample: `.assignment add <Assignment> \"4/17/2021 12:00\"`") 


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
        try:
            db.execute(
                "DELETE FROM assignments WHERE UserID = ? AND Name = ?",
               ctx.author.id,
               name
            )
        except:
            pass

        await ctx.send(embed=embed)

    @assignment_group.command(name="delete-all")
    async def assignment_delete_comand(self, ctx):
        try:
            db.execute(
                "DELETE FROM assignments WHERE UserID = ?",
                ctx.author.id,
            )
            
            await ctx.send(f"All assignments for {ctx.author.name} have been deleted")
        except:
            await ctx.send("You do not have any assignments to delete")


    @assignment_group.command(name="edit-name", aliases=["name-edit", "name"])
    async def assignment_edit_name_command(self, ctx, name: str, newName: str):
        embed = self.edit_name_command(ctx, name, newName)

        await ctx.send(embed=embed)


    @assignment_group.command(name="edit-date", aliases=["date-edit", "date"])
    async def assignment_edit_date_command(self, ctx, name: str, newDate: str):
        embed = self.edit_date_command(ctx, name, newDate)

        await ctx.send(embed=embed)


    def edit_name_command(self, ctx, name: str, newName: str):
        due_date, completion = db.record("SELECT DueDate, Completed FROM assignments WHERE UserID = ? AND Name = ?",
                              ctx.author.id,
                              name
                    )

        db.execute(
            "UPDATE assignments SET Name = ? WHERE Name = ?",
            newName,
            name
        )

        print(due_date)

        embed = Embed(title="Assignment's Name Changed")
        embed.add_field(name=f"**{newName}**", value=f"Due on {due_date}\nCompleted: {completion}", inline=True)

        return embed


    def edit_date_command(self, ctx, name: str, newDate: str):
        completion = db.record("SELECT DueDate, Completed FROM assignments WHERE UserID = ? AND Name = ?",
                              ctx.author.id,
                              name
                    )

        db.execute(
            "UPDATE assignments SET DueDate = ? WHERE Name = ?",
            newDate,
            name
        )

        embed = Embed(title="Assignment's Date Changed")
        embed.add_field(name=f"**{name}**", value=f"Due on {newDate}\nCompleted: {completion}", inline=True)

        return embed


    @assignment_group.command(name="display", aliases=["view", "see"])
    async def assignment_display_command(self, ctx, *, name: str):
        embed = self.display_assignment("Displaying an Assignment", ctx.author.id, name)

        await ctx.send(embed=embed)

    
    @assignment_group.command(name="display-all", aliases=["view-all", "see-all", "all"])
    async def assignment_display_all_command(self, ctx, target: t.Optional[t.Union[discord.Member, str]]):
        target = target or ctx.author
        if target != ctx.author and self.bot.guild.get_role(832910076972630106) not in target.roles and self.bot.guild.get_role(832910125329022977) in target.roles:
            await ctx.send("That user's list is private")
            return

        assignments = db.records("SELECT Name, DueDate, Completed FROM assignments WHERE UserID = ?",
                      target.id
        )

        embed = Embed(title=f"{target.name}'s Assignments")
        for assignment in assignments:
            embed.add_field(name=f"{assignment[0]}", value=f"Due on {assignment[1]}\nCompleted: {assignment[2]}", inline=False)

        await ctx.send(embed=embed)


    def display_assignment(self, title: str, UserID: int, name: str):
        try:
            due_date, completion = db.record("SELECT DueDate, Completed FROM assignments WHERE UserID = ? AND Name = ?",
                                UserID,
                                name
            )
        except:
            return Embed(title="No Assignment Found")

        embed = Embed(title=title,)
        embed.add_field(name=f"**{name}**", value=f"Due: {due_date}\nCompleted: {completion}", inline=True)

        return embed

    @assignment_group.command(name="completed")
    async def assignment_update_completion_command(self, ctx, name: str, newState: str):
        embed = self.update_completion_command(ctx, name, newState)

        await ctx.send(embed=embed)

    def update_completion_command(self, ctx, name: str, newState: str):
        due_date = db.record("SELECT DueDate FROM assignments WHERE UserID = ? AND Name = ?",
                              ctx.author.id,
                              name
                    )
        db.execute(
            "UPDATE assignments SET Completed = ? WHERE Name = ?",
            newState,
            name
        )

        embed = Embed(title="Assignment's Completion Changed")
        embed.add_field(name=f"**{name}**", value=f"Due: {due_date[0]}\nCompleted: {newState}", inline=True)

        return embed


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("assignments")

def setup(bot):
    bot.add_cog(Assignments(bot))