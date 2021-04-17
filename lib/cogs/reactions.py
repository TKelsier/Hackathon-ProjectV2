from discord.ext.commands import Cog

settings = {
    "🧠": 832909936107323392,
    "🔓": 832910076972630106,
}
class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("reactions")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.ready and payload.message_id == self.bot.reaction_message.id:
            role1 = self.bot.guild.get_role(settings[payload.emoji.name])
            await payload.member.add_roles(role1, reason = "Settings role reaction")
            if role1 == 832910125329022977:
                role2 = self.bot.guild.get_role(832910125329022977)
                await payload.member.remove_roles(role2, reason = "Settings role reaction.")


    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if self.bot.ready and payload.message_id == self.bot.reaction_message.id:
            member = self.bot.guild.get_member(payload.user_id)
            role1 = self.bot.guild.get_role(settings[payload.emoji.name])
            await member.remove_roles(role1, reason = "Settings role reaction.")
            if role1 == 832910125329022977:
                role2 = self.bot.guild.get_role(832910125329022977)
                await payload.member.add_roles(role2, reason = "Settings role reaction.")

def setup(bot):
    bot.add_cog(Reactions(bot))
