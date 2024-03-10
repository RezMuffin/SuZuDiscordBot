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

@client.command()
async def madat(ctx,target: discord.Member):
  embed = discord.Embed(
    colour=(discord.Colour.random()),
    description=f" {ctx.author.mention} is now mad at {target.mention}")
  embed.set_image(url=(random.choice(mad_gif)))
  await ctx.send(embed=embed)

@client.command()
async def mad(ctx):
  embed = discord.Embed(
    colour=(discord.Colour.random()),
    description=f" {ctx.author.mention} is now mad")
  embed.set_image(url=(random.choice(mad_gif)))
  await ctx.send(embed=embed)

@client.command()
async def pokeuser(ctx,target: discord.Member):
  embed = discord.Embed(
    colour=(discord.Colour.random()),
    description=f" {ctx.author.mention} poke {target.mention}")
  embed.set_image(url=(random.choice(poke_gif)))
  await ctx.send(embed=embed)

@client.command()
async def yay(ctx):
  embed = discord.Embed(colour=(discord.Colour.random()))
  embed.set_image(url=(random.choice(happy_gif)))
  await ctx.send(embed=embed)

@client.command()
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


# music
# youtube_dl.utils.bug_reports_message = lambda: ''

# ytdlopts = {
#   'format': 'bestaudio/best',
#   'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
#   'restrictfilenames': True,
#   'noplaylist': True,
#   'nocheckcertificate': True,
#   'ignoreerrors': False,
#   'logtostderr': False,
#   'quiet': True,
#   'no_warnings': True,
#   'default_search': 'auto',
#   'source_address': '0.0.0.0',
#   # 'force-ipv4': True,
#   # 'preferredcodec': 'mp3',
#   # 'cachedir': False
# }

# ffmpeg_options = {'options': '-vn'}

# ytdl = youtube_dl.YoutubeDL(ytdlopts)


# @client.command()
# async def play(ctx, *, query):

  # try:
  #   voice_channel = ctx.author.voice.channel  #checking if user is in a voice channel
  # except AttributeError:
  #   return await ctx.send("Masuk voice channel dulu bodoh!"
  #                         )  #member is not in a voice channel

  # permissions = voice_channel.permissions_for(ctx.me)
  # if not permissions.connect or not permissions.speak:
  #   await ctx.send("Aku tidak punya hak untuk bersamamu maaf ")
  #   return

  # voice_client = ctx.guild.voice_client
  # if not voice_client:
  #   await voice_channel.connect()
  #   voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)

  # loop = asyncio.get_event_loop()
  # data = await loop.run_in_executor(
  #   None, lambda: ytdl.extract_info(url=query, download=False)
  # )  #extracting the info and not downloading the source

  # title = data['title']
  # song = data['url']

  # if 'entries' in data:
  #   data = data['entries'][0]

  # try:
  #   voice_client.play(
  #     discord.FFmpegPCMAudio(source=song,
  #                            **ffmpeg_options,
  #                            executable="ffmpeg.exe"))  #playing the audio
  # except Exception as e:
  #   print(e)

  # await ctx.send(f'**Now playing:** {title}')


# @client.command()
# async def join(ctx):
#   voicetrue = ctx.author.voice
#   if voicetrue is None:
#     return await ctx.send("Masuk voice channel dulu bodoh!")
#   await ctx.author.voice.channel.connect()
#   await ctx.send("SuZu telah Masuk ke voice channel")


# @client.command()
# async def leave(ctx):
#   voicetrue = ctx.author.voice
#   novoicetrue = ctx.guild.me.voice
#   if voicetrue is None:
#     return await ctx.send("Kok aku kamu tinggal keluar sih dasar bodoh!")
#   if novoicetrue is None:
#     return await ctx.send("Aku sedang tidak di voice channel bodoh!")
#   await ctx.voice_client.disconnect()
#   await ctx.send('SuZu telah keluar dari Voice channel')


# @client.command()
# async def play(ctx, *, url):
#     player = music.get_player(guild_id=ctx.guild.id)
#     if not player:
#         player = music.create_player(ctx, ffmpeg_error_betterfix=True)

#     try:
#         if not ctx.voice_client.is_playing():
#             song = await player.queue(url, search=True)
#             if song:
#                 await player.play()
#                 await ctx.send(f"SuZu mulai memutar `{song.name}`")
#             else:
#                 await ctx.send("Tidak dapat menambahkan lagu ke playlist.")
#         else:
#             song = await player.queue(url, search=True)
#             if song:
#                 await ctx.send(f"`{song.name}` Sudah ada di Playlist")
#             else:
#                 await ctx.send("Tidak dapat menambahkan lagu ke playlist.")
#     except Exception as e:
#         await ctx.send(f"Terjadi kesalahan: {e}")
####
# async def play(ctx, *, url):
#     player = music.get_player(guild_id=ctx.guild.id)
#     if not player:
#         player = music.create_player(ctx, ffmpeg_error_betterfix=True)
#     if not ctx.voice_client.is_playing():
#         await player.queue(url, search=True)
#         song = await player.play()
#         await ctx.send(f"SuZU mulai memutar `{song.name}`")
#     else:
#         song = await player.queue(url, search=True)
#         await ctx.send(f"`{song.name}` Sudah ada di Playlist")

# ####
# @client.command(name='pause')
# async def pause(ctx):
#   """Pause Musik"""
#   vc = ctx.voice_client

#   if not vc or not vc.is_playing():
#     embed = discord.Embed(title="",
#                           description="Aku sedang tidak memutar musik",
#                           color=discord.Color.green())
#     return await ctx.send(embed=embed)
#   elif vc.is_paused():
#     return

#   vc.pause()
#   await ctx.send("Paused ⏸️")


# @client.command(name='resume')
# async def resume(ctx):
#   """Melanjutkan Musik"""
#   vc = ctx.voice_client

#   if not vc or not vc.is_connected():
#     embed = discord.Embed(title="",
#                           description="Aku sedang tidak di voice channel",
#                           color=discord.Color.green())
#     return await ctx.send(embed=embed)
#   elif not vc.is_paused():
#     return

#   vc.resume()
#   await ctx.send("Resuming ⏯️")




# Token
#buat file lokal dengan nama token.txt dan isi dengan token discord anda token bersifat private
with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()

# Run the bot
client.run(TOKEN)

