#!/usr/bin/env python3
"""
PyTorch CUDA Fix for Python 3.13

This script specifically fixes the CUDA installation issue by replacing
the CPU-only PyTorch with the CUDA-enabled version.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess
import os

def check_current_pytorch():
    """Check current PyTorch installation"""
    try:
        import torch
        print(f"Current PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU device: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  CPU-only version detected")
        return True
    except ImportError:
        print("PyTorch is not installed")
        return False

def uninstall_current_pytorch():
    """Uninstall current PyTorch installation"""
    print("\n=== Uninstalling Current PyTorch ===")
    
    packages_to_remove = ["torch", "torchvision", "torchaudio"]
    
    for package in packages_to_remove:
        try:
            print(f"Uninstalling {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "uninstall", package, "-y"
            ], check=True, capture_output=True, text=True)
            print(f"✅ {package} uninstalled")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  {package} not found or already uninstalled")

def install_cuda_pytorch():
    """Install CUDA-enabled PyTorch for Python 3.13"""
    print("\n=== Installing CUDA-enabled PyTorch 2.6.0 ===")
    
    # Try different CUDA versions in order of preference
    cuda_configs = [
        {
            "version": "cu121",
            "url": "https://download.pytorch.org/whl/cu121",
            "description": "CUDA 12.1 (matches your system)"
        },
        {
            "version": "cu118", 
            "url": "https://download.pytorch.org/whl/cu118",
            "description": "CUDA 11.8 (fallback)"
        },
        {
            "version": "cu124",
            "url": "https://download.pytorch.org/whl/cu124", 
            "description": "CUDA 12.4 (newer)"
        }
    ]
    
    for config in cuda_configs:
        print(f"\n🔄 Trying {config['description']}...")
        
        install_command = [
            sys.executable, "-m", "pip", "install",
            "torch==2.6.0",
            "torchvision==0.21.0", 
            "torchaudio==2.6.0",
            "--extra-index-url", config["url"],
            "--force-reinstall"
        ]
        
        print(f"Command: {' '.join(install_command)}")
        
        try:
            result = subprocess.run(install_command, check=True, capture_output=True, text=True)
            print(f"✅ Installation successful!")
            
            # Verify CUDA works
            if verify_cuda():
                print(f"✅ CUDA verification successful with {config['version'].upper()}!")
                return True
            else:
                print(f"⚠️  CUDA not working with {config['version'].upper()}, trying next...")
                continue
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed with {config['version'].upper()}")
            print(f"Error: {e.stderr if e.stderr else str(e)}")
            continue
    
    return False

def verify_cuda():
    """Verify CUDA installation works"""
    try:
        # Force reload torch module
        if 'torch' in sys.modules:
            del sys.modules['torch']
        
        import torch
        
        if torch.cuda.is_available():
            # Test basic CUDA operations
            device = torch.device('cuda')
            x = torch.rand(5, 3, device=device)
            y = torch.rand(5, 3, device=device)
            z = x + y
            return True
        else:
            return False
    except Exception as e:
        print(f"CUDA verification error: {e}")
        return False

def test_installation():
    """Test the final installation"""
    print("\n=== Testing Final Installation ===")
    
    try:
        # Force reload torch
        if 'torch' in sys.modules:
            del sys.modules['torch']
            
        import torch
        
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"✅ Python version: {sys.version}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA is available!")
            print(f"✅ CUDA version: {torch.version.cuda}")
            print(f"✅ GPU device: {torch.cuda.get_device_name(0)}")
            print(f"✅ GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            
            # Test GPU tensor operations
            device = torch.device('cuda')
            x = torch.rand(1000, 1000, device=device)
            y = torch.rand(1000, 1000, device=device)
            z = torch.matmul(x, y)
            print(f"✅ GPU tensor operations working!")
            
        else:
            print("❌ CUDA is not available")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def update_webui_config():
    """Update webui environment configuration"""
    print("\n=== Updating WebUI Configuration ===")
    
    # Update the webui_env.bat file
    webui_content = f"""@echo off
set TORCH_COMMAND=pip install torch==2.6.0 torchvision==0.21.0 --extra-index-url https://download.pytorch.org/whl/cu121
set COMMANDLINE_ARGS=--skip-python-version-check
call webui.bat %*
"""
    
    try:
        with open("webui_env.bat", "w") as f:
            f.write(webui_content)
        print("✅ Updated webui_env.bat with CUDA configuration")
    except Exception as e:
        print(f"⚠️  Could not update webui_env.bat: {e}")

def main():
    """Main function"""
    print("PyTorch CUDA Fix for Python 3.13")
    print("=" * 50)
    
    # Check current installation
    print("Checking current PyTorch installation...")
    pytorch_installed = check_current_pytorch()
    
    if not pytorch_installed:
        print("❌ PyTorch not found. Please run the main fix script first.")
        return
    
    # Check if CUDA is already working
    try:
        import torch
        if torch.cuda.is_available():
            print("✅ CUDA is already working! No fix needed.")
            test_installation()
            return
    except:
        pass
    
    print("\n🔧 CUDA not available. Starting fix process...")
    
    # Uninstall current version
    uninstall_current_pytorch()
    
    # Install CUDA version
    success = install_cuda_pytorch()
    
    if success:
        print("\n✅ CUDA PyTorch installation completed!")
        
        # Test the installation
        if test_installation():
            print("\n🎉 Success! PyTorch with CUDA is now working!")
        else:
            print("\n❌ Installation completed but CUDA test failed")
            
        # Update webui config
        update_webui_config()
        
    else:
        print("\n❌ CUDA installation failed")
        print("Possible solutions:")
        print("1. Check that NVIDIA drivers are properly installed")
        print("2. Verify CUDA 12.1 is installed on your system")
        print("3. Try running: nvidia-smi to check GPU status")
        print("4. Consider using CPU-only mode as fallback")
    
    print("\n" + "=" * 50)
    print("Next steps:")
    print("1. Test with: python -c \"import torch; print(torch.cuda.is_available())\"")
    print("2. Launch webui with: webui_env.bat")
    print("3. Check GPU usage in Task Manager during generation")

if __name__ == "__main__":
    main()
