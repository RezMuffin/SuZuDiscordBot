import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import asyncio
from discord import FFmpegPCMAudio
import youtube_dl

class music_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'quiet': True,
            'default_search': 'ytsearch',
            'extract_flat': False,
            'noplaylist': True,
            'source_address': '0.0.0.0',  # Bind ke IPv4 untuk menghindari masalah dengan IPv6
            'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'} ,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',}
            ]
        }
        # self.YDL_OPTIONS = {
        #     'format': 'bestaudio/best',
        #     'quiet': True,
        #     'default_search': 'auto',
        #     'noplaylist': True
        # }
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    # Search YouTube
    def search_yt(self, item):
        try:
            # input -> link
            if item.startswith("http://") or item.startswith("https://"):
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(item, download=False)
                return {'source': info['url'], 'title': info['title']}
            else:
                # input -> search
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
                return {'source': info['url'], 'title': info['title']}
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return None


    # Play next song dari queue
    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            song = self.music_queue.pop(0)
            m_url = song['source']

            try:
                self.vc.play(
                    discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                    after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop)
                )
            except Exception as e:
                print(f"Error playing next song: {e}")
                self.is_playing = False
        else:
            self.is_playing = False

    # Play or queue music
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            song = self.music_queue[0]
            m_url = song['source']

            if self.vc is None or not self.vc.is_connected():
                self.vc = await song['voice_channel'].connect()
                await ctx.send("SuZu telah bergabung ke Voice channel 😊")

            if self.vc is None:
                await ctx.send("SuZu tidak dapat bergabung ke Voice channel😥")
                return

            self.music_queue.pop(0)

            try:
                self.vc.play(
                    discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                    after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop)
                )
            except Exception as e:
                print(f"Error playing song: {e}")
                self.is_playing = False
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p", "playing"], help="Memutar lagu dan menambahkan ke queue")
    async def play(self, ctx, *args):
        query = " ".join(args)

        try:
            voice_channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send("Masuk voice channel dulu bodoh!🫵😡")
            return

        song = self.search_yt(query)
        if song is None:
            await ctx.send("SuZu tidak dapat memutar lagu, terjadi kesalahan format")
        else:
            song['voice_channel'] = voice_channel
            self.music_queue.append(song)

            if not self.is_playing:
                await self.play_music(ctx)
                await ctx.send(f"Lagu telah diputar: **{song['title']}**")
            else:
                await ctx.send(f"Lagu ditambahkan ke queue: **{song['title']}**")

    @commands.command(name="pause", help="Pause lagu yang sedang diputar")
    async def pause(self, ctx):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.send("Suzu Paused⏸")
        else:
            await ctx.send("Palakau pause, kau sedang tidak memutar lagu bodoh!")

    @commands.command(name="resume", aliases=["r"], help="Melanjutkan Lagu")
    async def resume(self, ctx):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await ctx.send("SuZu Resume ⏯️")
        else:
            await ctx.send("Tidak ada lagu yang dipause")

    @commands.command(name="skip", aliases=["s"], help="Skip lagu")
    async def skip(self, ctx):
        if self.vc and self.vc.is_playing():
            self.vc.stop()
            await self.play_music(ctx)
        else:
            await ctx.send("Tidak ada musik yang diputar")

    @commands.command(name="queue", aliases=["q"], help="Mempelihatkan queue")
    async def queue(self, ctx):
        if len(self.music_queue) > 0:
            retval = "\n".join([f"#{i + 1} - {song['title']}" for i, song in enumerate(self.music_queue)])
            await ctx.send(f"```Queue:\n{retval}```")
        else:
            await ctx.send("Queue lagu kosong kaya otak lu 🫵😌")

    @commands.command(name="clear", aliases=["c", "bin"], help="Clear queue atau hapus lagu tertentu dari queue")
    async def clear(self, ctx, index: int = None):
        if index is None:
            # Menghapus seluruh queue
            self.music_queue = []
            if self.vc and self.vc.is_playing():
                self.vc.stop()
            await ctx.send("Lagu sudah hilang dari peradaban")
        else:
            # Menghapus lagu tertentu dari queue
            try:
                if index < 1 or index > len(self.music_queue):
                    await ctx.send(f"Tidak ada lagu pada nomor {index} dalam queue!")
                    return

                removed_song = self.music_queue.pop(index - 1)
                await ctx.send(f"Lagu **{removed_song['title']}** telah dihapus dari queue.")
            except ValueError:
                await ctx.send("Mohon berikan urutan lagu yang sesuai")

    @commands.command(name="stop", aliases=["disconnect", "leave", "l", "dc"], help="SuZu keluar voice channel")
    async def stop(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        await ctx.send("SuZu telah keluar dari voice channel 😴")



#tutorial i use -> https://www.youtube.com/watch?v=dRHUW_KnHLs
