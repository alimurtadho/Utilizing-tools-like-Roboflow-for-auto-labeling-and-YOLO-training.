"""
QUICK START SCRIPT
Automated setup and initialization
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd: str, description: str) -> bool:
    """Run shell command and report result"""
    print(f"\n⏳ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Done")
            return True
        else:
            print(f"❌ {description} - Failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def main():
    """Main setup flow"""
    print("\n" + "="*70)
    print("🏍️  HELMET DETECTION SYSTEM - QUICK START")
    print("="*70)
    
    steps = []
    
    # Step 1: Project structure
    if not Path("api").exists():
        print("\n📁 Creating project structure...")
        run_command("python3 setup_project.py", "Project structure")
        steps.append(("Project Structure", True))
    else:
        print("\n✅ Project structure already exists")
        steps.append(("Project Structure", True))
    
    # Step 2: Virtual environment
    print("\n🔧 Setting up Python environment...")
    venv_path = Path("venv")
    if not venv_path.exists():
        run_command("python3 -m venv venv", "Virtual environment")
        steps.append(("Virtual Environment", True))
    else:
        print("✅ Virtual environment already exists")
        steps.append(("Virtual Environment", True))
    
    # Step 3: Install dependencies
    if sys.platform == "win32":
        pip_cmd = "venv\\Scripts\\pip install -r requirements.txt"
        activate = "venv\\Scripts\\activate.bat"
    else:
        pip_cmd = "source venv/bin/activate && pip install -r requirements.txt"
        activate = "source venv/bin/activate"
    
    success = run_command(pip_cmd, "Installing dependencies")
    steps.append(("Dependencies", success))
    
    # Step 4: Environment configuration
    if not Path(".env").exists():
        print("\n🔐 Creating .env file...")
        run_command("cp .env.example .env", "Environment file")
        print("⚠️  IMPORTANT: Edit .env file with your API keys!")
        print("   - GOOGLE_API_KEY: Get from https://ai.google.dev/")
        steps.append(("Environment Config", True))
    else:
        print("✅ .env file already exists")
        steps.append(("Environment Config", True))
    
    # Step 5: Database initialization
    if sys.platform == "win32":
        db_cmd = "venv\\Scripts\\python scripts/init_db.py"
    else:
        db_cmd = "source venv/bin/activate && python scripts/init_db.py"
    
    success = run_command(db_cmd, "Database initialization")
    steps.append(("Database", success))
    
    # Step 6: Download models
    if sys.platform == "win32":
        model_cmd = "venv\\Scripts\\python scripts/download_models.py"
    else:
        model_cmd = "source venv/bin/activate && python scripts/download_models.py"
    
    print("\n📥 Downloading YOLOv8 models (this may take a few minutes)...")
    success = run_command(model_cmd, "Model download")
    steps.append(("Models", success))
    
    # Summary
    print("\n" + "="*70)
    print("📋 SETUP SUMMARY")
    print("="*70)
    
    for step, completed in steps:
        status = "✅" if completed else "❌"
        print(f"{status} {step}")
    
    all_success = all(s[1] for s in steps)
    
    if all_success:
        print("\n" + "="*70)
        print("✅ SETUP COMPLETE!")
        print("="*70)
        print("\n🚀 Next Steps:\n")
        print("1. Edit .env file with your Google API key:")
        print("   GOOGLE_API_KEY=your_key_here\n")
        print("2. Run the development server:")
        if sys.platform == "win32":
            print("   venv\\Scripts\\activate")
            print("   python app.py")
        else:
            print("   source venv/bin/activate")
            print("   python app.py")
        print("\n3. Access the API:")
        print("   http://localhost:8000")
        print("   http://localhost:8000/docs (API documentation)")
        print("\n4. Test detection:")
        if sys.platform == "win32":
            print("   venv\\Scripts\\python scripts/test_detection.py --video sample.mp4")
        else:
            print("   python scripts/test_detection.py --video sample.mp4")
        print("\n📖 For deployment instructions:")
        print("   See DEPLOYMENT_SETUP.md")
        print("\n" + "="*70 + "\n")
    else:
        print("\n❌ Some setup steps failed. Please check the errors above.")
        print("You may need to install additional system dependencies.")
    
    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())
