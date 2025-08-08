# 🚀 CARA MENJALANKAN DRAGON BALL BOT

## 📋 Prerequisites

1. **Python 3.8-3.12** (PENTING: Jangan gunakan Python 3.13+)
2. **Discord Bot Token**
3. **Git** (optional)

## 🔧 Setup Bot Discord

### 1. Buat Discord Application
1. Pergi ke https://discord.com/developers/applications
2. Klik "New Application"
3. Beri nama "Dragon Ball Bot" 
4. Pergi ke tab "Bot"
5. Klik "Add Bot"
6. Copy **Token** (jangan share ke siapa-siapa!)

### 2. Set Permissions
Di tab "OAuth2" > "URL Generator":
- **Scopes**: `bot`
- **Bot Permissions**:
  - Send Messages
  - Use Slash Commands
  - Connect
  - Speak
  - Embed Links
  - Attach Files
  - Read Message History

### 3. Invite Bot
1. Copy URL yang dihasilkan
2. Paste ke browser
3. Pilih server dan authorize

## 🏃‍♂️ Menjalankan Bot

### Cara 1: Otomatis (Windows)
```cmd
# 1. Setup (jalankan sekali saja)
setup.bat

# 2. Edit file .env dan masukkan token bot
# DISCORD_TOKEN=your_actual_token_here

# 3. Jalankan bot
run_bot.bat
```

### Cara 2: Manual
```cmd
# 1. Install dependencies
pip install -r requirements.txt

# 2. Buat file .env
echo DISCORD_TOKEN=your_token_here > .env

# 3. Jalankan bot
python main.py
```

## 📱 Testing Bot

Setelah bot online, test dengan commands:

```
!help           # Bantuan lengkap
!char goku      # Info Goku
!quote          # Quote random
!fight goku vegeta  # Battle simulation
!guess          # Guess game
!leaderboard    # Ranking
```

## ⚠️ Troubleshooting

### Bot tidak respond
- ✅ Check token di .env benar
- ✅ Bot sudah di-invite ke server
- ✅ Bot punya permission yang cukup
- ✅ Prefix command benar (!)

### Import Error (audioop)
- ✅ Gunakan Python 3.8-3.12 (bukan 3.13+)
- ✅ Install ulang discord.py versi compatible

### Database Error
- ✅ Folder `data/` harus ada dan writable
- ✅ SQLite database akan auto-create

### Permission Error
- ✅ Bot perlu permission "Send Messages" & "Embed Links"
- ✅ Check role hierarchy di server

## 🎯 Available Commands

### Character System
- `!char <name>` - Character info
- `!fight <char1> <char2>` - Battle simulation
- `!list_chars` - List all characters

### Games
- `!guess` - Guess character game
- `!powerguess` - Guess power level

### Leaderboard
- `!leaderboard` - Top players
- `!mystats` - Your stats
- `!battlehistory` - Your battle history

### Music (Voice Channel)
- `!join` - Join voice channel
- `!dbsongs` - Dragon Ball playlist
- `!kamehameha` - Sound effect
- `!powerlevel` - "Over 9000!" effect

### Others
- `!quote` - Random DB quote
- `!help <category>` - Detailed help

## 📊 Point System

- **Win Battle**: +10 points
- **Lose Battle**: +1 point  
- **Guess Game (Correct)**: +10 points
- **Power Guess**: 5-15 points (based on accuracy)

## 🔒 Security Notes

- ❌ **JANGAN SHARE** Discord token
- ❌ **JANGAN COMMIT** .env ke Git
- ✅ Gunakan .gitignore untuk .env
- ✅ Regenerate token jika terkompromasi

## 📞 Support

Jika ada masalah:
1. Check troubleshooting di atas
2. Restart bot
3. Check bot logs di terminal
4. Join support server (jika ada)

---
Happy coding! 🐉⚡
