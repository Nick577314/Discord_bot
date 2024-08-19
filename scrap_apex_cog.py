import requests
from discord.ext import commands
from discord import Embed
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import aiohttp

class TournamentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chromedriver_path = '/Users/nicolas_leffray/Desktop/discord/chromedriver_mac64/chromedriver'  # Update with your actual path
        self.match_day_urls = [
            'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america/65fc89113fce34803f734707/round/0/match/0',
            'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america/65fc89113fce34803f734707/round/1/match/1',
            'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america/65fc89113fce34803f734707/round/2/match/2',
            'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america/65fc89113fce34803f734707/round/3/match/3',
            'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america/65fc89113fce34803f734707/round/4/match/4',
            'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america/65fc89113fce34803f734707/round/5/match/5',
            'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america/65fc89113fce34803f734707/round/6/match/6',
            'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america/65fc89113fce34803f734707/round/7/match/7',
            'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america/65fc89113fce34803f734707/round/8/match/8',
            'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2-regional-finals/north-america/65fc89113fce34803f734707/round/9/match/9',
        ]

    def scrape_tournament_data(self):
        url = 'https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america'

        # Initialize Chrome WebDriver
        webdriver.chrome.driver = self.chromedriver_path
        driver = webdriver.Chrome()

        try:
            # Load the webpage
            driver.get(url)

            # Wait until 'qualified-teams' elements are present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'qualified-teams')))

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            tournament_data = []
            team_elements = soup.find_all('div', class_='qualified-teams')

            for team in team_elements:
                try:
                    rank_element = team.find('p')
                    rank = rank_element.text.strip() if rank_element else 'N/A'

                    logo_url = team.find('img')['src']
                    # Resize logo URL here
                    resized_logo_url = f"{logo_url}=s100"  # Adjust size as needed

                    team_name_element = team.find('p', class_='team-name')
                    team_name = team_name_element.text.strip() if team_name_element else 'N/A'

                    # Ensure there are enough <p> elements before accessing them
                    p_elements = team.find_all('p')
                    days_played = p_elements[2].text.strip() if len(p_elements) > 2 else 'N/A'  # Adjust index to get correct element
                    overall_points = p_elements[3].text.strip() if len(p_elements) > 3 else 'N/A'  # Adjust index to get correct element

                    team_data = {
                        "rank": rank,
                        "team_name": team_name,
                        "days_played": days_played,
                        "overall_points": overall_points,
                        "logo_url": resized_logo_url  # Use resized logo URL
                    }
                    tournament_data.append(team_data)
                
                except Exception as e:
                    print(f"Error processing team data: {e}")

            return tournament_data

        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            return []

        finally:
            # Close the WebDriver
            driver.quit()

    def scrape_match_day_data(self, url):
        # Initialize Chrome WebDriver
        webdriver.chrome.driver = self.chromedriver_path
        
        driver = webdriver.Chrome()

        try:
            # Load the webpage
            driver.get(url)

            # Wait until the necessary elements are present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-fwqlvj-TeamInfoWrapper')))

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            match_day_data = []
            team_elements = soup.find_all('div', class_='css-fwqlvj-TeamInfoWrapper')

            for team in team_elements:
                try:
                    rank = team.find('div', class_='css-1dut3q3-TeamRanking').text.strip()
                    logo_url = team.find('img')['src']
                    # Resize logo URL here
                    resized_logo_url = f"{logo_url}=s50"  # Adjust size as needed
                    team_name = team.find('span').text.strip()
                    stats_elements = team.find_all('div', class_='css-1ll8l8q-Result')
                    
                    points = stats_elements[0].find('div', class_='css-19rge6r-ResultValue').text.strip()
                    best_placement = stats_elements[1].find('div', class_='css-19rge6r-ResultValue').text.strip()
                    kills = stats_elements[2].find('div', class_='css-19rge6r-ResultValue').text.strip()
                    
                    team_data = {
                        "rank": rank,
                        "team_name": team_name,
                        "points": points,
                        "best_placement": best_placement,
                        "kills": kills,
                        "logo_url": resized_logo_url  # Use resized logo URL
                    }
                    match_day_data.append(team_data)
                
                except Exception as e:
                    print(f"Error processing team data: {e}")

            return match_day_data

        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            return []

        finally:
            # Close the WebDriver
            driver.quit()


    @commands.command(name="Overall_Rankings_Apex", aliases=["Apex-rankings"])
    async def tournament(self, ctx):
        max_teams_to_display = 13  # Adjust the number of teams to display
        try:
            data = self.scrape_tournament_data()
            if data:
                embed = Embed(title="Apex Legends Tournament - Overall Rankings", color=0x00FF00, url="https://battlefy.com/apex-legends-global-series-year-4/pro-league-split-2/north-america")
                for team in data[:max_teams_to_display]:
                    embed.add_field(name=f"Rank {team['rank']} - {team['team_name']}",
                                    value=f"Days Played: {team['days_played']}, Points: {team['overall_points']}",
                                    inline=False)
                embed.set_footer(text="")
                await ctx.send(embed=embed)
            else:
                await ctx.send("No data found.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="Match_Day_Results_Apex", aliases=["Apex-matchday"])
    async def match_day(self, ctx, day: int):
        max_teams_to_display = 10  # Adjust the number of teams to display
        if 1 <= day <= len(self.match_day_urls):
            url = self.match_day_urls[day - 1]
            try:
                data = self.scrape_match_day_data(url)
                if data:
                    embed = Embed(title=f"Apex Legends Match Day {day} Results", color=0xFF0000, url=url)
                    for team in data[:max_teams_to_display]:
                        embed.add_field(name=f"Rank {team['rank']} - {team['team_name']}",
                                        value=f"Points: {team['points']}, Best Placement: {team['best_placement']}, Kills: {team['kills']}",
                                        inline=False)
                    embed.set_footer(text="")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("No data found.")
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")
        else:
            await ctx.send(f"Invalid day number. Please provide a number between 1 and {len(self.match_day_urls)}.")

async def setup(bot):
    await bot.add_cog(TournamentCog(bot))














