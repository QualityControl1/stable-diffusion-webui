#!/usr/bin/env python3
"""
Comprehensive PyTorch Fix for Python 3.13 Triton Issues

This script provides multiple approaches to resolve the persistent
TORCH_LIBRARY triton namespace conflict on Python 3.13.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess
import os
import shutil

def diagnose_environment():
    """Comprehensive environment diagnosis"""
    print("=== Environment Diagnosis ===")
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {sys.platform}")
    
    # Check for virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Running in system Python")
    
    # Check pip version
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"Pip version: {result.stdout.strip()}")
    except:
        print("❌ Pip not available")
    
    # Check CUDA drivers
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True, check=True)
        print("✅ NVIDIA drivers working")
    except:
        print("⚠️  NVIDIA drivers not accessible")

def complete_pytorch_cleanup():
    """Complete cleanup of all PyTorch and related packages"""
    print("\n=== Complete PyTorch Cleanup ===")
    
    packages_to_remove = [
        "torch", "torchvision", "torchaudio",
        "triton", "pytorch-triton", "pytorch-triton-rocm", "triton-nightly",
        "xformers", "transformers", "accelerate",
        "nvidia-ml-py", "nvidia-ml-py3"
    ]
    
    for package in packages_to_remove:
        try:
            print(f"Removing {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "uninstall", package, "-y"
            ], capture_output=True, check=True)
            print(f"✅ {package} removed")
        except:
            print(f"⚠️  {package} not found")
    
    # Clear pip cache
    try:
        subprocess.run([sys.executable, "-m", "pip", "cache", "purge"], 
                      capture_output=True, check=True)
        print("✅ Pip cache cleared")
    except:
        print("⚠️  Could not clear pip cache")

def try_pytorch_cpu_only():
    """Install CPU-only PyTorch to test basic functionality"""
    print("\n=== Installing CPU-only PyTorch ===")
    
    try:
        install_cmd = [
            sys.executable, "-m", "pip", "install",
            "torch==2.7.0", "torchvision==0.22.0", "torchaudio==2.7.0",
            "--index-url", "https://download.pytorch.org/whl/cpu"
        ]
        
        print(f"Command: {' '.join(install_cmd)}")
        result = subprocess.run(install_cmd, check=True, capture_output=True, text=True)
        print("✅ CPU-only PyTorch installed")
        
        # Test basic functionality
        return test_pytorch_basic()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ CPU-only installation failed: {e}")
        return False

def test_pytorch_basic():
    """Test basic PyTorch functionality without CUDA"""
    print("\n=== Testing Basic PyTorch ===")
    
    try:
        # Force reload
        for module in ['torch', 'triton']:
            if module in sys.modules:
                del sys.modules[module]
        
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        
        # Test basic tensor operations
        x = torch.rand(5, 3)
        y = torch.rand(5, 3)
        z = x + y
        print("✅ Basic tensor operations working")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic PyTorch test failed: {e}")
        return False

def try_pytorch_with_conda():
    """Try installing PyTorch using conda (if available)"""
    print("\n=== Trying Conda Installation ===")
    
    # Check if conda is available
    try:
        result = subprocess.run(["conda", "--version"], capture_output=True, text=True, check=True)
        print(f"Conda available: {result.stdout.strip()}")
    except:
        print("❌ Conda not available, skipping conda installation")
        return False
    
    try:
        # Install PyTorch via conda
        install_cmd = [
            "conda", "install", "pytorch", "torchvision", "torchaudio", 
            "pytorch-cuda=12.1", "-c", "pytorch", "-c", "nvidia", "-y"
        ]
        
        print(f"Command: {' '.join(install_cmd)}")
        result = subprocess.run(install_cmd, check=True, capture_output=True, text=True)
        print("✅ Conda PyTorch installation successful")
        
        return test_pytorch_basic()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Conda installation failed: {e}")
        return False

def create_webui_configs():
    """Create multiple WebUI configuration files"""
    print("\n=== Creating WebUI Configurations ===")
    
    # Configuration 1: CPU-only mode
    cpu_config = """@echo off
REM CPU-only configuration for Python 3.13
set TORCH_COMMAND=pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cpu
set COMMANDLINE_ARGS=--skip-python-version-check --skip-torch-cuda-test --precision full --no-half
set XFORMERS_PACKAGE=none
call webui.bat %*
"""
    
    # Configuration 2: CUDA with workarounds
    cuda_config = """@echo off
REM CUDA configuration with triton workarounds
set TORCH_COMMAND=pip install torch==2.7.0 torchvision==0.22.0 --extra-index-url https://download.pytorch.org/whl/cu121
set COMMANDLINE_ARGS=--skip-python-version-check --disable-safe-unpickle --no-half-vae
set XFORMERS_PACKAGE=none
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
call webui.bat %*
"""
    
    # Configuration 3: Python 3.10 recommendation
    python310_config = """@echo off
REM Recommended: Use Python 3.10 for best compatibility
echo.
echo RECOMMENDATION: For best compatibility with Stable Diffusion WebUI,
echo consider using Python 3.10 instead of Python 3.13.
echo.
echo Download Python 3.10.11 from:
echo https://www.python.org/downloads/release/python-31011/
echo.
echo Then create a virtual environment:
echo C:\\Python310\\python.exe -m venv venv_py310
echo venv_py310\\Scripts\\activate
echo.
pause
"""
    
    configs = [
        ("webui_cpu_only.bat", cpu_config),
        ("webui_cuda_workaround.bat", cuda_config),
        ("python310_recommendation.bat", python310_config)
    ]
    
    for filename, content in configs:
        try:
            with open(filename, "w") as f:
                f.write(content)
            print(f"✅ Created {filename}")
        except Exception as e:
            print(f"❌ Could not create {filename}: {e}")

def check_python_compatibility():
    """Check if Python 3.13 is fundamentally compatible"""
    print("\n=== Python 3.13 Compatibility Check ===")
    
    # Test C extension loading
    try:
        import ctypes
        print("✅ ctypes working")
    except:
        print("❌ ctypes not working")
    
    # Test multiprocessing
    try:
        import multiprocessing
        print("✅ multiprocessing working")
    except:
        print("❌ multiprocessing not working")
    
    # Check for known Python 3.13 issues
    if sys.version_info >= (3, 13):
        print("⚠️  Python 3.13 detected")
        print("Known issues with AI libraries:")
        print("- Triton C++ extensions may not be compatible")
        print("- Some CUDA libraries have limited support")
        print("- Recommendation: Use Python 3.10-3.12 for AI workloads")

def main():
    """Main function with multiple solution attempts"""
    print("Comprehensive PyTorch Fix for Python 3.13")
    print("=" * 60)
    
    # Diagnose environment
    diagnose_environment()
    check_python_compatibility()
    
    # Complete cleanup
    complete_pytorch_cleanup()
    
    # Try different installation methods
    success = False
    
    print("\n" + "=" * 60)
    print("ATTEMPTING MULTIPLE SOLUTIONS")
    print("=" * 60)
    
    # Method 1: CPU-only PyTorch
    if not success:
        print("\n🔄 Method 1: CPU-only PyTorch")
        success = try_pytorch_cpu_only()
        if success:
            print("✅ CPU-only PyTorch working - WebUI will run without GPU")
    
    # Method 2: Conda installation
    if not success:
        print("\n🔄 Method 2: Conda PyTorch")
        success = try_pytorch_with_conda()
    
    # Create configuration files regardless
    create_webui_configs()
    
    # Final recommendations
    print("\n" + "=" * 60)
    print("FINAL RECOMMENDATIONS")
    print("=" * 60)
    
    if success:
        print("✅ PyTorch is working (at least CPU mode)")
        print("\nNext steps:")
        print("1. Try webui_cpu_only.bat for guaranteed compatibility")
        print("2. Try webui_cuda_workaround.bat for GPU (may have issues)")
        print("3. Monitor for TORCH_LIBRARY errors")
    else:
        print("❌ PyTorch installation failed on Python 3.13")
        print("\nSTRONG RECOMMENDATION:")
        print("Use Python 3.10-3.12 for Stable Diffusion WebUI")
        print("\nSteps:")
        print("1. Download Python 3.10.11")
        print("2. Create new virtual environment")
        print("3. Install WebUI in Python 3.10 environment")
        print("4. Run python310_recommendation.bat for detailed steps")
    
    print(f"\nPython version: {sys.version}")
    print("For AI/ML workloads, Python 3.10-3.12 is recommended over 3.13")

if __name__ == "__main__":
    main()
