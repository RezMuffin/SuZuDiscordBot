import discord
from discord import app_commands
from discord import colour
from discord.ext import commands
from discord.embeds import Embed
from pypresence import Presence
import time
import random
import DiscordUtils
import asyncio
import yt_dlp as youtube_dl
import os
from help_cmd import help_cmd
from music import music_cmd
import youtube_dl
from yt_dlp import YoutubeDL

client = commands.Bot(command_prefix='rz! ', intents=discord.Intents.all())
music = DiscordUtils.Music()
client.remove_command('help')


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name="rz! for command"))
  print("Bot is Online")
  await client.add_cog(help_cmd(client))
  await client.add_cog(music_cmd(client))
  try:
    synced = await client.tree.sync()
    print(f"synced{len(synced)}command(s)")
  except Exception as e:
    print(e)


#test
@client.command()
async def hello(ctx):
  await ctx.send("Hi!")


#absen
@client.command()
async def absen(ctx):
  username = ctx.message.author.mention
  await ctx.send("Ada " + username)

#poke
@client.command()
async def poke(ctx):
  username = ctx.message.author.mention

  await ctx.send("WTF?! STOP IT " + username + "😠")


#Gif
mad_gif = [
  'https://media.tenor.com/gBLiDuugyrMAAAAC/haruhi-suzumiya-haruhi.gif',
  'https://media1.tenor.com/m/iYNJR0wL_s8AAAAC/melancholy-haruhi-suzumiya.gif',
  'https://media1.tenor.com/m/e0-bLlepygYAAAAC/angry-yelling.gif'
]
happy_gif = [
  'https://media.tenor.com/bnQLFSkqAhoAAAAC/haruhi-win.gif',
  'https://media.tenor.com/uMU9hNEw_zQAAAAC/haruhi-melancholy.gif'
]
poke_gif =[
  'https://media1.tenor.com/m/xxYMTHpOvz4AAAAC/haruhi-suzumiya-haruhi.gif'
]
tangi_gif = [
   'https://media1.tenor.com/m/pbzPHcx81nkAAAAC/haruhi-suzumiya-waking-up.gif'
]

@client.hybrid_command()
async def madat(ctx,target: discord.Member):
  embed = discord.Embed(
    colour=(discord.Colour.random()),
    description=f" {ctx.author.mention} is now mad at {target.mention}")
  embed.set_image(url=(random.choice(mad_gif)))
  await ctx.send(embed=embed)

@client.hybrid_command()
async def mad(ctx):
  embed = discord.Embed(
    colour=(discord.Colour.random()),
    description=f" {ctx.author.mention} is now mad")
  embed.set_image(url=(random.choice(mad_gif)))
  await ctx.send(embed=embed)

@client.hybrid_command()
async def pokeuser(ctx,target: discord.Member):
  embed = discord.Embed(
    colour=(discord.Colour.random()),
    description=f" {ctx.author.mention} poke {target.mention}")
  embed.set_image(url=(random.choice(poke_gif)))
  await ctx.send(embed=embed)

@client.hybrid_command()
async def yay(ctx):
  embed = discord.Embed(colour=(discord.Colour.random()))
  embed.set_image(url=(random.choice(happy_gif)))
  await ctx.send(embed=embed)

@client.hybrid_command()
async def tangi(ctx,target: discord.Member):
  embed = discord.Embed(
    colour=(discord.Colour.random()),
    description=f" {target.mention} tangi woy!")
  embed.set_image(url=(random.choice(tangi_gif)))
  await ctx.send(embed=embed)


# Slash Command
@client.tree.command(name="say")
@app_commands.describe(thing_to_say="What Should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
  await interaction.response.send_message(f"{thing_to_say}")

@client.tree.command(name="serverinfo")
async def server_info(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"Informasi server {guild.name}")
    embed.add_field(name="Server Name", value=guild.name)
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Total Member", value=guild.member_count)
    embed.add_field(name="Owner", value=guild.owner)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# @client.tree.command(name="poll")
# @app_commands.describe(question="Pertanyaan", option1="Opsi 1", option2="Opsi 2")
# async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str):
#     embed = discord.Embed(title=question, description=f"1️⃣ {option1}\n2️⃣ {option2}")
#     poll_message = await interaction.response.send_message(embed=embed)
#     await poll_message.add_reaction("1️⃣")
#     await poll_message.add_reaction("2️⃣")

# Invite Button
#anda bisa mengganti ini ke link yang anda mau
class InviteButton(discord.ui.View):
  def __init__(self, inv: str):
    super().__init__()
    self.inv = inv
    self.add_item(
      discord.ui.Button(label="Roti",
                        url="https://www.youtube.com/shorts/JNEAukTO9k4"))

  @discord.ui.button(label="Saint Invite Link",
                     style=discord.ButtonStyle.blurple)
  async def inviteSaint(self, interaction: discord.Interaction,
                        button: discord.ui.Button):
    await interaction.response.send_message(
      content="https://discord.gg/dFUx4w5", ephemeral=True)
      
  # async def inviteBtn(self, interaction: discord.Interaction,
  #                     button: discord.ui.Button):
  #   await interaction.response.send_message(self.inv, ephemeral=True)

  @discord.ui.button(label="My YT channel", style=discord.ButtonStyle.green)
  async def inviteYT(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
    await interaction.response.send_message(
      content="https://www.youtube.com/channel/UCasyDhK0j3BFt-puGHw74TA", ephemeral=True)


@client.command()
async def invite(ctx: commands.Context):
  inv = await ctx.channel.create_invite()
  await ctx.send("Pilih Tombol dibawah untuk Invite Link!",
                 view=InviteButton(str(inv)))


# profil

@client.tree.context_menu()
async def KTP(interaction: discord.Interaction, member: discord.Member):
  embed = discord.Embed(title=f"{member.name}#{member.discriminator}")
  embed.add_field(name="Joined Discord",
                  value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                  inline=False)
  embed.add_field(name="Joined Server",
                  value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
                  inline=False)
  embed.add_field(name="Roles",
                  value=", ".join([role.mention for role in member.roles]),
                  inline=False)
  embed.add_field(name="Badges",
                  value=", ".join(
                    [badge.name for badge in member.public_flags.all()]),
                  inline=False)
  embed.add_field(name="Activity", value=member.activity)
  embed.set_thumbnail(url=member.avatar.url)
  await interaction.response.send_message(embed=embed, ephemeral=True)



# Token
#buat file lokal dengan nama token.txt dan isi dengan token discord anda token bersifat private
with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()

# Run the bot
client.run(TOKEN)

