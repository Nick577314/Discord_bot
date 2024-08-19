import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from help_cog import help_cog
from music_cog import music_cog
from scrap_apex_cog import TournamentCog 
from scrap_cs2_cog import Cs2_cog

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

if discord_token is None:
    raise ValueError("Discord token not found. Please set it in the .env file.")

bot = commands.Bot(command_prefix="/", intents=intents)
bot.remove_command("help")

async def load_cogs():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(TournamentCog(bot))
    await bot.add_cog(Cs2_cog(bot))

async def main():
    async with bot:
        await load_cogs()
        await bot.start(discord_token)
        

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
