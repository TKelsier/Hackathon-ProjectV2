from discord import Intents
from datetime import datetime
from glob import glob 
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from asyncio import sleep

from lib.db import db

PREFIX = "."
OWNER_IDS = [177856746721640448]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix = PREFIX,
            owner_ids = OWNER_IDS,
            intents = Intents.all()
        )
    
    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")

        print("setup complete")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("lib/bot/token.0", "r", encoding = "utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect = True)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.stdout.send("An error occured.")
        raise 

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc, "original"):
            raise exc.original
        
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(832762981443829781)
            self.stdout = self.get_channel(832780649571155969)
            self.scheduler.start()

            await self.stdout.send("Now online!")

            # embed = Embed(title="Now online!", description="Schoolio is now online.")
            # fields = [("Name", "Value", True),
            #           ("Another field", "This field is ne tot the other one.", True),
            #           ("A non-inline field", "This field will appear on it's own row.", False)
            # ]
            
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)

            # await channel.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            
            self.ready = True
            print("bot ready")

        else:
            print("bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()