# 🚀 Quick Start Guide - Step by Step

## Prerequisites Check
```bash
# Check Python version (need 3.10+)
python3 --version

# Check pip
pip3 --version

# Check git
git --version
```

---

## ⚡ FAST TRACK (5 Steps - 15 minutes)

### Step 1: Activate Virtual Environment
```bash
cd /Users/newuser/ali/project/astra
source /Users/newuser/ali/project/kampus\ merdeka/repo_dibimbing/venv/bin/activate
```

You should see `(venv)` in your terminal.

---

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
```

**If error:** Check Python version. Need Python 3.10 or 3.11 (not 3.12).

---

### Step 3: Download YOLOv8 Model
```bash
python scripts/download_models.py
```

**Expected output:**
```
📥 Downloading YOLOv8 models...
✅ yolov8n ready
```

**Time:** ~2-3 minutes (downloads 6MB model)

---

### Step 4: Initialize Database
```bash
python scripts/init_db.py
```

**Expected output:**
```
✅ Database initialized successfully
```

**Creates:** `astra.db` file in project root

---

### Step 5: Run the Server!
```bash
python app.py
```

**Expected output:**
```
🚀 Starting Helmet Detection System...
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Open browser:** http://localhost:8000/docs

---

## 🧪 Test the API

### Test 1: Health Check
```bash
# Open new terminal
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "ok",
  "timestamp": "2026-02-02T10:00:00",
  "service": "Helmet Detection System",
  "version": "1.0.0"
}
```

---

### Test 2: Upload a Sample Video

**Option A: Use Swagger UI (Easiest)**
1. Go to http://localhost:8000/docs
2. Click on `POST /api/videos/upload`
3. Click "Try it out"
4. Choose a video file (MP4)
5. Click "Execute"

**Option B: Using curl**
```bash
# Create a sample video first (or use your own)
curl -X POST http://localhost:8000/api/videos/upload \
  -F "file=@/path/to/your/video.mp4"
```

**Expected response:**
```json
{
  "video_id": "uuid-here",
  "filename": "video.mp4",
  "size_mb": 25.5,
  "status": "pending",
  "message": "Video uploaded successfully"
}
```

---

### Test 3: List Uploaded Videos
```bash
curl http://localhost:8000/api/videos
```

---

### Test 4: Process Video
```bash
# Replace VIDEO_ID with actual ID from upload
curl -X POST http://localhost:8000/api/videos/VIDEO_ID/process \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### Test 5: Check Results
```bash
# Wait 2-3 minutes for processing, then:
curl http://localhost:8000/api/videos/VIDEO_ID/results
```

---

## 📁 Project Structure Quick Reference

```
astra/
├── app.py                    ← Main entry point (run this!)
├── requirements.txt          ← Dependencies
├── .env                      ← Your config (API keys)
├── astra.db                  ← Database (auto-created)
│
├── api/
│   ├── routes.py            ← All API endpoints
│   └── schemas.py           ← Request/response models
│
├── models/
│   └── detector.py          ← YOLOv8 detection logic
│
├── utils/
│   ├── gemini_client.py     ← LLM integration
│   └── line_crossing.py     ← Counting logic
│
├── config/
│   ├── settings.py          ← Configuration
│   └── constants.py         ← Constants
│
├── scripts/
│   ├── download_models.py   ← Download YOLOv8
│   ├── init_db.py          ← Setup database
│   └── test_detection.py   ← Test on video
│
├── data/
│   ├── videos/             ← Uploaded videos
│   └── outputs/            ← Results
│
└── logs/
    └── astra.log           ← Application logs
```

---

## 🔧 Troubleshooting

### Problem 1: Port Already in Use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
python app.py --port 8001
```

---

### Problem 2: Module Not Found
```bash
# Make sure virtual environment is activated
source /Users/newuser/ali/project/kampus\ merdeka/repo_dibimbing/venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Problem 3: Database Error
```bash
# Delete and recreate
rm astra.db
python scripts/init_db.py
```

---

### Problem 4: YOLOv8 Model Not Found
```bash
# Re-download model
python scripts/download_models.py

# Check if file exists
ls ~/.cache/ultralytics/
```

---

### Problem 5: Google API Error
```bash
# Check your API key in .env
cat .env | grep GOOGLE_API_KEY

# Test API key
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('API Key:', os.getenv('GOOGLE_API_KEY')[:10], '...')
"
```

---

## 🎯 Common Commands

### Start Server
```bash
# Development (with auto-reload)
python app.py

# Or with uvicorn directly
uvicorn app:app --reload --port 8000
```

### Stop Server
```
Press Ctrl + C in the terminal
```

### View Logs
```bash
# Follow logs in real-time
tail -f logs/astra.log

# View all logs
cat logs/astra.log

# Search for errors
grep ERROR logs/astra.log
```

### Test Detection on Local Video
```bash
python scripts/test_detection.py --video /path/to/video.mp4
```

---

## 📊 Test with Sample Data

### Create a Sample Video (For Testing)
```bash
# Using Python
python -c "
import cv2
import numpy as np

# Create 10-second video
out = cv2.VideoWriter('sample_test.mp4', 
    cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))

for i in range(300):
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    out.write(frame)

out.release()
print('✅ sample_test.mp4 created')
"
```

### Test Detection
```bash
python scripts/test_detection.py --video sample_test.mp4
```

---

## 🌐 Access Points

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | Main API |
| http://localhost:8000/docs | Interactive API docs (Swagger) |
| http://localhost:8000/redoc | Alternative API docs |
| http://localhost:8000/health | Health check |
| http://localhost:8000/api/videos | List videos |

---

## 📈 Next Steps After Running

### 1. Test with Real Video
```bash
# Upload your motorcycle video
curl -X POST http://localhost:8000/api/videos/upload \
  -F "file=@your_real_video.mp4"
```

### 2. Check Processing Status
```bash
curl http://localhost:8000/api/videos/VIDEO_ID/status
```

### 3. View Results
```bash
# Get JSON results
curl http://localhost:8000/api/videos/VIDEO_ID/results

# Export to CSV
curl "http://localhost:8000/api/videos/VIDEO_ID/export?format=csv"
```

### 4. View Analytics
```bash
curl http://localhost:8000/api/analytics/summary
```

---

## 🚀 Deploy to Production

### Option 1: Render.com (Recommended)
```bash
# Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# Then on Render.com:
1. New Web Service
2. Connect GitHub repo
3. Build: pip install -r requirements.txt
4. Start: uvicorn app:app --host 0.0.0.0 --port $PORT
5. Add environment variables from .env
6. Deploy!
```

### Option 2: Railway.app
```bash
# Install CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Option 3: Docker
```bash
# Build image
docker build -t astra:latest .

# Run container
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  astra:latest
```

---

## ✅ Success Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed (no errors)
- [ ] YOLOv8 model downloaded
- [ ] Database initialized
- [ ] Server running (port 8000)
- [ ] Health check returns OK
- [ ] Swagger docs accessible
- [ ] Sample video uploaded
- [ ] Video processing works
- [ ] Results retrieved successfully

---

## 🆘 Get Help

### Check Logs
```bash
tail -f logs/astra.log
```

### Check Configuration
```bash
cat .env
```

### Check Database
```bash
sqlite3 astra.db "SELECT COUNT(*) FROM videos;"
```

### Python Environment
```bash
pip list | grep fastapi
pip list | grep ultralytics
```

---

## 📞 Quick Reference

**Start Development:**
```bash
cd /Users/newuser/ali/project/astra
source /Users/newuser/ali/project/kampus\ merdeka/repo_dibimbing/venv/bin/activate
python app.py
```

**Open in Browser:**
```
http://localhost:8000/docs
```

**Stop Server:**
```
Ctrl + C
```

**That's it! You're ready to go! 🎉**
