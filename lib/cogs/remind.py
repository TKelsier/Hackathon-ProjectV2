from discord.ext.commands import Cog
from discord.ext import tasks, commands
from datetime import datetime
from datetime import date

from lib.db import db

class Remind(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminds.start()

    @tasks.loop(seconds=20.0)
    async def reminds(self):
        now = datetime.now()
        date_string = now.strftime("%m/%d/%Y %H:%M")
        current_date = date_string.replace(":", "/")
        current_date = current_date.replace(" ", "/")
        current_date = current_date.split("/")

        if current_date[0].startswith("0") and len(current_date[0]) == 2:
            current_date[0] = current_date[0].replace("0", "")

        if current_date[1].startswith("0") and len(current_date[1]) > 1:
            current_date[1] = current_date[1].replace("0", "")

        assignments = db.records("SELECT UserID, Name, DueDate FROM assignments")

        for assignment in assignments:
            due_date = assignment[2].replace(":", "/")
            due_date = due_date.replace(" ", "/")
            due_date = due_date.split("/")

            if due_date[0] == current_date[0] and due_date[1] == current_date[1] and due_date[2] == current_date[2]:
                if int(due_date[3]) - int(current_date[3]) == 1 and int(due_date[4]) - int(current_date[4]) == 0:
                    member = await self.bot.guild.fetch_member(assignment[0])
                    await member.send(f"{assignment[1]} is due in an hour!")
        

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("remind")

def setup(bot):
    bot.add_cog(Remind(bot))