#!/usr/bin/env python3
"""
Install Safe Packages for stable-diffusion-webui on Python 3.13

This script installs only packages that don't require cmake/C++ compilation.
"""

import sys
import subprocess

def install_safe_packages():
    """Install packages that have wheels for Python 3.13"""
    print("Installing safe packages (no compilation required)...")
    
    # Core packages that should have wheels
    safe_packages = [
        "Pillow>=9.0.0",
        "numpy>=1.21.0", 
        "opencv-python>=4.6.0",
        "requests>=2.28.0",
        "tqdm>=4.64.0",
        "omegaconf>=2.2.0",
        "safetensors>=0.3.0",
        "accelerate>=0.20.0",
        "diffusers>=0.20.0",
        "transformers>=4.30.0",
        "gradio>=3.40.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "psutil>=5.9.0",
        "scipy>=1.9.0",
        "scikit-image>=0.19.0",
        "imageio>=2.22.0",
        "realesrgan>=0.3.0",
        "basicsr>=1.4.2",
        "gfpgan>=1.3.8",
        "kornia>=0.6.8",
        "lark>=1.1.5",
        "inflection>=0.5.1",
        "GitPython>=3.1.30",
        "torchsde>=0.2.5",
        "einops>=0.6.1",
        "jsonmerge>=1.9.0",
        "clean-fid>=0.1.35",
        "resize-right>=0.0.2",
        "torchdiffeq>=0.2.3",
        "piexif>=1.1.3",
        "fonts>=0.0.3",
        "font-roboto>=0.0.1",
        "timm>=0.9.2",
        "addict>=2.4.0",
        "yapf>=0.32.0",
        "future>=0.18.3",
        "httpcore>=0.15",
        "pydantic>=1.10.8",
        "packaging>=21.3",
        "filelock>=3.8.0",
        "networkx>=2.8",
        "jinja2>=3.1.2",
        "markupsafe>=2.1.1",
        "certifi>=2022.12.7",
        "charset-normalizer>=3.1.0",
        "idna>=3.4",
        "urllib3>=1.26.15",
        "click>=8.1.3",
        "colorama>=0.4.6",
        "h11>=0.14.0",
        "typing-extensions>=4.5.0",
        "pyyaml>=6.0",
        "regex>=2023.6.3",
        "ftfy>=6.1.1",
        "blendmodes>=2022",
        "pytorch-lightning>=2.0.0",
        "torchmetrics>=0.11.4",
    ]
    
    successful = 0
    failed = 0
    
    for package in safe_packages:
        try:
            print(f"Installing {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package, "--no-deps"
            ], capture_output=True, text=True, check=True)
            print(f"✅ {package}")
            successful += 1
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} - {e}")
            failed += 1
            continue
    
    print(f"\nResults: {successful} successful, {failed} failed")
    return successful > 0

def install_core_dependencies():
    """Install absolutely essential packages"""
    print("\nInstalling core dependencies...")
    
    core_packages = [
        "torch==2.7.0",  # Should already be installed
        "torchvision==0.22.0",
        "Pillow",
        "numpy", 
        "gradio",
        "fastapi",
        "uvicorn",
        "requests",
        "tqdm",
        "omegaconf",
        "safetensors"
    ]
    
    for package in core_packages:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True, capture_output=True)
            print(f"✅ {package}")
        except subprocess.CalledProcessError:
            print(f"❌ {package}")

def test_imports():
    """Test if essential packages can be imported"""
    print("\nTesting package imports...")
    
    test_packages = [
        "torch",
        "torchvision", 
        "PIL",
        "numpy",
        "gradio",
        "fastapi",
        "transformers",
        "diffusers",
        "safetensors"
    ]
    
    working = 0
    for package in test_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
            working += 1
        except ImportError:
            print(f"❌ {package}")
    
    print(f"\nWorking packages: {working}/{len(test_packages)}")
    return working >= len(test_packages) // 2  # At least half should work

def main():
    print("Safe Package Installation for Python 3.13")
    print("=" * 50)
    print("Installing packages that don't require cmake/compilation...")
    print()
    
    # Install core dependencies first
    install_core_dependencies()
    
    # Install additional safe packages
    success = install_safe_packages()
    
    # Test the installation
    imports_working = test_imports()
    
    print("\n" + "=" * 50)
    print("INSTALLATION SUMMARY")
    print("=" * 50)
    
    if success and imports_working:
        print("✅ Safe packages installed successfully!")
        print("\nNext steps:")
        print("1. Try running: webui_no_compilation.bat")
        print("2. This should start WebUI without compilation errors")
        print("3. It will run in CPU-only mode but should be functional")
    else:
        print("⚠️  Some packages failed to install")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Try upgrading pip: python -m pip install --upgrade pip")
        print("3. Clear pip cache: pip cache purge")
        print("4. Consider using Python 3.10 for better compatibility")
    
    print(f"\nPython version: {sys.version}")
    print("Note: Some advanced features may not work without CLIP/open_clip")

if __name__ == "__main__":
    main()
