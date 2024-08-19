import requests
from discord.ext import commands
from discord import Embed
from bs4 import BeautifulSoup

class Cs2_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = 'https://liquipedia.net/counterstrike'

        self.s_tier_urls = [
            'https://liquipedia.net/counterstrike/Perfect_World/Major/2024/Shanghai',
            'https://liquipedia.net/counterstrike/BLAST/Premier/2024/World_Final',
            'https://liquipedia.net/counterstrike/Thunderpick/World_Championship/2024',
            'https://liquipedia.net/counterstrike/Intel_Extreme_Masters/2024/Rio',
            'https://liquipedia.net/counterstrike/BLAST/Premier/2024/Fall',
            'https://liquipedia.net/counterstrike/ESL/Pro_League/Season_20',
            'https://liquipedia.net/counterstrike/Intel_Extreme_Masters/2024/Cologne',
            'https://liquipedia.net/counterstrike/BLAST/Premier/2024/Fall/Groups',
            'https://liquipedia.net/counterstrike/Esports_World_Cup/2024',
        ]

    @commands.command(name='cs2_tournaments')
    async def cs2_tournaments(self, ctx, year: int, *stages):
        embed = Embed(title=f"CS2 {year} Tournaments", color=0x00ff00)
        
        for link in self.s_tier_urls:
            for stage in stages:
                data = self.get_tournament_data(link, stage)
                formatted_data = self.format_tournament_data(data)
                embed.add_field(name=f"{link} - {stage}", value=formatted_data or "No data found", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='cs2_opening_stage')
    async def cs2_opening_stage(self, ctx):
        embed = Embed(title="CS2 Opening Stage Tournaments", color=0x00ff00)
        
        for link in self.s_tier_urls:
            data = self.get_tournament_data(link, 'Opening_Stage')
            formatted_data = self.format_tournament_data(data)
            embed.add_field(name=link, value=formatted_data or "No data found", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='cs2_playin_stage')
    async def cs2_playin_stage(self, ctx):
        embed = Embed(title="CS2 Play-in Stage Tournaments", color=0x00ff00)
        
        for link in self.s_tier_urls:
            data = self.get_tournament_data(link, 'Play-in_Stage')
            formatted_data = self.format_tournament_data(data)
            embed.add_field(name=link, value=formatted_data or "No data found", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='cs2_playoffs')
    async def cs2_playoffs(self, ctx):
        embed = Embed(title="CS2 Playoffs Tournaments", color=0x00ff00)
        
        for link in self.s_tier_urls:
            data = self.get_tournament_data(link, 'Playoffs')
            formatted_data = self.format_tournament_data(data)
            embed.add_field(name=link, value=formatted_data or "No data found", inline=False)
        
        await ctx.send(embed=embed)






