
import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import traceback

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = None
        
        opus_path = '/usr/local/Cellar/opus/1.5.2/lib/libopus.dylib'
        discord.opus.load_opus(opus_path)
    def search_yt(self, item):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
                return {'source': info['url'], 'title': info['title']}
            except Exception as e:
                print(f"Error extracting info: {e}")
                return False

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            try:
                print(f"Attempting to play next song: {m_url}")
                if self.vc is not None and self.vc.is_connected():
                    self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
                    print("Audio playback started")
                else:
                    print("Voice client is not connected")
                    self.is_playing = False
            except discord.errors.ClientException as e:
                print(f"Discord Client Exception: {e}")
                traceback.print_exc()
                self.is_playing = False
            except Exception as e:
                print(f"Error playing audio: {e}")
                traceback.print_exc()
                self.is_playing = False
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                if self.vc is None:
                    await ctx.send("Could not connect to the voice channel")
                    return
                print("Bot connected to the voice channel")
            else:
                await self.vc.move_to(self.music_queue[0][1])
                print("Bot moved to the voice channel")
            self.music_queue.pop(0)

            print(f"Playing URL: {m_url}")
            try:
                if self.vc.is_connected():
                    self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
                    print("Audio playback started")
                else:
                    print("Voice client is not connected")
                    self.is_playing = False
            except discord.errors.ClientException as e:
                print(f"Discord Client Exception: {e}")
                traceback.print_exc()
                self.is_playing = False
            except Exception as e:
                print(f"Error playing audio: {e}")
                traceback.print_exc()
                self.is_playing = False
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p", "playing"], help="Play the selected song from YouTube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("You need to be connected to a voice channel!")
            return
        if self.is_paused:
            self.vc.resume()
            print("Resuming playback")
        else:
            song = self.search_yt(query)
            if song is False:
                await ctx.send("Could not download the song. Incorrect format, try a different keyword")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                if not self.is_playing:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            print("Pausing playback")
        elif self.is_paused:
            self.vc.resume()
            print("Resuming playback")

    @commands.command(name="resume", aliases=["r"], help="Resumes the current song being played")
    async def resume(self, ctx):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            print("Resuming playback")

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc is not None and self.vc.is_playing():
            self.vc.stop()
            print("Skipping current song")
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="Displays all the songs currently in the queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            if i > 4:
                break
            retval += self.music_queue[i][0]['title'] + '\n'
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue.")

    @commands.command(name="clear", aliases=["c"], help="Clears the queue")
    async def clear(self, ctx):
        if self.vc is not None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")
        print("Music queue cleared")

    @commands.command(name="leave", aliases=["disconnect"], help="Leaves the voice channel")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        print("Bot disconnected from the voice channel")

def setup(bot):
    bot.add_cog(music_cog(bot))



      

            

        
