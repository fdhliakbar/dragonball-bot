import discord
from discord.ext import commands
import json
import random

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="quote")
    async def random_quote(self, ctx):
        """Get a random Dragon Ball quote"""
        with open('data/quotes.json') as f:
            quotes = json.load(f)
        
        quote = random.choice(quotes)
        
        embed = discord.Embed(color=0xFFD700)
        embed.add_field(name="💬 Quote", value=f'"{quote["text"]}"', inline=False)
        embed.add_field(name="👤 Character", value=quote["character"], inline=True)
        embed.set_footer(text="Dragon Ball Quotes")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Quotes(bot))