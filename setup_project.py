#!/usr/bin/env python3
"""
Automated Project Setup Script
Generates complete project structure for Helmet Detection System
"""

import os
import sys
from pathlib import Path
import json

def create_directory_structure(base_path):
    """Create all necessary directories"""
    directories = [
        "api",
        "models",
        "utils",
        "data/videos",
        "data/outputs",
        "data/annotations",
        "config",
        "scripts",
        "tests",
        "frontend",
        "logs",
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}/")
    
    print("✅ Directory structure created!\n")

def create_files(base_path):
    """Create necessary Python files"""
    print("📝 Creating project files...")
    
    # __init__.py files
    init_files = [
        "api/__init__.py",
        "models/__init__.py",
        "utils/__init__.py",
        "config/__init__.py",
        "scripts/__init__.py",
        "tests/__init__.py",
    ]
    
    for file_path in init_files:
        full_path = base_path / file_path
        full_path.touch(exist_ok=True)
        print(f"  ✓ {file_path}")
    
    print("✅ Init files created!\n")

def create_env_file(base_path):
    """Create .env.example file"""
    print("🔐 Creating .env.example...")
    
    env_content = """# Helmet Detection System - Configuration

# API & Server
DEBUG=True
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your-secret-key-here-generate-with-secrets

# Database
DATABASE_URL=sqlite:///astra.db
# Alternative: postgresql://user:password@localhost/astradb

# Google Gemini API
GOOGLE_API_KEY=your-google-api-key-here

# Hugging Face (optional)
HUGGINGFACE_TOKEN=your-hf-token-here

# Model Configuration
YOLO_MODEL_SIZE=n  # n (nano), s (small), m (medium), l (large)
CONFIDENCE_THRESHOLD=0.70
NMS_THRESHOLD=0.45

# Video Processing
MAX_VIDEO_SIZE_MB=100
FRAMES_PER_SECOND=5
PROCESS_TIMEOUT_MINUTES=15

# Storage
STORAGE_PATH=./data
MAX_VIDEOS_PER_USER=100

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/astra.log

# Email (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Optional: LLM Selection
LLM_PROVIDER=gemini  # gemini, openrouter, huggingface
"""
    
    env_path = base_path / ".env.example"
    env_path.write_text(env_content)
    print(f"  ✓ .env.example created")
    
    # Create .env if it doesn't exist
    env_local = base_path / ".env"
    if not env_local.exists():
        env_local.write_text(env_content.replace("your-", "CHANGE_ME_"))
        print(f"  ✓ .env created (configure this file!)")
    
    print("✅ Environment files created!\n")

def create_config_files(base_path):
    """Create configuration modules"""
    print("⚙️  Creating config modules...")
    
    # settings.py
    settings_content = '''"""Configuration Settings"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application Settings"""
    
    # API
    APP_NAME: str = "Helmet Detection System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///astra.db")
    
    # AI/ML
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    
    # Model Config
    YOLO_MODEL_SIZE: str = os.getenv("YOLO_MODEL_SIZE", "n")  # n, s, m, l, x
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
    NMS_THRESHOLD: float = float(os.getenv("NMS_THRESHOLD", "0.45"))
    
    # Video Processing
    MAX_VIDEO_SIZE_MB: int = int(os.getenv("MAX_VIDEO_SIZE_MB", "100"))
    FRAMES_PER_SECOND: int = int(os.getenv("FRAMES_PER_SECOND", "5"))
    PROCESS_TIMEOUT_MINUTES: int = int(os.getenv("PROCESS_TIMEOUT_MINUTES", "15"))
    
    # Storage
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./data")
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/astra.log")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
'''
    
    settings_path = base_path / "config" / "settings.py"
    settings_path.write_text(settings_content)
    print(f"  ✓ config/settings.py")
    
    # constants.py
    constants_content = '''"""Application Constants"""

# Detection Classes
DETECTION_CLASSES = {
    0: "motorcycle",
    1: "person",
    2: "helmet",
    3: "no-helmet"
}

# Status Codes
STATUS_PENDING = "pending"
STATUS_PROCESSING = "processing"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

# Video Formats
ALLOWED_FORMATS = {"mp4", "avi", "mov", "mkv", "flv", "wmv"}

# Batch Sizes
BATCH_SIZE_INFERENCE = 8
BATCH_SIZE_TRACKING = 1

# Confidence Thresholds
MIN_HELMET_CONFIDENCE = 0.70
MIN_MOTORCYCLE_CONFIDENCE = 0.60
MIN_PERSON_CONFIDENCE = 0.65
'''
    
    constants_path = base_path / "config" / "constants.py"
    constants_path.write_text(constants_content)
    print(f"  ✓ config/constants.py")
    
    print("✅ Config modules created!\n")

def create_gitignore(base_path):
    """Create .gitignore file"""
    print("🚫 Creating .gitignore...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local
.env.*.local

# Data & Logs
data/
logs/
*.log
astra.db
.cache/

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Models
models/weights/
*.pt
*.onnx

# Node (for frontend)
node_modules/
.next/
dist/
build/
"""
    
    gitignore_path = base_path / ".gitignore"
    gitignore_path.write_text(gitignore_content)
    print(f"  ✓ .gitignore created\n")

def create_readme(base_path):
    """Create README.md"""
    print("📖 Creating README.md...")
    
    readme_content = """# 🏍️ Helmet Compliance & Occupancy Counting System

Automated AI-powered detection of motorcycle helmet usage and occupancy from video footage.

## ✨ Features

- ✅ Automatic motorcycle detection
- ✅ Helmet compliance detection
- ✅ Occupancy counting (riders + passengers)
- ✅ Line-crossing logic for unique counting
- ✅ Real-time processing status
- ✅ Compliance analytics & reporting
- ✅ Video annotation with bounding boxes

## 🚀 Quick Start

### 1. Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env with your Google API key
```

### 3. Run
```bash
python3 app.py
# Access: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 4. Test
```bash
python3 scripts/test_detection.py --video sample_video.mp4
```

## 📦 Project Structure

```
astra/
├── api/           # FastAPI endpoints
├── models/        # YOLOv8, Tracking, Analysis
├── utils/         # Video processing, Gemini API
├── config/        # Settings & constants
├── scripts/       # Training, testing utilities
├── data/          # Videos, outputs, annotations
├── frontend/      # Web UI (optional)
└── tests/         # Unit & integration tests
```

## 🔑 Free Services Used

- **YOLOv8**: Open source object detection
- **Google Gemini**: Free LLM for analysis (1M tokens/day)
- **FastAPI**: Modern Python web framework
- **Render/Railway**: Free Python deployment

## 📊 API Endpoints

- `POST /api/videos/upload` - Upload video
- `GET /api/videos` - List videos
- `POST /api/videos/{id}/process` - Start processing
- `GET /api/videos/{id}/results` - Get results
- `GET /api/analytics/summary` - Get summary stats

## 🎯 Deployment

### Local Development
```bash
uvicorn app:app --reload
```

### Production (Render.com)
```bash
# See DEPLOYMENT_SETUP.md for step-by-step
```

## 📚 Documentation

- [DEPLOYMENT_SETUP.md](./DEPLOYMENT_SETUP.md) - Complete deployment guide
- [API_REFERENCE.md](./API_REFERENCE.md) - API documentation
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Development guide

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 📞 Support

- Issues: GitHub Issues
- Questions: GitHub Discussions
- Email: support@astra.local

---

**Status**: MVP Phase ✅
**Version**: 1.0
**Last Updated**: January 31, 2026
"""
    
    readme_path = base_path / "README.md"
    readme_path.write_text(readme_content)
    print(f"  ✓ README.md created\n")

def print_next_steps():
    """Print next steps"""
    print("\n" + "="*60)
    print("✅ PROJECT STRUCTURE CREATED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Next Steps:\n")
    print("1️⃣  Install dependencies:")
    print("   pip install -r requirements.txt\n")
    print("2️⃣  Configure environment:")
    print("   cp .env.example .env")
    print("   # Edit .env with your API keys\n")
    print("3️⃣  Download YOLOv8 model:")
    print("   python3 scripts/download_models.py\n")
    print("4️⃣  Initialize database:")
    print("   python3 scripts/init_db.py\n")
    print("5️⃣  Run development server:")
    print("   python3 app.py\n")
    print("6️⃣  Access API documentation:")
    print("   http://localhost:8000/docs\n")
    print("="*60)
    print("📖 For deployment guide, see: DEPLOYMENT_SETUP.md")
    print("="*60 + "\n")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("🏍️  HELMET DETECTION SYSTEM - PROJECT SETUP")
    print("="*60 + "\n")
    
    base_path = Path.cwd()
    print(f"📍 Setting up in: {base_path}\n")
    
    try:
        create_directory_structure(base_path)
        create_files(base_path)
        create_env_file(base_path)
        create_config_files(base_path)
        create_gitignore(base_path)
        create_readme(base_path)
        print_next_steps()
        
        return 0
    except Exception as e:
        print(f"\n❌ Error during setup: {e}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
