import discord
from discord.ext import commands
import json
import random

class Characters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_character(self, name):
        """Get character data by name"""
        with open('data/characters.json') as f:
            characters = json.load(f)
        return next((c for c in characters if c["name"].lower() == name.lower()), None)

    @commands.command(name="char")
    async def show_character(self, ctx, *, name):
        """Show character information"""
        char = self.get_character(name)
        
        if char:
            embed = discord.Embed(title=char["name"], color=0xFF0000)
            embed.add_field(name="Race", value=char["race"], inline=True)
            embed.add_field(name="Power Level", value=f"{char['power_level']:,}", inline=True)
            
            if "transformations" in char:
                embed.add_field(name="Transformations", value=", ".join(char["transformations"]), inline=False)
            
            if "image_url" in char:
                embed.set_image(url=char["image_url"])
            
            embed.set_footer(text="Dragon Ball Bot")
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Karakter tidak ditemukan!")

    @commands.command(name="fight")
    async def fight(self, ctx, char1_name, *, char2_name):
        """Simulate a fight between two characters"""
        char1 = self.get_character(char1_name)
        char2 = self.get_character(char2_name)
        
        if not char1 or not char2:
            await ctx.send("❌ Salah satu karakter tidak valid!")
            return
        
        result = self.simulate_fight(char1, char2)
        
        embed = discord.Embed(title="⚔️ Pertarungan Dragon Ball", color=0xFF4500)
        embed.add_field(name="Fighter 1", value=f"{char1['name']} (Power: {char1['power_level']:,})", inline=True)
        embed.add_field(name="Fighter 2", value=f"{char2['name']} (Power: {char2['power_level']:,})", inline=True)
        embed.add_field(name="Winner", value=f"🏆 {result['winner']}", inline=False)
        embed.add_field(name="Battle Details", value=result['details'], inline=False)
        
        # Update leaderboard if user chose char1
        leaderboard_cog = self.bot.get_cog('Leaderboard')
        if leaderboard_cog:
            user_won = result['winner'] == char1['name']
            leaderboard_cog.update_battle_result(
                ctx.author.id, 
                ctx.author.display_name, 
                char1['name'], 
                char2['name'], 
                user_won
            )
        
        await ctx.send(embed=embed)

    def simulate_fight(self, char1, char2):
        """Simulate fight between characters"""
        # Add some randomness to make fights more interesting
        char1_power = char1['power_level'] * random.uniform(0.8, 1.2)
        char2_power = char2['power_level'] * random.uniform(0.8, 1.2)
        
        if char1_power > char2_power:
            winner = char1['name']
            power_diff = ((char1_power - char2_power) / char2_power) * 100
        else:
            winner = char2['name']
            power_diff = ((char2_power - char1_power) / char1_power) * 100
        
        if power_diff > 50:
            details = f"{winner} menang dengan mudah! Kekuatan terlalu berbeda jauh."
        elif power_diff > 20:
            details = f"{winner} menang setelah pertarungan yang cukup sengit."
        else:
            details = f"Pertarungan yang sangat seru! {winner} menang tipis."
        
        return {
            'winner': winner,
            'details': details
        }

    @commands.command(name="list_chars")
    async def list_characters(self, ctx):
        """List all available characters"""
        with open('data/characters.json') as f:
            characters = json.load(f)
        
        char_list = [f"• {char['name']} (Power: {char['power_level']:,})" for char in characters]
        
        embed = discord.Embed(title="📋 Daftar Karakter Dragon Ball", color=0x00FF00)
        embed.description = "\n".join(char_list)
        embed.set_footer(text=f"Total: {len(characters)} karakter")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Characters(bot))