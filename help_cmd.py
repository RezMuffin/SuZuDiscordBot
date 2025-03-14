import discord
from discord.ext import commands

class help_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = ""
        self.text_channel_list = []
        self.set_message()
    #hapus default help
    def set_message(self):
        self.help_message = f"""
```
General commands:
{self.bot.command_prefix}help - Menampilkan Semua Command Bot SuZu
{self.bot.command_prefix}hello - menyapa SuZu
{self.bot.command_prefix}absen - Absen adick-adick
{self.bot.command_prefix}poke - Poke SuZu
{self.bot.command_prefix}invite - Menampilkan label Invite
{self.bot.command_prefix}play - SuZu join voice channel dan play musik
{self.bot.command_prefix}stop/disconnect - SuZu keluar voice channel
{self.bot.command_prefix}pause - SuZu pause music 
{self.bot.command_prefix}resume - SuZu resume music
{self.bot.command_prefix}skip - SuZu skip music
{self.bot.command_prefix}queue - SuZu menampilkan queue music
{self.bot.command_prefix}disconnect - SuZu stop dan clear music
{self.bot.command_prefix}remove - SuZu remove musik terakhir di queue
/say - SuZu ngomong
KTP member - Klik kanan Member -> apps-> KTP

GIF commands:
{self.bot.command_prefix}mad - marah😡
{self.bot.command_prefix}madat - marah ke @taguser😡
{self.bot.command_prefix}pokeuser - poke @taguser
{self.bot.command_prefix}yay - YAY!
{self.bot.command_prefix}tangi - @taguser bangun bang



```
"""

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(f"type {self.bot.command_prefix}help"))

    @commands.command(name="help", help="Menampilkan Semua Command Bot SuZu")
    async def help(self, ctx):
        await ctx.send(self.help_message)
    
    # @commands.command(name="prefix", help="Change bot prefix")
    # async def prefix(self, ctx, *args):
    #     self.bot.command_prefix = " ".join(args)
    #     self.set_message()
    #     await ctx.send(f"prefix set to **'{self.bot.command_prefix}'**")
    #     await self.bot.change_presence(activity=discord.Game(f"type {self.bot.command_prefix}help"))

    @commands.command(name="send_to_all", help="send a message to all members")
    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)
