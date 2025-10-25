# Quick Setup Guide: Enable AI Features

## ✅ Step 1: Anthropic Package (COMPLETED)

The Anthropic Python SDK has been installed successfully!

---

## 📝 Step 2: Get Your Anthropic API Key

### Option A: If you already have an account

1. Visit: https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Give it a name (e.g., "EcoFreonTrack")
4. Copy the API key (starts with `sk-ant-api03-`)

### Option B: If you need to create an account

1. Visit: https://console.anthropic.com/
2. Click "Sign Up"
3. Create your account (you can use Google/GitHub)
4. Once logged in, go to Settings → API Keys
5. Click "Create Key"
6. Copy the API key

### Pricing Information

Anthropic offers **$5 in free credits** when you sign up!

After free credits:
- Claude 3.5 Sonnet: $3 per million input tokens, $15 per million output tokens
- For EcoFreonTrack: ~$17-37/month for typical small business usage

---

## 🔧 Step 3: Configure EcoFreonTrack

Once you have your API key, you have two options:

### Option A: Environment Variables (Recommended for Testing)

Open a new command prompt and run:

```batch
cd C:\Users\Manny\EcoFreonTrack

set AI_ENABLED=true
set ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE

python app.py
```

Replace `sk-ant-api03-YOUR-KEY-HERE` with your actual API key.

### Option B: Create .env File (Recommended for Permanent Setup)

Create a file called `.env` in the EcoFreonTrack folder:

```batch
cd C:\Users\Manny\EcoFreonTrack
copy .env.example .env
notepad .env
```

Edit the `.env` file and set:

```ini
FLASK_ENV=development

# AI Configuration
AI_ENABLED=true
ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE

# Optional: Set a secure secret key
SECRET_KEY=93aa23bf4d70bdb254c74521678705a935849b540d7c594f7a36e661fbf969ea
```

Save and close the file.

Then start the app:
```batch
python app.py
```

---

## ✨ Step 4: Verify AI Features Are Working

1. Open your browser to: http://localhost:5000

2. Check the navigation menu - you should see:
   - **Leak Prediction** (works without API key - uses local data)
   - **Quick Entry** (requires API key)
   - **EPA Assistant** (requires API key)

3. Test each feature:

### Test Leak Prediction (No API Key Needed)
- Click "Leak Prediction" in the AI Features menu
- Should show equipment risk analysis
- If you have equipment with leak inspections, you'll see risk scores

### Test Natural Language Entry (Requires API Key)
- Click "Quick Entry"
- Type: "Serviced AC-12 today, added 3 pounds of R-410A"
- Click "Parse with AI"
- Should extract: Equipment AC-12, Refrigerant Added 3 lbs

### Test EPA Chatbot (Requires API Key)
- Click "EPA Assistant"
- Type: "What is the leak rate threshold for comfort cooling?"
- Click "Ask AI Assistant"
- Should return detailed answer with CFR citations

---

## ❗ Troubleshooting

### Problem: "AI features not enabled" message

**Solution:** Make sure you set `AI_ENABLED=true` and restarted the app

### Problem: "Invalid API Key" error

**Possible causes:**
1. API key is incorrect
2. Extra spaces in the key
3. Quotes around the key

**Solution:**
```batch
# Make sure there are NO quotes around the key
set ANTHROPIC_API_KEY=sk-ant-api03-your-key

# NOT this:
set ANTHROPIC_API_KEY="sk-ant-api03-your-key"
```

### Problem: Natural Language / Chatbot not working

**Check:**
1. API key is set correctly
2. You have credits remaining in your Anthropic account
3. Internet connection is working

**Test API key:**
```batch
python -c "import anthropic; client = anthropic.Anthropic(api_key='YOUR-KEY'); print('API key works!')"
```

---

## 🔒 Security Best Practices

### DO:
✅ Keep your API key secret
✅ Use environment variables or .env file
✅ Add `.env` to .gitignore (already done)
✅ Rotate keys periodically

### DON'T:
❌ Commit API keys to git
❌ Share keys publicly
❌ Hardcode keys in source files

---

## 💰 Monitor Your Usage

Track your API usage and costs:

1. Visit: https://console.anthropic.com/settings/usage
2. View token usage and costs
3. Set up usage alerts if desired

**Estimated costs for EcoFreonTrack:**
- 100 natural language service entries: ~$1-2
- 200 chatbot questions: ~$2-4
- Total for small business: $17-37/month

---

## 🎯 Quick Start Commands

### Start with AI enabled (temporary - this session only):
```batch
cd C:\Users\Manny\EcoFreonTrack
set AI_ENABLED=true
set ANTHROPIC_API_KEY=your-key-here
python app.py
```

### Start with .env file (permanent):
```batch
cd C:\Users\Manny\EcoFreonTrack
# Make sure .env file has your API key
python app.py
```

### Start development mode:
```batch
cd C:\Users\Manny\EcoFreonTrack
run_dev.bat
# Or manually:
set FLASK_ENV=development
set AI_ENABLED=true
set ANTHROPIC_API_KEY=your-key-here
python app.py
```

---

## 📚 Next Steps

Once AI is working:

1. **Read the full guide:** `AI_FEATURES_GUIDE.md`
2. **Add some test equipment** with leak inspections to test predictions
3. **Try natural language entry** with example service descriptions
4. **Ask the chatbot** common EPA compliance questions
5. **Bookmark the app** for easy access

---

## 🆘 Need Help?

- **Full AI Documentation:** See `AI_FEATURES_GUIDE.md`
- **Anthropic Console:** https://console.anthropic.com/
- **Anthropic Docs:** https://docs.anthropic.com/

---

**You're almost there!** Just get your API key and you'll have AI-powered EPA compliance at your fingertips! 🚀
