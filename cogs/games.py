import discord
from discord.ext import commands
import json
import random
import asyncio

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guess")
    async def guess_character(self, ctx):
        """Guess the Dragon Ball character game"""
        with open('data/characters.json') as f:
            characters = json.load(f)
        
        char = random.choice(characters)
        hints = [f"🔹 Race: {char['race']}"]
        
        if 'transformations' in char and char['transformations']:
            hints.append(f"🔹 Transformations: {', '.join(char['transformations'][:2])}")
        
        power_range = f"{char['power_level'] - 1000:,} - {char['power_level'] + 1000:,}"
        hints.append(f"🔹 Power Level Range: {power_range}")
        
        embed = discord.Embed(title="🎯 Tebak Karakter Dragon Ball!", color=0x9932CC)
        embed.description = "Tebak nama karakter berdasarkan petunjuk berikut:"
        embed.add_field(name="Petunjuk", value="\n".join(hints), inline=False)
        embed.set_footer(text="Waktu: 30 detik")
        
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            guess = await self.bot.wait_for("message", check=check, timeout=30.0)
            if guess.content.lower() == char["name"].lower():
                embed = discord.Embed(title="🎉 Benar!", color=0x00FF00)
                embed.description = f"Selamat! Karakter itu adalah **{char['name']}**"
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="❌ Salah!", color=0xFF0000)
                embed.description = f"Karakter itu adalah **{char['name']}**"
                await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="⏰ Waktu Habis!", color=0xFFFF00)
            embed.description = f"Karakter itu adalah **{char['name']}**"
            await ctx.send(embed=embed)

    @commands.command(name="powerguess")
    async def guess_power_level(self, ctx):
        """Guess the power level game"""
        with open('data/characters.json') as f:
            characters = json.load(f)
        
        char = random.choice(characters)
        
        embed = discord.Embed(title="⚡ Tebak Power Level!", color=0xFF6347)
        embed.description = f"Berapa power level **{char['name']}**?"
        embed.set_footer(text="Waktu: 20 detik")
        
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
        
        try:
            guess = await self.bot.wait_for("message", check=check, timeout=20.0)
            guess_num = int(guess.content)
            actual_power = char['power_level']
            
            difference = abs(guess_num - actual_power)
            percentage_diff = (difference / actual_power) * 100
            
            if percentage_diff <= 5:
                embed = discord.Embed(title="🎯 Sempurna!", color=0x00FF00)
                embed.description = f"Power level {char['name']}: **{actual_power:,}**\nTebakan Anda hampir tepat!"
            elif percentage_diff <= 20:
                embed = discord.Embed(title="👍 Bagus!", color=0xFFD700)
                embed.description = f"Power level {char['name']}: **{actual_power:,}**\nTebakan Anda cukup dekat!"
            else:
                embed = discord.Embed(title="❌ Coba Lagi!", color=0xFF0000)
                embed.description = f"Power level {char['name']}: **{actual_power:,}**\nTebakan Anda: **{guess_num:,}**"
            
            await ctx.send(embed=embed)
            
        except asyncio.TimeoutError:
            embed = discord.Embed(title="⏰ Waktu Habis!", color=0xFFFF00)
            embed.description = f"Power level **{char['name']}** adalah **{char['power_level']:,}**"
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Games(bot))