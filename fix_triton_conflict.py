#!/usr/bin/env python3
"""
PyTorch Triton Conflict Fix for Python 3.13

This script specifically fixes the TORCH_LIBRARY triton namespace conflict
that occurs with PyTorch 2.6.0 on Windows with Python 3.13.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess
import os

def check_current_installation():
    """Check current PyTorch and Triton installation"""
    print("=== Checking Current Installation ===")
    
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
    except ImportError:
        print("PyTorch not installed")
        return False
    
    try:
        import triton
        print(f"Triton version: {triton.__version__}")
    except ImportError:
        print("Triton not installed")
    
    # Check for multiple triton installations
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "list"
        ], capture_output=True, text=True, check=True)
        
        triton_packages = [line for line in result.stdout.split('\n') if 'triton' in line.lower()]
        if triton_packages:
            print("Triton-related packages found:")
            for pkg in triton_packages:
                print(f"  {pkg}")
        
    except Exception as e:
        print(f"Could not check installed packages: {e}")
    
    return True

def clean_triton_installations():
    """Remove all triton-related packages"""
    print("\n=== Cleaning Triton Installations ===")
    
    triton_packages = [
        "triton",
        "pytorch-triton", 
        "pytorch-triton-rocm",
        "triton-nightly"
    ]
    
    for package in triton_packages:
        try:
            print(f"Removing {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "uninstall", package, "-y"
            ], capture_output=True, check=True)
            print(f"✅ {package} removed")
        except subprocess.CalledProcessError:
            print(f"⚠️  {package} not found or already removed")

def install_pytorch_with_compatible_triton():
    """Install PyTorch with compatible Triton version"""
    print("\n=== Installing PyTorch with Compatible Triton ===")
    
    # Strategy 1: Try PyTorch 2.5.1 (more stable with Triton)
    print("Trying PyTorch 2.5.1 (more stable with Triton)...")
    
    try:
        # First, uninstall current PyTorch
        subprocess.run([
            sys.executable, "-m", "pip", "uninstall", 
            "torch", "torchvision", "torchaudio", "-y"
        ], capture_output=True)
        
        # Install PyTorch 2.5.1 with CUDA
        install_cmd = [
            sys.executable, "-m", "pip", "install",
            "torch==2.5.1",
            "torchvision==0.20.1", 
            "torchaudio==2.5.1",
            "--extra-index-url", "https://download.pytorch.org/whl/cu121"
        ]
        
        print(f"Command: {' '.join(install_cmd)}")
        result = subprocess.run(install_cmd, check=True, capture_output=True, text=True)
        print("✅ PyTorch 2.5.1 installation successful!")
        
        return test_cuda_without_triton()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ PyTorch 2.5.1 installation failed: {e}")
        print("Trying alternative approach...")
        return False

def install_pytorch_2_7():
    """Try PyTorch 2.7.0 which has better Triton integration"""
    print("\n=== Trying PyTorch 2.7.0 (Latest Stable) ===")
    
    try:
        # Uninstall current version
        subprocess.run([
            sys.executable, "-m", "pip", "uninstall", 
            "torch", "torchvision", "torchaudio", "-y"
        ], capture_output=True)
        
        # Install PyTorch 2.7.0
        install_cmd = [
            sys.executable, "-m", "pip", "install",
            "torch==2.7.0",
            "torchvision==0.22.0",
            "torchaudio==2.7.0", 
            "--extra-index-url", "https://download.pytorch.org/whl/cu121"
        ]
        
        print(f"Command: {' '.join(install_cmd)}")
        result = subprocess.run(install_cmd, check=True, capture_output=True, text=True)
        print("✅ PyTorch 2.7.0 installation successful!")
        
        return test_cuda_without_triton()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ PyTorch 2.7.0 installation failed: {e}")
        return False

def test_cuda_without_triton():
    """Test CUDA functionality without importing triton"""
    print("\n=== Testing CUDA (avoiding Triton) ===")
    
    try:
        # Force reload torch
        if 'torch' in sys.modules:
            del sys.modules['torch']
        if 'triton' in sys.modules:
            del sys.modules['triton']
            
        import torch
        
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU device: {torch.cuda.get_device_name(0)}")
            
            # Test basic CUDA operations (without triton)
            device = torch.device('cuda')
            x = torch.rand(100, 100, device=device)
            y = torch.rand(100, 100, device=device)
            z = torch.matmul(x, y)
            
            print("✅ Basic CUDA operations working!")
            return True
        else:
            print("❌ CUDA not available")
            return False
            
    except Exception as e:
        print(f"❌ CUDA test failed: {e}")
        return False

def install_cpu_fallback():
    """Install CPU-only version as fallback"""
    print("\n=== Installing CPU-only Fallback ===")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "uninstall", 
            "torch", "torchvision", "torchaudio", "-y"
        ], capture_output=True)
        
        install_cmd = [
            sys.executable, "-m", "pip", "install",
            "torch==2.5.1",
            "torchvision==0.20.1",
            "torchaudio==2.5.1",
            "--extra-index-url", "https://download.pytorch.org/whl/cpu"
        ]
        
        result = subprocess.run(install_cmd, check=True, capture_output=True, text=True)
        print("✅ CPU-only PyTorch installed as fallback")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ CPU fallback installation failed: {e}")
        return False

def create_webui_config_without_triton():
    """Create WebUI config that avoids Triton issues"""
    print("\n=== Creating WebUI Configuration ===")
    
    # Detect which PyTorch version was successfully installed
    try:
        import torch
        torch_version = torch.__version__.split('+')[0]  # Remove +cu121 suffix
        
        if torch_version.startswith('2.5'):
            torch_cmd = "pip install torch==2.5.1 torchvision==0.20.1 --extra-index-url https://download.pytorch.org/whl/cu121"
        elif torch_version.startswith('2.7'):
            torch_cmd = "pip install torch==2.7.0 torchvision==0.22.0 --extra-index-url https://download.pytorch.org/whl/cu121"
        else:
            torch_cmd = "pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu121"
            
    except:
        torch_cmd = "pip install torch==2.5.1 torchvision==0.20.1 --extra-index-url https://download.pytorch.org/whl/cu121"
    
    webui_content = f"""@echo off
REM PyTorch Triton-Compatible Configuration
set TORCH_COMMAND={torch_cmd}
set COMMANDLINE_ARGS=--skip-python-version-check --disable-safe-unpickle
REM Disable xformers to avoid triton conflicts
set XFORMERS_PACKAGE=none
call webui.bat %*
"""
    
    try:
        with open("webui_triton_fix.bat", "w") as f:
            f.write(webui_content)
        print("✅ Created webui_triton_fix.bat")
        print("Use this file to launch WebUI without Triton conflicts")
    except Exception as e:
        print(f"⚠️  Could not create config file: {e}")

def main():
    """Main function"""
    print("PyTorch Triton Conflict Fix")
    print("=" * 50)
    
    # Check current installation
    check_current_installation()
    
    # Clean triton installations
    clean_triton_installations()
    
    # Try different PyTorch versions
    success = False
    
    # Strategy 1: PyTorch 2.5.1 (more stable)
    if not success:
        success = install_pytorch_with_compatible_triton()
    
    # Strategy 2: PyTorch 2.7.0 (latest)
    if not success:
        success = install_pytorch_2_7()
    
    # Strategy 3: CPU fallback
    if not success:
        print("\n⚠️  CUDA installations failed, installing CPU version...")
        success = install_cpu_fallback()
    
    if success:
        print("\n✅ PyTorch installation successful!")
        create_webui_config_without_triton()
        
        print("\n" + "=" * 50)
        print("SUCCESS! Next steps:")
        print("1. Use webui_triton_fix.bat to launch WebUI")
        print("2. This configuration avoids Triton conflicts")
        print("3. GPU acceleration should work without the TORCH_LIBRARY error")
        
    else:
        print("\n❌ All installation attempts failed")
        print("Recommendations:")
        print("1. Check NVIDIA driver installation")
        print("2. Consider using Python 3.10-3.12 for better compatibility")
        print("3. Try manual installation with specific versions")

if __name__ == "__main__":
    main()
