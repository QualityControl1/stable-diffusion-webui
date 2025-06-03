#!/usr/bin/env python3
"""
Windows Build Tools Fix for Python 3.13 and stable-diffusion-webui

This script resolves the sentencepiece/open_clip build dependency issues
by installing required build tools and using alternative package sources.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess
import os
import platform

def check_build_environment():
    """Check current build environment and tools"""
    print("=== Build Environment Check ===")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check if we're on Windows
    if platform.system() != "Windows":
        print("This script is designed for Windows")
        return False
    
    # Check for Visual Studio Build Tools
    vs_paths = [
        r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools", 
        r"C:\Program Files\Microsoft Visual Studio\2022\Community",
        r"C:\Program Files\Microsoft Visual Studio\2019\Community"
    ]
    
    vs_found = False
    for path in vs_paths:
        if os.path.exists(path):
            print(f"✅ Visual Studio found at: {path}")
            vs_found = True
            break
    
    if not vs_found:
        print("❌ Visual Studio Build Tools not found")
    
    # Check for cl.exe (MSVC compiler)
    try:
        result = subprocess.run(["cl"], capture_output=True, text=True)
        print("✅ MSVC compiler (cl.exe) available")
    except FileNotFoundError:
        print("❌ MSVC compiler (cl.exe) not found")
    
    return vs_found

def install_prebuilt_packages():
    """Install pre-built packages to avoid compilation"""
    print("\n=== Installing Pre-built Packages ===")
    
    # Strategy 1: Install sentencepiece from conda-forge (if conda available)
    try:
        result = subprocess.run(["conda", "--version"], capture_output=True, text=True, check=True)
        print(f"Conda available: {result.stdout.strip()}")
        
        print("Installing sentencepiece via conda...")
        subprocess.run([
            "conda", "install", "sentencepiece", "-c", "conda-forge", "-y"
        ], check=True)
        print("✅ sentencepiece installed via conda")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Conda not available, trying pip alternatives...")
    
    # Strategy 2: Try installing compatible versions
    compatible_packages = [
        "sentencepiece==0.1.99",  # Older version with wheels
        "sentencepiece==0.2.0",   # Alternative version
    ]
    
    for package in compatible_packages:
        try:
            print(f"Trying {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True, capture_output=True)
            print(f"✅ {package} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ {package} failed")
            continue
    
    return False

def install_build_tools():
    """Guide user through installing Visual Studio Build Tools"""
    print("\n=== Installing Visual Studio Build Tools ===")
    
    print("""
To compile Python packages on Windows, you need Visual Studio Build Tools.

OPTION 1: Download and install Visual Studio Build Tools 2022
1. Go to: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
2. Download "Build Tools for Visual Studio 2022"
3. Run the installer
4. Select "C++ build tools" workload
5. Install and restart your computer

OPTION 2: Install via winget (if available)
Run this command in an Administrator PowerShell:
winget install Microsoft.VisualStudio.2022.BuildTools

OPTION 3: Use chocolatey (if available)
choco install visualstudio2022buildtools --package-parameters "--add Microsoft.VisualStudio.Workload.VCTools"
""")
    
    response = input("Have you installed Visual Studio Build Tools? (y/n): ")
    return response.lower() == 'y'

def modify_webui_packages():
    """Modify webui to use alternative package sources"""
    print("\n=== Modifying WebUI Package Configuration ===")
    
    # Check if launch_utils.py exists
    launch_utils_path = "modules/launch_utils.py"
    if not os.path.exists(launch_utils_path):
        print(f"❌ {launch_utils_path} not found")
        return False
    
    try:
        # Read the current file
        with open(launch_utils_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create backup
        with open(launch_utils_path + ".backup", 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created backup: {launch_utils_path}.backup")
        
        # Modify the open_clip package URL to use a version with wheels
        old_openclip = 'openclip_package = os.environ.get(\'OPENCLIP_PACKAGE\', "https://github.com/mlfoundations/open_clip/archive/bb6e834e9c70d9c27d0dc3ecedeebeaeb1ffad6b.zip")'
        new_openclip = 'openclip_package = os.environ.get(\'OPENCLIP_PACKAGE\', "open-clip-torch==2.24.0")'
        
        if old_openclip in content:
            content = content.replace(old_openclip, new_openclip)
            print("✅ Modified open_clip package to use PyPI version")
        else:
            print("⚠️  open_clip package line not found, manual modification needed")
        
        # Write the modified file
        with open(launch_utils_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Modified {launch_utils_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error modifying {launch_utils_path}: {e}")
        return False

def create_alternative_webui_config():
    """Create WebUI configuration that avoids problematic packages"""
    print("\n=== Creating Alternative WebUI Configuration ===")
    
    config_content = """@echo off
REM WebUI configuration that avoids build issues on Python 3.13
echo Starting WebUI with build-friendly configuration...

REM Use PyPI packages instead of GitHub archives
set OPENCLIP_PACKAGE=open-clip-torch==2.24.0
set CLIP_PACKAGE=clip-by-openai

REM Skip problematic installations
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install

REM Use CPU-only PyTorch
set TORCH_COMMAND=pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cpu

echo Configuration:
echo - Using PyPI packages instead of GitHub archives
echo - Skipping automatic package installation
echo - CPU-only mode for compatibility
echo.

call webui.bat %*
"""
    
    try:
        with open("webui_build_friendly.bat", "w") as f:
            f.write(config_content)
        print("✅ Created webui_build_friendly.bat")
        return True
    except Exception as e:
        print(f"❌ Could not create config file: {e}")
        return False

def manual_package_installation():
    """Manually install packages that typically cause build issues"""
    print("\n=== Manual Package Installation ===")
    
    packages_to_install = [
        # Try different versions/sources for problematic packages
        ("open-clip-torch", "2.24.0"),
        ("clip-by-openai", ""),
        ("transformers", ""),
        ("tokenizers", ""),
    ]
    
    for package, version in packages_to_install:
        try:
            if version:
                cmd = [sys.executable, "-m", "pip", "install", f"{package}=={version}"]
            else:
                cmd = [sys.executable, "-m", "pip", "install", package]
            
            print(f"Installing {package}...")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ {package} installed successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} installation failed: {e}")
            continue

def test_package_imports():
    """Test if the installed packages work"""
    print("\n=== Testing Package Imports ===")
    
    test_packages = [
        "torch",
        "torchvision", 
        "open_clip",
        "clip",
        "transformers"
    ]
    
    for package in test_packages:
        try:
            __import__(package)
            print(f"✅ {package} imports successfully")
        except ImportError as e:
            print(f"❌ {package} import failed: {e}")

def main():
    """Main function"""
    print("Windows Build Tools Fix for Python 3.13")
    print("=" * 50)
    
    # Check build environment
    build_tools_available = check_build_environment()
    
    # Try different strategies
    success = False
    
    print("\n" + "=" * 50)
    print("STRATEGY 1: Use Pre-built Packages")
    print("=" * 50)
    
    if install_prebuilt_packages():
        success = True
        print("✅ Pre-built packages installed successfully")
    
    if not success and not build_tools_available:
        print("\n" + "=" * 50)
        print("STRATEGY 2: Install Build Tools")
        print("=" * 50)
        
        if install_build_tools():
            # Re-check after installation
            build_tools_available = check_build_environment()
    
    print("\n" + "=" * 50)
    print("STRATEGY 3: Modify WebUI Configuration")
    print("=" * 50)
    
    modify_webui_packages()
    create_alternative_webui_config()
    
    print("\n" + "=" * 50)
    print("STRATEGY 4: Manual Package Installation")
    print("=" * 50)
    
    manual_package_installation()
    
    # Test the results
    test_package_imports()
    
    print("\n" + "=" * 50)
    print("RECOMMENDATIONS")
    print("=" * 50)
    
    if success:
        print("✅ Build issues likely resolved!")
        print("\nNext steps:")
        print("1. Try running: webui_build_friendly.bat")
        print("2. If that works, try the regular webui.bat")
        print("3. Monitor for any remaining build errors")
    else:
        print("⚠️  Build tools may still be needed")
        print("\nOptions:")
        print("1. Install Visual Studio Build Tools (recommended)")
        print("2. Use webui_build_friendly.bat (skips problematic packages)")
        print("3. Consider switching to Python 3.10 for better compatibility")
    
    print(f"\nCurrent Python: {sys.version}")
    print("For best compatibility, consider Python 3.10-3.12")

if __name__ == "__main__":
    main()
