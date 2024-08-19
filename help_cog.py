
import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_message = """
```
General Commands:
/help - displays all the available commands
/p <URL> - finds the song on YouTube and plays it in your current channel. Will resume
/q - displays the current music queue
/skip - skips the current song being played
/clear - stops the music and clears the queue
/leave - disconnects the bot from the voice channel
/pause - pauses the current song being played or resumes if already paused
/resume - resumes playing the current song

Apex Legends Commands:
/apex-rankings - displays overall rankings for Apex Legends esports
/Apex-matchday <number> - displays results and stats for a specific match day in Apex Legends esports
```
"""
        self.text_channels = []

    @commands.command(name="help", help="Displays all the available commands")
    async def help_command(self, ctx):
        await ctx.send(self.help_message)

    @commands.command(name="clean", help="Cleans the channel of messages")
    @commands.has_permissions(manage_messages=True)
    async def clean_channel(self, ctx, limit: int = 100):
        await ctx.channel.purge(limit=limit)
        await ctx.send(f"Deleted {limit} messages", delete_after=5)

def setup(bot):
    bot.add_cog(help_cog(bot))
    bot.add_command(clean_channel)


