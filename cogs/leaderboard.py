import discord
from discord.ext import commands
import sqlite3
import os

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'data/leaderboard.db'
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for leaderboard"""
        os.makedirs('data', exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    games_played INTEGER DEFAULT 0,
                    total_score INTEGER DEFAULT 0
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS battles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    opponent_character TEXT,
                    user_character TEXT,
                    result TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            conn.commit()

    def add_user_if_not_exists(self, user_id, username):
        """Add user to database if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username)
                VALUES (?, ?)
            ''', (user_id, username))
            conn.commit()

    def update_battle_result(self, user_id, username, user_char, opponent_char, won):
        """Update user stats after a battle"""
        self.add_user_if_not_exists(user_id, username)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Update user stats
            if won:
                cursor.execute('''
                    UPDATE users 
                    SET wins = wins + 1, games_played = games_played + 1, 
                        total_score = total_score + 10, username = ?
                    WHERE user_id = ?
                ''', (username, user_id))
                result = 'win'
            else:
                cursor.execute('''
                    UPDATE users 
                    SET losses = losses + 1, games_played = games_played + 1, 
                        total_score = total_score + 1, username = ?
                    WHERE user_id = ?
                ''', (username, user_id))
                result = 'loss'
            
            # Add battle record
            cursor.execute('''
                INSERT INTO battles (user_id, user_character, opponent_character, result)
                VALUES (?, ?, ?, ?)
            ''', (user_id, user_char, opponent_char, result))
            
            conn.commit()

    @commands.command(name="leaderboard", aliases=["lb", "top"])
    async def show_leaderboard(self, ctx, limit: int = 10):
        """Show the battle leaderboard"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT username, wins, losses, games_played, total_score,
                       CASE WHEN games_played > 0 
                            THEN ROUND((CAST(wins AS FLOAT) / games_played) * 100, 1)
                            ELSE 0 END as win_rate
                FROM users 
                WHERE games_played > 0
                ORDER BY total_score DESC, win_rate DESC
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()

        if not results:
            embed = discord.Embed(
                title="🏆 Dragon Ball Battle Leaderboard",
                description="Belum ada data pertarungan!",
                color=0xFFD700
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="🏆 Dragon Ball Battle Leaderboard",
            color=0xFFD700
        )

        leaderboard_text = []
        medals = ["🥇", "🥈", "🥉"]
        
        for i, (username, wins, losses, games, score, win_rate) in enumerate(results):
            medal = medals[i] if i < 3 else f"{i+1}."
            leaderboard_text.append(
                f"{medal} **{username}**\n"
                f"   Score: {score} | W: {wins} L: {losses} | Win Rate: {win_rate}%\n"
            )

        embed.description = "\n".join(leaderboard_text)
        embed.set_footer(text=f"Menampilkan top {len(results)} pemain")

        await ctx.send(embed=embed)

    @commands.command(name="mystats", aliases=["stats", "profile"])
    async def show_user_stats(self, ctx, user: discord.Member = None):
        """Show user's battle statistics"""
        target_user = user or ctx.author
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT wins, losses, games_played, total_score
                FROM users WHERE user_id = ?
            ''', (target_user.id,))
            
            result = cursor.fetchone()

        if not result:
            embed = discord.Embed(
                title="📊 Battle Stats",
                description=f"{target_user.display_name} belum pernah bertarung!",
                color=0xFF6347
            )
            await ctx.send(embed=embed)
            return

        wins, losses, games, score = result
        win_rate = (wins / games * 100) if games > 0 else 0

        embed = discord.Embed(
            title=f"📊 Battle Stats - {target_user.display_name}",
            color=0x00CED1
        )
        
        embed.add_field(name="🎯 Total Score", value=str(score), inline=True)
        embed.add_field(name="🎮 Games Played", value=str(games), inline=True)
        embed.add_field(name="📈 Win Rate", value=f"{win_rate:.1f}%", inline=True)
        embed.add_field(name="🏆 Wins", value=str(wins), inline=True)
        embed.add_field(name="💀 Losses", value=str(losses), inline=True)
        embed.add_field(name="⚖️ W/L Ratio", value=f"{wins/losses:.2f}" if losses > 0 else "∞", inline=True)

        embed.set_thumbnail(url=target_user.display_avatar.url)
        embed.set_footer(text="Terus bertarung untuk meningkatkan ranking!")

        await ctx.send(embed=embed)

    @commands.command(name="battlehistory", aliases=["history"])
    async def show_battle_history(self, ctx, limit: int = 5):
        """Show user's recent battle history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_character, opponent_character, result, timestamp
                FROM battles 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (ctx.author.id, limit))
            
            battles = cursor.fetchall()

        if not battles:
            embed = discord.Embed(
                title="📜 Battle History",
                description="Anda belum pernah bertarung!",
                color=0xFF6347
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title=f"📜 Battle History - {ctx.author.display_name}",
            color=0x9370DB
        )

        history_text = []
        for user_char, opp_char, result, timestamp in battles:
            result_emoji = "🏆" if result == "win" else "💀"
            history_text.append(
                f"{result_emoji} {user_char} vs {opp_char}"
            )

        embed.description = "\n".join(history_text)
        embed.set_footer(text=f"Showing last {len(battles)} battles")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
