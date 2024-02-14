# Importing packages and local utils
import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
from utils import fetch_from_tldr, write_to_txt_file

# Initializing things
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

# Constants
categories = ['tech', 'marketing', 'founders', 'design']

# Bot wrapper functions
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command()
async def help(ctx):
    response = discord.Embed(
                title="How to fetch news?",
                description="""The `!fetch` command needs to be used as follows:
                ```!fetch <category> <YYYY-MM-DD>```
                **Categories** involve tech, marketing, founders, design
                **Date** should be in YYYY-MM-DD format. Do not use today's date!!!
                """,
                colour=discord.Colour.purple()
            )
    await ctx.send(embed=response)
    
@bot.command()
async def fetch(ctx, category, date):
    if category in categories:
            res = fetch_from_tldr(category, date)
            if len(res)==3:
                # Writing results to file
                write_to_txt_file(res['headlines'], res['contents'], res['urls'])
                
                response = """"""
                total_news = len(res['headlines'])
                for i in range(total_news):
                    response += f"""# {res['headlines'][i]}
                    `Full article: {res['urls'][i]}`
                    {res['contents'][i]}\n"""
                await ctx.send(file=discord.File("./content.txt"))
            else:
                response = discord.Embed(
                    title="Invalid Date",
                    description=f"Unfortunately no news can be fetched for the date {date}")
                await ctx.send(embed=response)
    
# keep_alive()
bot.run(DISCORD_TOKEN)