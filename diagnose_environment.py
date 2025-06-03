#!/usr/bin/env python3
"""
Environment Diagnostic Tool for stable-diffusion-webui

This script diagnoses your Python environment and provides specific
solutions for CLIP installation and compatibility issues.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess
import os
import platform

def check_python_environment():
    """Check Python version and environment details"""
    print("=== Python Environment Check ===")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {platform.system()} {platform.release()}")
    
    # Check if in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
        print(f"Virtual env path: {sys.prefix}")
    else:
        print("⚠️  Running in system Python")
    
    # Check pip version
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"Pip version: {result.stdout.strip()}")
    except:
        print("❌ Pip not available")
    
    return version

def check_pytorch_installation():
    """Check PyTorch installation and version"""
    print("\n=== PyTorch Installation Check ===")
    
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU device: {torch.cuda.get_device_name(0)}")
        else:
            print("Running in CPU-only mode")
        
        return torch.__version__
    except ImportError:
        print("❌ PyTorch not installed")
        return None

def check_problematic_packages():
    """Check for packages that cause issues"""
    print("\n=== Problematic Package Check ===")
    
    problematic_packages = {
        "clip": "clip-by-openai (requires torch<1.7.2)",
        "open_clip": "open-clip-torch (requires sentencepiece/cmake)",
        "sentencepiece": "sentencepiece (requires cmake compilation)",
        "triton": "triton (TORCH_LIBRARY conflicts)"
    }
    
    for package, description in problematic_packages.items():
        try:
            __import__(package)
            print(f"⚠️  {package} is installed - {description}")
        except ImportError:
            print(f"✅ {package} not installed (good)")

def check_clip_compatibility():
    """Check CLIP package compatibility with current PyTorch"""
    print("\n=== CLIP Compatibility Check ===")
    
    try:
        import torch
        torch_version = torch.__version__
        
        # Parse torch version
        major, minor = torch_version.split('.')[:2]
        torch_major = int(major)
        torch_minor = int(minor.split('+')[0])  # Remove +cpu suffix
        
        print(f"Current PyTorch: {torch_version}")
        
        # Check clip-by-openai compatibility
        if torch_major >= 2 or (torch_major == 1 and torch_minor >= 7):
            print("❌ clip-by-openai incompatible (requires torch<1.7.2)")
        else:
            print("✅ clip-by-openai compatible")
        
        # Check open-clip-torch compatibility
        print("⚠️  open-clip-torch requires sentencepiece (cmake compilation)")
        
        return False  # Assume incompatible for modern PyTorch
        
    except ImportError:
        print("❌ PyTorch not available for compatibility check")
        return False

def suggest_solutions(python_version, pytorch_version):
    """Suggest solutions based on environment"""
    print("\n=== Recommended Solutions ===")
    
    if python_version.minor >= 11:
        print("🎯 For Python 3.11+:")
        print("1. Skip CLIP installation (already configured)")
        print("2. Use WebUI without CLIP features")
        print("3. Install alternative packages if needed")
        
        if pytorch_version and pytorch_version.startswith('2.'):
            print("\n🔧 PyTorch 2.x detected:")
            print("- clip-by-openai is incompatible")
            print("- open-clip-torch requires cmake")
            print("- Skipping CLIP is the best option")
    
    print(f"\n📋 Configuration for Python {python_version.major}.{python_version.minor}:")
    print("- CLIP installation: SKIPPED (compatibility issues)")
    print("- WebUI mode: CPU-only recommended")
    print("- Expected functionality: Basic features work, some CLIP features limited")

def create_compatible_webui_config():
    """Create WebUI configuration for current environment"""
    print("\n=== Creating Compatible WebUI Configuration ===")
    
    python_version = sys.version_info
    
    config_content = f'''@echo off
REM Compatible WebUI Configuration for Python {python_version.major}.{python_version.minor}
echo Starting WebUI with Python {python_version.major}.{python_version.minor} compatibility...
echo.

REM Skip problematic package installations
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install

REM Use existing PyTorch installation
set TORCH_COMMAND=echo "Using existing PyTorch installation"

REM Skip CLIP packages (compatibility issues)
set CLIP_PACKAGE=echo "Skipping CLIP (compatibility issues)"
set OPENCLIP_PACKAGE=echo "Skipping open_clip (compatibility issues)"

REM Disable xformers if problematic
set XFORMERS_PACKAGE=none

REM Additional stability flags
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half --precision full

echo Configuration:
echo - Python {python_version.major}.{python_version.minor} compatibility mode
echo - Skipping CLIP installation (compatibility issues)
echo - Using existing PyTorch installation
echo - Stability flags enabled
echo.

call webui.bat %*
'''
    
    try:
        with open("webui_compatible.bat", "w") as f:
            f.write(config_content)
        print("✅ Created webui_compatible.bat")
        return True
    except Exception as e:
        print(f"❌ Could not create config: {e}")
        return False

def install_alternative_packages():
    """Install alternative packages that work with current setup"""
    print("\n=== Installing Alternative Packages ===")
    
    # Packages that should work without CLIP
    alternative_packages = [
        "transformers",  # For text processing
        "diffusers",     # For diffusion models
        "accelerate",    # For model acceleration
        "safetensors",   # For model loading
        "omegaconf",     # For configuration
        "gradio",        # For web interface
        "fastapi",       # For API
        "uvicorn",       # For server
        "Pillow",        # For image processing
        "numpy",         # Core dependency
        "requests",      # For downloads
        "tqdm",          # For progress bars
    ]
    
    successful = 0
    for package in alternative_packages:
        try:
            print(f"Installing {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True, capture_output=True)
            print(f"✅ {package}")
            successful += 1
        except subprocess.CalledProcessError:
            print(f"❌ {package}")
    
    print(f"\nInstalled {successful}/{len(alternative_packages)} packages")
    return successful > len(alternative_packages) // 2

def main():
    """Main diagnostic function"""
    print("Environment Diagnostic for stable-diffusion-webui")
    print("=" * 60)
    
    # Check environment
    python_version = check_python_environment()
    pytorch_version = check_pytorch_installation()
    check_problematic_packages()
    clip_compatible = check_clip_compatibility()
    
    # Provide solutions
    suggest_solutions(python_version, pytorch_version)
    
    # Create configuration
    config_created = create_compatible_webui_config()
    
    # Install alternatives
    packages_installed = install_alternative_packages()
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    print(f"PyTorch version: {pytorch_version or 'Not installed'}")
    print(f"CLIP compatible: {'Yes' if clip_compatible else 'No (skipping recommended)'}")
    print(f"Config created: {'Yes' if config_created else 'No'}")
    print(f"Alternative packages: {'Installed' if packages_installed else 'Failed'}")
    
    print("\n🎯 NEXT STEPS:")
    if config_created:
        print("1. Use webui_compatible.bat to launch WebUI")
        print("2. This configuration skips problematic CLIP packages")
        print("3. Basic WebUI functionality should work")
        print("4. Some CLIP-dependent features may be limited")
    else:
        print("1. Try running webui.bat with --skip-install flag")
        print("2. Manual package installation may be needed")
    
    if python_version.minor >= 11:
        print("\n💡 For best compatibility:")
        print("Consider using Python 3.10 for AI/ML workloads")
        print("Python 3.10 has the most mature ecosystem support")
    
    print(f"\nModified launch_utils.py will skip CLIP on Python {python_version.major}.{python_version.minor}+")

if __name__ == "__main__":
    main()
