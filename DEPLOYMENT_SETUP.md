# Helmet Detection System - Deployment Setup Guide
**Python-Based | Free Server | Step-by-Step**

---

## 📋 Prerequisites

```bash
- Python 3.10+
- Git
- 4GB RAM minimum
- Internet connection
```

---

## 🚀 STEP 1: Get Free API Keys (No Credit Card)

### 1.1 Google Gemini API Key
```
1. Go to: https://ai.google.dev/
2. Click "Get API key" → Create new API key
3. Copy the key
4. FREE TIER: 1M tokens/day, 15 RPM
```

### 1.2 Hugging Face Token (Optional - for model downloads)
```
1. Go to: https://huggingface.co/settings/tokens
2. Create new token (Read)
3. Copy token
```

### 1.3 GitHub Token (Optional - for private repos)
```
1. Settings → Developer settings → Personal access tokens
2. Create token with repo access
```

---

## 📁 STEP 2: Project Structure Setup

### 2.1 Clone or Create Project
```bash
cd /Users/newuser/ali/project/astra
git init
git remote add origin https://github.com/yourusername/astra-helmet-detection.git
```

### 2.2 Create Directory Structure
```bash
# Run this command:
python3 setup_project.py

# Or manually:
mkdir -p astra/{api,models,utils,data,config,logs}
mkdir -p astra/{frontend,tests,scripts,docs}
```

### 2.3 Directory Tree
```
astra/
├── api/
│   ├── __init__.py
│   ├── routes.py              # FastAPI endpoints
│   ├── schemas.py             # Pydantic models
│   └── middleware.py
├── models/
│   ├── __init__.py
│   ├── detector.py            # YOLOv8 wrapper
│   ├── tracker.py             # ByteTrack
│   └── analyzer.py            # Line crossing logic
├── utils/
│   ├── __init__.py
│   ├── video_processor.py      # Video handling
│   ├── gemini_client.py        # Gemini API wrapper
│   └── line_crossing.py        # Detection logic
├── data/
│   ├── videos/                # Uploaded videos
│   ├── outputs/               # Results
│   └── annotations/           # Detection results
├── config/
│   ├── __init__.py
│   ├── settings.py            # Environment config
│   └── constants.py
├── scripts/
│   ├── train_model.py         # Model training
│   ├── generate_sample_data.py
│   └── test_detection.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── app.py                     # Main FastAPI app
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── setup.py
└── README.md
```

---

## 🔧 STEP 3: Install & Setup

### 3.1 Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# OR
venv\Scripts\activate             # Windows
```

### 3.2 Copy Environment File
```bash
cp .env.example .env

# Edit .env with your keys:
GOOGLE_API_KEY=your_key_here
HUGGINGFACE_TOKEN=your_token_here
DATABASE_URL=sqlite:///astra.db
DEBUG=True
```

### 3.3 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt

# This will install:
# - fastapi & uvicorn
# - ultralytics (YOLOv8)
# - opencv-python
# - torch & torchvision
# - google-generativeai
# - sqlalchemy
# - python-dotenv
# - pydantic
```

### 3.4 Download YOLOv8 Pretrained Model
```bash
python3 scripts/download_models.py

# Models saved to: models/weights/
```

---

## 🎯 STEP 4: Deploy to Free Server

### Option A: Render.com (Recommended for Python)

**Setup Steps:**
```
1. Sign up: https://render.com (GitHub account)
2. Create New → Web Service
3. Connect GitHub repository
4. Fill in:
   - Name: astra-helmet-detection
   - Environment: Python 3.10
   - Build command: pip install -r requirements.txt
   - Start command: uvicorn app:app --host 0.0.0.0 --port $PORT
5. Add Environment Variables (from .env)
6. Deploy!

Domain: astra-helmet-detection.onrender.com
```

**Limits (Free):**
- 750 hours/month
- Auto-sleep after 15 min inactivity
- 512MB RAM
- 0.5GB disk

---

### Option B: Railway.app

**Setup Steps:**
```
1. Sign up: https://railway.app (GitHub)
2. New Project → Deploy from GitHub
3. Select your repository
4. Configure:
   - Root directory: ./
   - Build: pip install -r requirements.txt
   - Start: uvicorn app:app --host 0.0.0.0 --port $PORT
5. Add environment variables
6. Deploy

Domain: your-service.up.railway.app
```

**Limits (Free - New Users):**
- $5 credit/month
- ~750 hours
- 100GB bandwidth

---

### Option C: Replit.com (Easiest)

**Setup:**
```
1. Go to: https://replit.com
2. Import from GitHub
3. Create Secret keys (.env)
4. Click "Run"
5. Open URL from browser

Domain: replit-username.repl.co
```

**Limits:**
- Unlimited projects
- 3GB storage
- Auto-sleep (but quick wake)

---

## 📡 STEP 5: API Endpoints Test

### 5.1 Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{"status": "ok", "version": "1.0"}
```

### 5.2 Upload Video
```bash
curl -X POST http://localhost:8000/api/videos/upload \
  -F "file=@test_video.mp4"
```

### 5.3 Process Video
```bash
curl -X POST http://localhost:8000/api/videos/{video_id}/process \
  -H "Content-Type: application/json" \
  -d '{"roi": [[100, 100], [500, 100], [500, 300], [100, 300]]}'
```

### 5.4 Get Results
```bash
curl http://localhost:8000/api/videos/{video_id}/results
```

---

## 🎨 STEP 6: Frontend Setup (Optional - Simple Web UI)

### 6.1 Simple HTML UI
```bash
# Create frontend/index.html (see template below)
# Serve with Python:
python3 -m http.server 3000 --directory frontend/
# Access: http://localhost:3000
```

### 6.2 Deploy Frontend to Vercel (Optional)
```bash
npm install -g vercel
cd frontend/
vercel --prod
```

---

## 🧪 STEP 7: Test Locally

### 7.1 Run Development Server
```bash
python3 app.py
# OR
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 7.2 API Documentation (Auto-Generated)
```
http://localhost:8000/docs          # Swagger UI
http://localhost:8000/redoc         # ReDoc
```

### 7.3 Test with Sample Video
```bash
python3 scripts/test_detection.py --video sample_video.mp4
```

---

## 📊 STEP 8: Database Setup

### 8.1 SQLite (Recommended for Free Tier)
```bash
# Automatically created on first run
# File: astra.db (stored in project root)
```

### 8.2 Initialize Database
```bash
python3 scripts/init_db.py
```

### 8.3 View Database
```bash
# Option 1: SQLite CLI
sqlite3 astra.db

# Option 2: DB Browser
# Download: https://sqlitebrowser.org/
```

---

## 🔒 STEP 9: Security Setup

### 9.1 Generate Secret Key
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy output to .env as SECRET_KEY
```

### 9.2 CORS Configuration (for frontend)
```python
# In config/settings.py
CORS_ORIGINS = ["http://localhost:3000", "your-domain.com"]
```

### 9.3 Rate Limiting
```python
# Already included in api/middleware.py
# Limits: 100 requests/minute per IP
```

---

## 📦 STEP 10: Docker Deployment (Optional)

### 10.1 Build Docker Image
```bash
docker build -t astra-helmet-detection .
```

### 10.2 Run Container
```bash
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  astra-helmet-detection
```

### 10.3 Docker Compose (Multiple Services)
```bash
docker-compose up -d
# Services: FastAPI + Redis (optional) + PostgreSQL (optional)
```

---

## 🚨 STEP 11: Troubleshooting

### Issue: CUDA/GPU not found
```bash
# Use CPU only (slower but free)
export TORCH_DEVICE=cpu
# In code: device = "cpu"
```

### Issue: Out of Memory
```bash
# Use smaller model
python3 setup_project.py --model yolov8n  # nano
# Or: yolov8s (small)
```

### Issue: Free server goes to sleep
```bash
# Add periodic ping to keep alive
python3 scripts/keep_alive.py
```

### Issue: Video upload fails
```bash
# Check storage limits:
df -h
# Max video size: 100MB (adjust in config)
```

---

## 📈 STEP 12: Scaling to Production

### When Free Tier Limits Hit:

**Upgrade Option 1: Dedicated Server**
- DigitalOcean: $5-6/month
- Linode: $5/month
- AWS EC2: $9.50/month (first year free)

**Upgrade Option 2: Better Free Tier**
- Google Cloud Run: 2M invocations/month
- AWS Lambda: 1M requests/month
- Heroku: Discontinued (use Railway instead)

**Cost Estimate at Scale:**
```
Free:        $0/month (limited to ~100 videos)
Small:      $10-15/month (1000+ videos)
Medium:     $30-50/month (10k+ videos)
Enterprise: Custom pricing
```

---

## ✅ Deployment Checklist

- [ ] API keys generated (Google Gemini)
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] YOLOv8 model downloaded
- [ ] Database initialized
- [ ] Local testing successful
- [ ] Server deployed (Render/Railway/Replit)
- [ ] API endpoints tested
- [ ] Frontend running (optional)
- [ ] Monitoring setup (logs)
- [ ] Backup strategy configured

---

## 📞 Support & Resources

**Documentation:**
- YOLOv8: https://docs.ultralytics.com/
- FastAPI: https://fastapi.tiangolo.com/
- Google Gemini: https://ai.google.dev/
- Render: https://render.com/docs

**Community:**
- Ultralytics Discussions: https://github.com/ultralytics/yolov8/discussions
- FastAPI Discord: https://discord.gg/VTkJ7Z2

**Next Steps:**
1. Follow STEP 1-5 to get deployed
2. Use API endpoints to test
3. Upload sample videos
4. Verify detection results
5. Fine-tune model with custom data

---

**Last Updated:** January 31, 2026
**Version:** 1.0
**Status:** Ready to Deploy
