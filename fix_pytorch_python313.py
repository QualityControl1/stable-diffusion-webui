#!/usr/bin/env python3
"""
PyTorch Python 3.13 Compatibility Fix for Stable Diffusion WebUI

This script provides multiple solutions to fix PyTorch installation issues
when using Python 3.13 with the Stable Diffusion WebUI.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check current Python version"""
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    return version

def check_pytorch_availability():
    """Check if PyTorch is available for current Python version"""
    try:
        import torch
        print(f"PyTorch is already installed: {torch.__version__}")
        return True
    except ImportError:
        print("PyTorch is not installed")
        return False

def solution_1_install_compatible_pytorch():
    """Solution 1: Install PyTorch version compatible with Python 3.13"""
    print("\n=== Solution 1: Installing Compatible PyTorch with CUDA ===")

    python_version = sys.version_info

    if python_version.minor >= 13:
        # For Python 3.13+, use PyTorch 2.6.0 or newer (available versions)
        torch_version = "2.6.0"
        torchvision_version = "0.21.0"
        torchaudio_version = "2.6.0"
    else:
        # For older Python versions
        torch_version = "2.1.2"
        torchvision_version = "0.16.2"
        torchaudio_version = "2.1.2"

    # Try multiple CUDA versions in order of preference
    cuda_versions = ["cu121", "cu118", "cu124"]  # CUDA 12.1, 11.8, 12.4

    for cuda_version in cuda_versions:
        print(f"\nTrying CUDA version: {cuda_version}")

        install_command = [
            sys.executable, "-m", "pip", "install", "--force-reinstall",
            f"torch=={torch_version}",
            f"torchvision=={torchvision_version}",
            f"torchaudio=={torchaudio_version}",
            "--extra-index-url", f"https://download.pytorch.org/whl/{cuda_version}"
        ]

        print(f"Installing PyTorch {torch_version} with {cuda_version.upper()}")
        print(f"Command: {' '.join(install_command)}")

        try:
            result = subprocess.run(install_command, check=True, capture_output=True, text=True)
            print(f"✅ PyTorch with {cuda_version.upper()} installation successful!")

            # Verify CUDA is actually available
            if verify_cuda_installation():
                print(f"✅ CUDA verification successful!")
                return True
            else:
                print(f"⚠️  CUDA not detected, trying next version...")
                continue

        except subprocess.CalledProcessError as e:
            print(f"❌ PyTorch with {cuda_version.upper()} installation failed")
            print(f"Error: {e}")
            continue

    print("❌ All CUDA installations failed")
    return False

def verify_cuda_installation():
    """Verify that CUDA is properly installed and available"""
    try:
        import torch
        return torch.cuda.is_available()
    except Exception:
        return False

def solution_2_use_nightly_build():
    """Solution 2: Use PyTorch nightly build for Python 3.13"""
    print("\n=== Solution 2: Installing PyTorch Nightly Build ===")
    
    install_command = [
        sys.executable, "-m", "pip", "install",
        "--pre", "torch", "torchvision", "torchaudio",
        "--extra-index-url", "https://download.pytorch.org/whl/nightly/cu121"
    ]
    
    print("Installing PyTorch nightly build...")
    print(f"Command: {' '.join(install_command)}")
    
    try:
        result = subprocess.run(install_command, check=True, capture_output=True, text=True)
        print("✅ PyTorch nightly installation successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyTorch nightly installation failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def solution_3_cpu_only():
    """Solution 3: Install CPU-only PyTorch (fallback)"""
    print("\n=== Solution 3: Installing CPU-only PyTorch ===")
    
    python_version = sys.version_info
    
    if python_version.minor >= 13:
        torch_version = "2.6.0"
        torchvision_version = "0.21.0"
        torchaudio_version = "2.6.0"
    else:
        torch_version = "2.1.2"
        torchvision_version = "0.16.2"
        torchaudio_version = "2.1.2"
    
    install_command = [
        sys.executable, "-m", "pip", "install",
        f"torch=={torch_version}",
        f"torchvision=={torchvision_version}",
        f"torchaudio=={torchaudio_version}",
        "--extra-index-url", "https://download.pytorch.org/whl/cpu"
    ]
    
    print("Installing CPU-only PyTorch...")
    print(f"Command: {' '.join(install_command)}")
    
    try:
        result = subprocess.run(install_command, check=True, capture_output=True, text=True)
        print("✅ CPU-only PyTorch installation successful!")
        print("⚠️  Note: This will use CPU only, no GPU acceleration")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ CPU-only PyTorch installation failed: {e}")
        return False

def create_environment_override():
    """Create environment variable override for WebUI"""
    print("\n=== Creating Environment Override ===")
    
    python_version = sys.version_info
    
    if python_version.minor >= 13:
        torch_version = "2.6.0"
        torchvision_version = "0.21.0"
    else:
        torch_version = "2.1.2"
        torchvision_version = "0.16.2"
    
    torch_command = f"pip install torch=={torch_version} torchvision=={torchvision_version} --extra-index-url https://download.pytorch.org/whl/cu121"
    
    # Create a batch file for Windows
    if platform.system() == "Windows":
        with open("webui_env.bat", "w") as f:
            f.write(f'@echo off\n')
            f.write(f'set TORCH_COMMAND={torch_command}\n')
            f.write(f'set COMMANDLINE_ARGS=--skip-python-version-check\n')
            f.write(f'call webui.bat %*\n')
        
        print("✅ Created webui_env.bat with environment overrides")
        print("Use 'webui_env.bat' instead of 'webui.bat' to launch")
    else:
        with open("webui_env.sh", "w") as f:
            f.write(f'#!/bin/bash\n')
            f.write(f'export TORCH_COMMAND="{torch_command}"\n')
            f.write(f'export COMMANDLINE_ARGS="--skip-python-version-check"\n')
            f.write(f'./webui.sh "$@"\n')
        
        os.chmod("webui_env.sh", 0o755)
        print("✅ Created webui_env.sh with environment overrides")
        print("Use './webui_env.sh' instead of './webui.sh' to launch")

def test_pytorch_installation():
    """Test if PyTorch installation works"""
    print("\n=== Testing PyTorch Installation ===")
    
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"✅ Python version: {sys.version}")
        
        # Test basic tensor operations
        x = torch.rand(5, 3)
        print(f"✅ Basic tensor creation works: {x.shape}")
        
        # Test CUDA availability
        if torch.cuda.is_available():
            print(f"✅ CUDA is available: {torch.cuda.get_device_name(0)}")
            print(f"✅ CUDA version: {torch.version.cuda}")
        else:
            print("⚠️  CUDA is not available (CPU-only mode)")
        
        return True
    except Exception as e:
        print(f"❌ PyTorch test failed: {e}")
        return False

def main():
    """Main function to run the fix"""
    print("PyTorch Python 3.13 Compatibility Fix")
    print("=" * 50)
    
    # Check current setup
    python_version = check_python_version()
    pytorch_available = check_pytorch_availability()
    
    if python_version.minor < 13:
        print("✅ Python version is compatible with standard PyTorch")
        if not pytorch_available:
            print("Installing standard PyTorch...")
            solution_1_install_compatible_pytorch()
    else:
        print("⚠️  Python 3.13 detected - need compatible PyTorch version")
        
        # Try solutions in order
        success = False
        
        if not success:
            print("\nTrying Solution 1: Compatible PyTorch version...")
            success = solution_1_install_compatible_pytorch()
        
        if not success:
            print("\nTrying Solution 2: PyTorch nightly build...")
            success = solution_2_use_nightly_build()
        
        if not success:
            print("\nTrying Solution 3: CPU-only PyTorch...")
            success = solution_3_cpu_only()
        
        if success:
            print("\n✅ PyTorch installation completed!")
        else:
            print("\n❌ All PyTorch installation attempts failed")
            print("Consider downgrading to Python 3.10-3.12")
    
    # Create environment override regardless
    create_environment_override()
    
    # Test the installation
    test_pytorch_installation()
    
    print("\n" + "=" * 50)
    print("Fix completed! Next steps:")
    print("1. Use the created environment script to launch WebUI")
    print("2. If issues persist, consider using Python 3.10-3.12")
    print("3. Check the WebUI documentation for additional troubleshooting")

if __name__ == "__main__":
    main()
