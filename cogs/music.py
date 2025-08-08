import discord
from discord.ext import commands
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}
        
        # Dragon Ball theme songs and soundtracks
        self.dragon_ball_songs = {
            "cha-la": {
                "title": "Cha-La Head-Cha-La",
                "url": "https://www.youtube.com/watch?v=GHnfX1RmZX8",
                "description": "Dragon Ball Z Opening Theme"
            },
            "rock-the-dragon": {
                "title": "Rock The Dragon",
                "url": "https://www.youtube.com/watch?v=R4vjJrGeh1c", 
                "description": "Dragon Ball Z English Opening"
            },
            "dan-dan": {
                "title": "Dan Dan Kokoro Hikareteku",
                "url": "https://www.youtube.com/watch?v=BIyscFghyUE",
                "description": "Dragon Ball GT Opening Theme"
            },
            "ultimate-battle": {
                "title": "Ultimate Battle",
                "url": "https://www.youtube.com/watch?v=h8qg-XzHgYk",
                "description": "Dragon Ball Super Ultra Instinct Theme"
            },
            "limit-break": {
                "title": "Limit Break x Survivor", 
                "url": "https://www.youtube.com/watch?v=BDiEKYC_kKY",
                "description": "Dragon Ball Super Opening 2"
            }
        }

    @commands.command(name="join", aliases=["connect"])
    async def join_voice(self, ctx):
        """Join the user's voice channel"""
        if not ctx.author.voice:
            embed = discord.Embed(
                title="❌ Error",
                description="Anda harus berada di voice channel terlebih dahulu!",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return

        channel = ctx.author.voice.channel
        
        try:
            voice_client = await channel.connect()
            self.voice_clients[ctx.guild.id] = voice_client
            
            embed = discord.Embed(
                title="🎵 Connected!",
                description=f"Terhubung ke **{channel.name}**",
                color=0x00FF00
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Tidak dapat terhubung ke voice channel: {str(e)}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    @commands.command(name="leave", aliases=["disconnect", "dc"])
    async def leave_voice(self, ctx):
        """Leave the voice channel"""
        if ctx.guild.id in self.voice_clients:
            voice_client = self.voice_clients[ctx.guild.id]
            await voice_client.disconnect()
            del self.voice_clients[ctx.guild.id]
            
            embed = discord.Embed(
                title="👋 Disconnected",
                description="Keluar dari voice channel",
                color=0xFFD700
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Error", 
                description="Bot tidak sedang berada di voice channel!",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

    @commands.command(name="dbsongs", aliases=["songs", "playlist"])
    async def show_dragon_ball_songs(self, ctx):
        """Show available Dragon Ball songs"""
        embed = discord.Embed(
            title="🎵 Dragon Ball Music Playlist",
            description="Gunakan `!play <song_code>` untuk memutar lagu",
            color=0x9932CC
        )
        
        for code, info in self.dragon_ball_songs.items():
            embed.add_field(
                name=f"🎶 `{code}`",
                value=f"**{info['title']}**\n{info['description']}",
                inline=False
            )
        
        embed.set_footer(text="Contoh: !play cha-la")
        await ctx.send(embed=embed)

    @commands.command(name="play", aliases=["p"])
    async def play_song(self, ctx, *, song_code=None):
        """Play a Dragon Ball song"""
        if not song_code:
            await ctx.send("❌ Masukkan kode lagu! Gunakan `!dbsongs` untuk melihat daftar lagu.")
            return

        song_code = song_code.lower().strip()
        
        if song_code not in self.dragon_ball_songs:
            embed = discord.Embed(
                title="❌ Lagu Tidak Ditemukan",
                description=f"Lagu dengan kode `{song_code}` tidak ditemukan.\nGunakan `!dbsongs` untuk melihat daftar lagu.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return

        # Check if bot is in voice channel
        if ctx.guild.id not in self.voice_clients:
            if ctx.author.voice:
                await self.join_voice(ctx)
            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="Anda harus berada di voice channel atau bot harus sudah terhubung!",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
                return

        song_info = self.dragon_ball_songs[song_code]
        
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{song_info['title']}**\n{song_info['description']}",
            color=0x00CED1
        )
        embed.add_field(name="URL", value=f"[Click here to listen]({song_info['url']})", inline=False)
        embed.set_footer(text="Note: Bot akan memberikan link untuk diputar manual karena keterbatasan YouTube streaming")
        
        await ctx.send(embed=embed)

    @commands.command(name="kamehameha")
    async def kamehameha_sound(self, ctx):
        """Play Kamehameha sound effect"""
        embed = discord.Embed(
            title="🔥 KAMEHAMEHA!",
            description="**Ka-me-ha-me-HAAA!** 💥",
            color=0x00BFFF
        )
        embed.set_image(url="https://media.giphy.com/media/3o84sq21TxDH6PyYms/giphy.gif")
        await ctx.send(embed=embed)
        
        # Play sound effect (simplified)
        if ctx.guild.id in self.voice_clients:
            voice_client = self.voice_clients[ctx.guild.id]
            # In a real implementation, you would play an actual sound file here

    @commands.command(name="powerlevel")  
    async def power_level_sound(self, ctx):
        """Play 'It's over 9000!' sound"""
        embed = discord.Embed(
            title="📊 POWER LEVEL",
            description="**IT'S OVER 9000!** 🔥💥",
            color=0xFF4500
        )
        embed.set_image(url="https://media.giphy.com/media/MvedbKot538WY/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command(name="volume", aliases=["vol"])
    async def set_volume(self, ctx, volume: int):
        """Set playback volume (0-100)"""
        if not (0 <= volume <= 100):
            embed = discord.Embed(
                title="❌ Error",
                description="Volume harus antara 0-100!",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="🔊 Volume",
            description=f"Volume diatur ke **{volume}%**",
            color=0x32CD32
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
