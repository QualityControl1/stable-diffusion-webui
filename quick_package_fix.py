#!/usr/bin/env python3
"""
Quick Package Fix for sentencepiece/open_clip build issues

This script provides immediate solutions to avoid compilation issues.
"""

import sys
import subprocess

def install_prebuilt_packages():
    """Install pre-built versions of problematic packages"""
    print("Installing pre-built packages to avoid compilation...")
    
    packages = [
        "open-clip-torch==2.24.0",
        "clip-by-openai", 
        "transformers",
        "tokenizers",
        "sentencepiece==0.1.99"  # Older version with wheels
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True)
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"⚠️  {package} failed, continuing...")

def test_imports():
    """Test if packages import correctly"""
    print("\nTesting package imports...")
    
    test_packages = ["torch", "open_clip", "clip", "transformers"]
    
    for package in test_packages:
        try:
            __import__(package)
            print(f"✅ {package} working")
        except ImportError:
            print(f"❌ {package} not working")

if __name__ == "__main__":
    print("Quick Package Fix for Python 3.13 Build Issues")
    print("=" * 50)
    
    install_prebuilt_packages()
    test_imports()
    
    print("\n✅ Quick fix completed!")
    print("Try running webui.bat now.")
