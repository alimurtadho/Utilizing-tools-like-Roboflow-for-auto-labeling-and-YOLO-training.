# Command Reference & Cheat Sheet

## 🚀 Quick Start (Copy-Paste Ready)

```bash
# Activate venv (do this first!)
source venv/bin/activate    # macOS/Linux
# OR
venv\Scripts\activate       # Windows

# Run everything
python3 setup_project.py              # Generate structure
pip install -r requirements.txt       # Install deps
python3 scripts/init_db.py            # Initialize DB
python3 scripts/download_models.py    # Download models
python3 app.py                        # Start server
```

**Then open browser:**
```
http://localhost:8000/docs
```

---

## 📁 File Generation

### Create All Project Files
```bash
python3 setup_project.py
```

### Generated Structure
```
api/              → API routes & schemas
models/           → YOLOv8 detector
utils/            → Helper functions
config/           → Settings & constants
scripts/          → Setup & testing
data/             → Videos & results
logs/             → Application logs
```

---

## 🔧 Installation

### Create Virtual Environment
```bash
python3 -m venv venv
```

### Activate (Required Before Any Python Command)
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# You should see (venv) in terminal
```

### Install All Dependencies
```bash
pip install -r requirements.txt
```

### Install Specific Package
```bash
pip install ultralytics          # YOLOv8
pip install fastapi              # Web framework
pip install torch                # Deep learning
pip install google-generativeai   # Gemini API
```

### Freeze Dependencies (After Installing)
```bash
pip freeze > requirements.txt
```

---

## ⚙️ Configuration

### Copy Environment Template
```bash
cp .env.example .env
```

### Edit Environment
```bash
nano .env          # macOS/Linux
# OR
code .env          # VS Code
# OR
notepad .env       # Windows
```

### View Current Configuration
```bash
cat .env
# OR
echo $GOOGLE_API_KEY  # Check specific var
```

### Test Configuration
```bash
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('API Key:', os.getenv('GOOGLE_API_KEY')[:5], '...')
print('Debug:', os.getenv('DEBUG'))
print('Model:', os.getenv('YOLO_MODEL_SIZE'))
"
```

---

## 📦 Models & Data

### Download YOLOv8 Models
```bash
python3 scripts/download_models.py
```

### Models Available
```
yolov8n.pt   (6MB)    - Nano, fastest
yolov8s.pt   (23MB)   - Small, balanced
yolov8m.pt   (49MB)   - Medium, accurate
yolov8l.pt   (94MB)   - Large, very accurate
```

### Initialize Database
```bash
python3 scripts/init_db.py
```

### Check Database Status
```bash
sqlite3 astra.db ".tables"        # List tables
sqlite3 astra.db "SELECT COUNT(*) FROM videos;"  # Count records
```

---

## 🌐 Running the Application

### Development Server (With Auto-Reload)
```bash
python3 app.py
# OR
uvicorn app:app --reload
```

### Production Server (No Reload)
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Specify Different Port
```bash
python3 app.py --port 8001
uvicorn app:app --port 3000
```

### Run in Background (macOS/Linux)
```bash
python3 app.py &
# Stop: kill %1
```

### Access API
```
Browser: http://localhost:8000
Docs:    http://localhost:8000/docs
ReDoc:   http://localhost:8000/redoc
Health:  http://localhost:8000/health
```

---

## 🧪 Testing

### Test Detection on Video
```bash
python3 scripts/test_detection.py --video sample.mp4
```

### Test with Custom ROI
```bash
python3 scripts/test_detection.py \
  --video sample.mp4 \
  --roi "[[100, 100], [500, 100], [500, 300], [100, 300]]"
```

### Run Unit Tests
```bash
pytest tests/
pytest tests/ -v              # Verbose
pytest tests/ --cov           # Coverage report
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# List videos
curl http://localhost:8000/api/videos

# Upload video
curl -X POST http://localhost:8000/api/videos/upload \
  -F "file=@video.mp4"

# Get results
curl http://localhost:8000/api/videos/{video_id}/results
```

---

## 🐳 Docker

### Build Docker Image
```bash
docker build -t astra:latest .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  -v $(pwd)/data:/app/data \
  astra:latest
```

### Docker Compose (Simpler)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Check Running Containers
```bash
docker ps
docker logs container_id
```

---

## 🚀 Deployment

### Deploy to Render
```bash
# 1. Git push
git add .
git commit -m "Initial commit"
git push origin main

# 2. Go to https://render.com
# 3. New Web Service
# 4. Connect GitHub repository
# 5. Configure and deploy

# Access at:
# https://your-service-name.onrender.com
```

### Deploy to Railway
```bash
# Install
npm install -g @railway/cli

# Login & Deploy
railway login
railway init
railway up

# View logs
railway logs
```

### Deploy to Replit
```
1. Go to https://replit.com
2. Import from GitHub
3. Create secrets (.env)
4. Click "Run"
```

---

## 📝 Code Quality

### Format Code (Black)
```bash
black .                    # Format all
black app.py               # Format file
```

### Lint Code (Flake8)
```bash
flake8 .                   # Check all
flake8 app.py              # Check file
flake8 app.py --max-line-length=120
```

### Sort Imports (isort)
```bash
isort .                    # Sort all
isort app.py               # Sort file
```

### Type Check (mypy)
```bash
mypy .
mypy app.py
```

### Full Quality Check
```bash
black . && isort . && flake8 . && mypy .
```

---

## 🔍 Debugging

### View Logs
```bash
tail -f logs/astra.log              # Follow logs
cat logs/astra.log                  # View all
grep ERROR logs/astra.log           # Find errors
```

### Debug Mode
```bash
DEBUG=True python3 app.py           # Enable debug
```

### Python REPL Testing
```bash
python3
>>> from models.detector import HelmetDetector
>>> detector = HelmetDetector()
>>> results = detector.detect(frame)
```

### Check Imports
```bash
python3 -c "import ultralytics; print(ultralytics.__version__)"
python3 -c "import torch; print(torch.__version__)"
python3 -c "import cv2; print(cv2.__version__)"
```

---

## 🧹 Cleanup & Maintenance

### Remove Cache Files
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
rm -rf .pytest_cache
rm -rf .mypy_cache
```

### Clean Database
```bash
rm astra.db
python3 scripts/init_db.py
```

### Clean Downloads/Cache
```bash
rm -rf ~/.cache/pip
rm -rf ~/.yolov8
```

### Full Project Reset
```bash
rm -rf venv logs data/*
rm .env *.db
# Then restart from setup
```

---

## 📊 Monitoring

### System Resources
```bash
# Check memory
python3 -c "import psutil; print(psutil.virtual_memory())"

# Check disk space
df -h

# Check GPU
nvidia-smi                 # If NVIDIA GPU
```

### API Metrics
```bash
# Request count
curl http://localhost:8000/analytics/summary

# Video processing time
time python3 scripts/test_detection.py --video sample.mp4
```

### Process Management
```bash
# Show processes
ps aux | grep python

# Kill process
kill -9 process_id

# Process info
top -pid process_id
```

---

## 🔐 Security

### Generate Secret Key
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Environment Variables Safe
```bash
# Don't commit .env
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

### Check Exposed Secrets
```bash
# Search for hardcoded keys
grep -r "GOOGLE_API_KEY=" .
grep -r "SECRET_KEY=" .
```

---

## 📚 Documentation

### Generate API Docs
```bash
# Auto-generated at:
# http://localhost:8000/docs    (Swagger)
# http://localhost:8000/redoc   (ReDoc)
```

### Generate Code Documentation
```bash
# Install pdoc
pip install pdoc

# Generate HTML docs
pdoc -o docs app
```

### View in Browser
```bash
open docs/app.html              # macOS
xdg-open docs/app.html          # Linux
start docs/app.html             # Windows
```

---

## 🎯 Common Workflows

### First Time Setup (Complete)
```bash
python3 setup_project.py
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env
python3 scripts/download_models.py
python3 scripts/init_db.py
python3 app.py
```

### Daily Development
```bash
source venv/bin/activate
python3 app.py
# Test in another terminal
python3 scripts/test_detection.py --video video.mp4
```

### Before Deployment
```bash
black .
isort .
flake8 .
pytest tests/
git add .
git commit -m "Ready for deployment"
git push origin main
```

### After Deployment
```bash
# Check server
curl https://your-domain/health

# View logs
curl https://your-domain/logs

# Test upload
curl -X POST https://your-domain/api/videos/upload -F "file=@video.mp4"
```

---

## 💾 Git Commands

### Initial Setup
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/user/repo.git
git branch -M main
git push -u origin main
```

### Regular Workflow
```bash
git status                    # Check changes
git add .                     # Stage all
git commit -m "message"       # Commit
git push                      # Push to GitHub
git pull                      # Get updates
```

### Branches
```bash
git checkout -b feature/name   # Create branch
git checkout main              # Switch branch
git merge feature/name         # Merge branch
```

---

## 🆘 Emergency Commands

### Server Won't Start
```bash
# Check port in use
lsof -i :8000

# Kill process on port
kill -9 $(lsof -ti:8000)

# Try different port
python3 app.py --port 8001
```

### Out of Memory
```bash
# Kill resource hog processes
killall python3

# Check RAM
free -h
```

### Git Merge Conflicts
```bash
git status                    # See conflicts
git diff                      # View differences
# Edit files manually
git add .
git commit -m "Resolved conflicts"
git push
```

---

## 📞 Quick Links

- 📚 **FastAPI Docs**: https://fastapi.tiangolo.com/
- 🎯 **YOLOv8 Guide**: https://docs.ultralytics.com/
- 🤖 **Gemini API**: https://ai.google.dev/
- 🐳 **Docker Hub**: https://hub.docker.com/
- 🚀 **Render Docs**: https://render.com/docs
- 🚂 **Railway Docs**: https://railway.app/docs

---

**Bookmark this file!** 📌
Save as: `CHEATSHEET.md`
