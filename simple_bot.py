# Import audioop patch first (MUST be before discord import)
import audioop_patch

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Bot setup - Enable message content intent
intents = discord.Intents.default()
intents.message_content = True  # Now enabled!
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)  # Remove default help

@bot.event
async def on_ready():
    print(f'🐉 {bot.user} Dragon Ball Bot is ready!')
    print(f'🎯 Connected to {len(bot.guilds)} servers')
    if bot.guilds:
        for guild in bot.guilds:
            print(f'   - Server: {guild.name} (ID: {guild.id})')
    else:
        print('   ⚠️  Bot belum di-invite ke server manapun!')
    print('✅ Bot is online and ready to use!')
    print('\nAvailable commands:')
    print('!ping - Test bot response')
    print('!char <name> - Character info')
    print('!quote - Random quote')

@bot.event
async def on_message(message):
    """Log all messages for debugging"""
    if not message.author.bot:  # Don't log bot messages
        print(f'📨 Message from {message.author}: {message.content} (Channel: {message.channel.name})')
    
    # Process commands
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    """Test if bot is responding"""
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: {round(bot.latency * 1000)}ms",
        color=0x00FF00
    )
    await ctx.send(embed=embed)

@bot.command(name='char')
async def character_info(ctx, *, name=None):
    """Show character information"""
    if not name:
        await ctx.send("❌ Masukkan nama karakter! Contoh: `!char Goku`")
        return
    
    try:
        with open('data/characters.json', 'r') as f:
            characters = json.load(f)
        
        char = next((c for c in characters if c["name"].lower() == name.lower()), None)
        
        if char:
            embed = discord.Embed(title=f"🐉 {char['name']}", color=0xFF6600)
            embed.add_field(name="Race", value=char['race'], inline=True)
            embed.add_field(name="Power Level", value=f"{char['power_level']:,}", inline=True)
            
            if 'transformations' in char and char['transformations']:
                embed.add_field(name="Transformations", value=", ".join(char['transformations'][:3]), inline=False)
            
            embed.set_footer(text="Dragon Ball Bot")
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Karakter tidak ditemukan! Coba: Goku, Vegeta, Gohan, Frieza, Cell, Piccolo")
    except Exception as e:
        await ctx.send(f"❌ Error loading character data: {str(e)}")

@bot.command(name='quote')
async def random_quote(ctx):
    """Get random Dragon Ball quote"""
    try:
        with open('data/quotes.json', 'r') as f:
            quotes = json.load(f)
        
        import random
        quote = random.choice(quotes)
        
        embed = discord.Embed(color=0xFFD700)
        embed.add_field(name="💬 Quote", value=f'"{quote["text"]}"', inline=False)
        embed.add_field(name="👤 Character", value=quote["character"], inline=True)
        embed.set_footer(text="Dragon Ball Quotes")
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error loading quotes: {str(e)}")

@bot.command(name='help')
async def help_command(ctx):
    """Show help information"""
    embed = discord.Embed(
        title="🐉 Dragon Ball Bot Commands",
        description="Bot Dragon Ball dengan fitur menarik!",
        color=0xFF6600
    )
    
    embed.add_field(
        name="📋 Available Commands",
        value=(
            "`!ping` - Test bot response\n"
            "`!char <name>` - Info karakter (Goku, Vegeta, dll)\n"
            "`!quote` - Random Dragon Ball quote\n"
            "`!help` - Show this help"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📚 Examples",
        value=(
            "`!char Goku` - Info Goku\n"
            "`!char Vegeta` - Info Vegeta\n"
            "`!quote` - Random quote"
        ),
        inline=False
    )
    
    embed.set_footer(text="More features coming soon!")
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        try:
            embed = discord.Embed(
                title="❌ Command Not Found",
                description=f"Command tidak ditemukan! Gunakan `!help` untuk melihat daftar command.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            print(f"❌ Bot tidak punya permission untuk mengirim pesan di channel {ctx.channel.name}")
    elif isinstance(error, discord.Forbidden):
        print(f"❌ Permission Error: Bot tidak punya izin di channel {ctx.channel.name}")
        print("💡 Solusi: Berikan bot permission 'Send Messages' dan 'Embed Links'")
    else:
        print(f"❌ Error: {error}")
        try:
            await ctx.send(f"❌ Terjadi error: {str(error)}")
        except discord.Forbidden:
            print(f"❌ Tidak bisa kirim error message - missing permissions")

# Run bot
if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Error: DISCORD_TOKEN tidak ditemukan di file .env!")
        print("Pastikan file .env berisi: DISCORD_TOKEN=your_token_here")
        exit(1)
    
    try:
        bot.run(token)
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        input("Press Enter to exit...")
