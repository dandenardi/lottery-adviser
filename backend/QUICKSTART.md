# 🚀 Quick Start Guide - Lottery Adviser API

## ⚡ Get Running in 5 Minutes

### Step 1: Setup Environment (1 min)

```bash
cd lottery-adviser-api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Step 2: Configure (1 min)

```bash
# Copy environment file
copy .env.example .env

# Edit .env and set DATABASE_URL
# For local testing with SQLite (quick):
DATABASE_URL=sqlite:///./lottery.db

# Or use PostgreSQL (recommended):
DATABASE_URL=postgresql://user:password@localhost:5432/lottery_adviser
```

### Step 3: Migrate Data (2 min)

```bash
# Update Excel file path in scripts/migrate_data.py (line 87)
# Then run:
python scripts/migrate_data.py
```

### Step 4: Run! (1 min)

```bash
uvicorn app.main:app --reload
```

✅ **Done!** API running at: http://localhost:8000

---

## 🧪 Test It

### Open Browser

- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Try Endpoints

```bash
# Latest result
curl http://localhost:8000/api/v1/results/latest

# Statistics
curl http://localhost:8000/api/v1/statistics

# Generate suggestion
curl -X POST http://localhost:8000/api/v1/suggestions \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"test-user\", \"strategy\": \"balanced\", \"count\": 1}"
```

---

## 🚀 Deploy to Render.com (Free)

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/lottery-adviser-api.git
git push -u origin main
```

### 2. Deploy on Render

1. Go to https://render.com
2. Sign up/Login
3. Click "New +" → "Blueprint"
4. Connect GitHub repo
5. Click "Apply"

**That's it!** Render will:

- Create PostgreSQL database
- Deploy API
- Give you HTTPS URL

### 3. Update CORS

After deploy, update `render.yaml` with your React Native app URL:

```yaml
- key: CORS_ORIGINS
  value: https://your-render-url.onrender.com
```

### 4. Migrate Data to Production

Use Render Shell or connect to database and run:

```bash
python scripts/migrate_data.py
```

---

## 📱 Connect React Native App

Update your React Native app's API URL:

```typescript
// src/services/api.ts
const API_URL = __DEV__
  ? "http://localhost:8000/api/v1"
  : "https://your-app.onrender.com/api/v1";
```

---

## 🎯 Next Steps

1. ✅ Test all endpoints
2. ✅ Deploy to Render
3. ✅ Connect React Native app
4. ✅ Test end-to-end
5. 🚀 Launch!

---

## ❓ Troubleshooting

### Database connection error?

- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Or use SQLite for quick testing

### Import error?

- Activate virtual environment: `venv\Scripts\activate`
- Reinstall: `pip install -r requirements.txt`

### Migration fails?

- Check Excel file path in `scripts/migrate_data.py`
- Ensure file exists and is readable

---

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

---

**Need help?** Check the logs or API docs at `/docs`
