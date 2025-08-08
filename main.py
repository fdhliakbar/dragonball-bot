import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup - Basic intents only
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

# Load cogs
async def load_cogs():
    await bot.load_extension('cogs.help')  # Load help first to override default
    await bot.load_extension('cogs.characters')
    await bot.load_extension('cogs.quotes')
    await bot.load_extension('cogs.games')
    await bot.load_extension('cogs.leaderboard')
    # await bot.load_extension('cogs.music')  # Temporarily disabled due to audioop issue

async def main():
    await load_cogs()
    await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())