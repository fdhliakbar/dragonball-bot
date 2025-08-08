# Railway Deployment Guide for Dragon Ball Bot

## 🚀 Deploy ke Railway (Recommended)

### Prerequisites:
- ✅ GitHub account
- ✅ Bot code sudah di-push ke GitHub
- ✅ Discord Bot Token

### Steps:

1. **Push ke GitHub:**
   ```bash
   git add .
   git commit -m "Dragon Ball Bot ready for deployment"
   git push origin main
   ```

2. **Deploy di Railway:**
   - Buka: https://railway.app
   - Login dengan GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Pilih repository `dragonball-bot`

3. **Set Environment Variables:**
   - Di Railway dashboard, pilih service Anda
   - Go to "Variables" tab
   - Add: `DISCORD_TOKEN` = `your_actual_token_here`
   - Save

4. **Deploy:**
   - Railway akan otomatis build dan deploy
   - Bot akan online 24/7!

### 💰 Pricing:
- **Free tier**: 500 jam per bulan
- **Upgrade**: $5/bulan untuk unlimited

---

## 🌐 Alternative: Render.com

1. **Push ke GitHub** (sama seperti di atas)

2. **Deploy di Render:**
   - Buka: https://render.com
   - Login dengan GitHub  
   - Click "New" → "Web Service"
   - Connect GitHub repo

3. **Configure:**
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python simple_bot.py`
   - Add environment variable: `DISCORD_TOKEN`

4. **Deploy:**
   - Render akan build dan deploy
   - Free tier: 750 jam per bulan

---

## 🔧 Alternative: Replit

1. **Import dari GitHub:**
   - Buka: https://replit.com
   - Click "Create Repl" → "Import from GitHub"
   - Paste repo URL

2. **Setup:**
   - Add `DISCORD_TOKEN` ke Secrets
   - Run bot
   - Upgrade untuk "Always On" ($7/bulan)

---

## 📱 Monitor Bot:

Setelah deploy, bot Anda akan:
- ✅ **Online 24/7**
- ✅ **Auto-restart** jika crash
- ✅ **Scalable** jika perlu
- ✅ **Logs** untuk debugging

## 🚨 Important:

**Before Deploy:**
- ✅ Pastikan `.env` file ada di `.gitignore`
- ✅ Set `DISCORD_TOKEN` sebagai environment variable di platform
- ✅ Test bot locally dulu
- ✅ Push ke GitHub

**Recommended: Railway.app** karena paling mudah untuk pemula dan gratis 500 jam/bulan (cukup untuk bot kecil).

---

Happy deploying! 🚀
