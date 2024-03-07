import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import asyncio
from discord import FFmpegPCMAudio

class music_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {'options': '-vn'}
        # self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        #                       'options': '-vn -volume 1.0'}
        self.vc = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    #search link Youtube
    def search_yt(self, item):
        if item.startswith("https://"):
            title = self.ytdl.extract_info(item, download=False)["title"]
            return {'source': item, 'title': title}
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
            except Exception as e:
                print(e)
                return None
            return {'source': info['formats'][0]['url'], 'title': info['title']}
    #play next
    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False
    #play dan queue
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            #connect ke VC dan play 
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

               
                if self.vc == None:
                    await ctx.send("SuZu gagal join voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            #hilangin queue no 1
            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
           
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing"], help="SuZu Join voice channel dan play musik")
    async def play(self, ctx, *args):
        query = " ".join(args)
        try:
            voice_channel = ctx.author.voice.channel
        except:
            await ctx.send("Masuk voice channel dulu bodoh!🫵😡")
            return
        if self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("SuZu tidak bisa mendownload music.")
            else:
                if self.is_playing:
                    await ctx.send(f"**#{len(self.music_queue)+2} -'{song['title']}'** sudah masuk ke queue")  
                else:
                    await ctx.send(f"**'{song['title']}'** sudah masuk ke queue")  
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)
    #pause lagu
    @commands.command(name="pause", help="SuZu pause music")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.send("Paused ⏸️")
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
    #resume lagu
    @commands.command(name = "resume", aliases=["r"], help="SuZu resume music")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await ctx.send("Resuming ⏯️")
    #Skip lagu
    @commands.command(name="skip", aliases=["s"], help="SuZu skip music")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #memutar lagu selanjutnya jika ada 
            await self.play_music(ctx)
    #menampilkan queue
    @commands.command(name="queue", aliases=["q"], help="SuZu menampilkan queue music")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"#{i+1} -" + self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(f"```queue:\n{retval}```")
        else:
            await ctx.send("Tidak ada musik di queue")
    #clear queue music
    @commands.command(name="clear", aliases=["c", "bin"], help="SuZu stop dan clear music")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music sudah hilang dari peradaban")
    #stop/disconect bot
    @commands.command(name="stop", aliases=["disconnect","leave", "l", "dc"], help="SuZu keluar voice channel")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        await ctx.send("SuZu keluar voice channel")
    #remove lagu terakhir dari queue
    @commands.command(name="remove", help="SuZu remove musik terakhir di queue")
    async def re(self, ctx):
        self.music_queue.pop()
        await ctx.send("Yahaha lagumu sudah hilang dari queue")



#tutorial i use -> https://www.youtube.com/watch?v=dRHUW_KnHLs