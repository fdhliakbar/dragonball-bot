import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h", "commands"])
    async def show_help(self, ctx, category=None):
        """Show help information"""
        
        if not category:
            # Main help embed
            embed = discord.Embed(
                title="🐉 Dragon Ball Discord Bot",
                description="Bot Dragon Ball dengan berbagai fitur menarik!",
                color=0xFF6600
            )
            
            embed.add_field(
                name="📚 Categories",
                value=(
                    "`!help characters` - Karakter & Pertarungan\n"
                    "`!help games` - Mini Games\n" 
                    "`!help leaderboard` - Ranking & Stats\n"
                    "`!help music` - Voice & Music\n"
                    "`!help quotes` - Dragon Ball Quotes"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🚀 Quick Start",
                value=(
                    "`!char goku` - Info karakter\n"
                    "`!fight goku vegeta` - Simulasi pertarungan\n"
                    "`!quote` - Quote random\n"
                    "`!guess` - Tebak karakter"
                ),
                inline=False
            )
            
            embed.set_footer(text="Gunakan !help <category> untuk detail lebih lanjut")
            await ctx.send(embed=embed)
            return

        category = category.lower()
        
        if category == "characters":
            embed = discord.Embed(
                title="👥 Character Commands",
                color=0xFF0000
            )
            embed.add_field(
                name="Commands",
                value=(
                    "`!char <name>` - Tampilkan info karakter\n"
                    "`!fight <char1> <char2>` - Simulasi pertarungan\n"
                    "`!list_chars` - Daftar semua karakter"
                ),
                inline=False
            )
            embed.add_field(
                name="Contoh",
                value=(
                    "`!char Goku`\n"
                    "`!fight Goku Vegeta`\n"
                    "`!list_chars`"
                ),
                inline=False
            )
            
        elif category == "games":
            embed = discord.Embed(
                title="🎮 Game Commands",
                color=0x9932CC
            )
            embed.add_field(
                name="Commands", 
                value=(
                    "`!guess` - Tebak karakter dari petunjuk\n"
                    "`!powerguess` - Tebak power level karakter"
                ),
                inline=False
            )
            embed.add_field(
                name="Scoring",
                value=(
                    "Guess Game: Benar = 10 poin\n"
                    "Power Guess: Akurasi menentukan poin"
                ),
                inline=False
            )
            
        elif category == "leaderboard":
            embed = discord.Embed(
                title="🏆 Leaderboard Commands",
                color=0xFFD700
            )
            embed.add_field(
                name="Commands",
                value=(
                    "`!leaderboard` - Top 10 pemain\n"
                    "`!mystats` - Stats pribadi\n"
                    "`!battlehistory` - Riwayat pertarungan"
                ),
                inline=False
            )
            embed.add_field(
                name="Point System",
                value=(
                    "Menang pertarungan: +10 poin\n"
                    "Kalah pertarungan: +1 poin\n"
                    "Game berhasil: +5-15 poin"
                ),
                inline=False
            )
            
        elif category == "music":
            embed = discord.Embed(
                title="🎵 Music Commands", 
                color=0x00CED1
            )
            embed.add_field(
                name="Voice Commands",
                value=(
                    "`!join` - Join voice channel\n"
                    "`!leave` - Leave voice channel\n"
                    "`!dbsongs` - Daftar lagu Dragon Ball"
                ),
                inline=False
            )
            embed.add_field(
                name="Fun Commands",
                value=(
                    "`!kamehameha` - Kamehameha sound\n"
                    "`!powerlevel` - It's over 9000!\n"
                    "`!play <song>` - Play Dragon Ball music"
                ),
                inline=False
            )
            
        elif category == "quotes":
            embed = discord.Embed(
                title="💬 Quote Commands",
                color=0xFFD700
            )
            embed.add_field(
                name="Commands",
                value="`!quote` - Random Dragon Ball quote",
                inline=False
            )
            embed.add_field(
                name="Features", 
                value="Quote dari karakter terkenal Dragon Ball",
                inline=False
            )
            
        else:
            embed = discord.Embed(
                title="❌ Unknown Category",
                description=f"Category `{category}` tidak ditemukan.\nGunakan `!help` untuk melihat daftar category.",
                color=0xFF0000
            )

        await ctx.send(embed=embed)

    @commands.command(name="info", aliases=["about"])
    async def bot_info(self, ctx):
        """Show bot information"""
        embed = discord.Embed(
            title="🐉 Dragon Ball Bot Info",
            color=0xFF6600
        )
        
        embed.add_field(name="Version", value="1.0.0", inline=True)
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Users", value=str(len(self.bot.users)), inline=True)
        
        embed.add_field(
            name="Features",
            value=(
                "• Character Database\n"
                "• Battle Simulation\n"
                "• Mini Games\n"
                "• Leaderboard System\n"
                "• Music Commands\n"
                "• Random Quotes"
            ),
            inline=False
        )
        
        embed.add_field(
            name="Links",
            value="[GitHub](https://github.com/your-repo) | [Support](https://discord.gg/your-server)",
            inline=False
        )
        
        embed.set_footer(text="Made with ❤️ for Dragon Ball fans")
        await ctx.send(embed=embed)

async def setup(bot):
    # Remove default help command to use our custom one
    bot.remove_command('help')
    await bot.add_cog(Help(bot))
