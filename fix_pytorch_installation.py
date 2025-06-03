#!/usr/bin/env python3
"""
Fix PyTorch Installation for Python 3.13 + CUDA 12.8 + RTX 3080

This script provides multiple strategies to install PyTorch with CUDA support
when standard installation methods fail.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess
import platform
import os

def check_environment():
    """Check current environment state"""
    print("=== Environment Diagnosis ===")
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    
    # Check pip
    try:
        import pip
        print(f"Pip version: {pip.__version__}")
    except ImportError:
        print("❌ Pip not available")
    
    # Check current PyTorch state
    try:
        import torch
        print(f"⚠️  PyTorch already installed: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        return True
    except ImportError:
        print("❌ PyTorch not installed (expected after failed setup)")
        return False

def clean_pytorch_remnants():
    """Clean any PyTorch installation remnants"""
    print("\n=== Cleaning PyTorch Remnants ===")
    
    packages_to_remove = [
        'torch',
        'torchvision', 
        'torchaudio',
        'torchtext',
        'xformers'
    ]
    
    for package in packages_to_remove:
        try:
            print(f"Removing {package}...")
            subprocess.run([
                sys.executable, '-m', 'pip', 'uninstall', package, '-y'
            ], check=False, capture_output=True)
        except Exception:
            pass
    
    print("✅ Cleanup completed")

def install_pytorch_strategy_1():
    """Strategy 1: PyTorch with CUDA 11.8 (better Python 3.13 support)"""
    print("\n=== Strategy 1: PyTorch CUDA 11.8 ===")
    
    try:
        print("Installing PyTorch with CUDA 11.8 (better Python 3.13 compatibility)...")
        
        # CUDA 11.8 has better Python 3.13 support
        cmd = [
            sys.executable, '-m', 'pip', 'install', 
            'torch', 'torchvision', 'torchaudio',
            '--index-url', 'https://download.pytorch.org/whl/cu118'
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ PyTorch CUDA 11.8 installation successful")
        
        # Test installation
        import torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print("⚠️  CUDA not available, but PyTorch installed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Strategy 1 failed: {e}")
        return False
    except ImportError:
        print("❌ Strategy 1 failed: PyTorch import failed")
        return False

def install_pytorch_strategy_2():
    """Strategy 2: CPU version first, then upgrade to CUDA"""
    print("\n=== Strategy 2: CPU First, Then CUDA ===")
    
    try:
        # Install CPU version first
        print("Installing PyTorch CPU version first...")
        cmd_cpu = [
            sys.executable, '-m', 'pip', 'install',
            'torch', 'torchvision', 'torchaudio'
        ]
        
        subprocess.run(cmd_cpu, check=True, capture_output=True)
        print("✅ CPU PyTorch installed")
        
        # Now upgrade to CUDA
        print("Upgrading to CUDA version...")
        cmd_cuda = [
            sys.executable, '-m', 'pip', 'install',
            'torch', 'torchvision', 'torchaudio',
            '--upgrade', '--index-url', 'https://download.pytorch.org/whl/cu118'
        ]
        
        subprocess.run(cmd_cuda, check=True, capture_output=True)
        print("✅ Upgraded to CUDA PyTorch")
        
        # Test installation
        import torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        
        return torch.cuda.is_available()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Strategy 2 failed: {e}")
        return False
    except ImportError:
        print("❌ Strategy 2 failed: PyTorch import failed")
        return False

def install_pytorch_strategy_3():
    """Strategy 3: Nightly build with CUDA support"""
    print("\n=== Strategy 3: PyTorch Nightly Build ===")
    
    try:
        print("Installing PyTorch nightly build (latest CUDA support)...")
        
        cmd = [
            sys.executable, '-m', 'pip', 'install',
            '--pre', 'torch', 'torchvision', 'torchaudio',
            '--index-url', 'https://download.pytorch.org/whl/nightly/cu121'
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        print("✅ PyTorch nightly installation successful")
        
        # Test installation
        import torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        
        return torch.cuda.is_available()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Strategy 3 failed: {e}")
        return False
    except ImportError:
        print("❌ Strategy 3 failed: PyTorch import failed")
        return False

def install_pytorch_strategy_4():
    """Strategy 4: Manual wheel download and install"""
    print("\n=== Strategy 4: Manual Wheel Installation ===")
    
    try:
        print("Attempting manual wheel installation...")
        
        # Try direct wheel URLs for Python 3.13
        wheel_urls = [
            "https://download.pytorch.org/whl/cu118/torch-2.1.0%2Bcu118-cp311-cp311-win_amd64.whl",
            "https://download.pytorch.org/whl/cu118/torchvision-0.16.0%2Bcu118-cp311-cp311-win_amd64.whl",
            "https://download.pytorch.org/whl/cu118/torchaudio-2.1.0%2Bcu118-cp311-cp311-win_amd64.whl"
        ]
        
        print("⚠️  Manual wheel installation requires specific wheel files")
        print("This strategy requires manual download of compatible wheels")
        print("Skipping automatic implementation")
        
        return False
        
    except Exception as e:
        print(f"❌ Strategy 4 failed: {e}")
        return False

def install_xformers_after_pytorch():
    """Install xFormers after PyTorch is working"""
    print("\n=== Installing xFormers ===")
    
    try:
        # Verify PyTorch is available first
        import torch
        if not torch.cuda.is_available():
            print("⚠️  CUDA not available, skipping xFormers")
            return False
        
        print("Installing xFormers...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 'xformers'
        ], check=True, capture_output=True)
        
        # Test xFormers
        import xformers
        print(f"✅ xFormers installed: {xformers.__version__}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ xFormers installation failed: {e}")
        return False
    except ImportError as e:
        print(f"❌ xFormers import failed: {e}")
        return False

def test_gpu_functionality():
    """Test GPU functionality after installation"""
    print("\n=== GPU Functionality Test ===")
    
    try:
        import torch
        
        if not torch.cuda.is_available():
            print("❌ CUDA not available")
            return False
        
        print(f"✅ CUDA available")
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory // 1024**3}GB")
        
        # Test basic GPU operations
        device = torch.device('cuda')
        test_tensor = torch.randn(100, 100, device=device)
        result = torch.mm(test_tensor, test_tensor)
        
        print("✅ Basic GPU operations working")
        return True
        
    except Exception as e:
        print(f"❌ GPU test failed: {e}")
        return False

def create_recovery_script():
    """Create a recovery script for future use"""
    print("\n=== Creating Recovery Script ===")
    
    recovery_script = '''@echo off
REM PyTorch Recovery Script for Python 3.13 + CUDA
echo PyTorch Recovery for Python 3.13 + RTX 3080
echo =============================================
echo.

echo Cleaning previous installations...
pip uninstall torch torchvision torchaudio xformers -y

echo Installing PyTorch with CUDA 11.8 (Python 3.13 compatible)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo Testing installation...
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"

echo Installing xFormers...
pip install xformers

echo Recovery completed!
pause
'''
    
    try:
        with open('pytorch_recovery.bat', 'w') as f:
            f.write(recovery_script)
        print("✅ Created pytorch_recovery.bat")
        return True
    except Exception as e:
        print(f"❌ Failed to create recovery script: {e}")
        return False

def main():
    """Main recovery function"""
    print("PyTorch Installation Recovery for Python 3.13 + CUDA 12.8")
    print("=" * 60)
    
    # Check current state
    pytorch_exists = check_environment()
    
    if pytorch_exists:
        print("\n⚠️  PyTorch already installed. Checking CUDA availability...")
        try:
            import torch
            if torch.cuda.is_available():
                print("✅ PyTorch with CUDA already working!")
                return
            else:
                print("❌ PyTorch installed but CUDA not available")
        except:
            pass
    
    # Clean any remnants
    clean_pytorch_remnants()
    
    # Try installation strategies in order
    strategies = [
        ("CUDA 11.8 (Recommended for Python 3.13)", install_pytorch_strategy_1),
        ("CPU first, then CUDA upgrade", install_pytorch_strategy_2),
        ("Nightly build with latest CUDA", install_pytorch_strategy_3),
    ]
    
    success = False
    for strategy_name, strategy_func in strategies:
        print(f"\n🔄 Trying: {strategy_name}")
        if strategy_func():
            print(f"✅ Success with: {strategy_name}")
            success = True
            break
        else:
            print(f"❌ Failed: {strategy_name}")
    
    if success:
        # Test GPU functionality
        gpu_working = test_gpu_functionality()
        
        # Install xFormers if GPU is working
        if gpu_working:
            xformers_installed = install_xformers_after_pytorch()
        
        print("\n" + "=" * 60)
        print("PYTORCH RECOVERY SUMMARY")
        print("=" * 60)
        
        if gpu_working:
            print("🎉 PyTorch with CUDA successfully installed!")
            print("\nNext steps:")
            print("1. Run: .\\webui_gpu_rtx3080_balanced.bat")
            print("2. Verify GPU acceleration is working")
            print("3. Test image generation speed")
            
            if xformers_installed:
                print("4. Use maximum performance mode for best speed")
        else:
            print("⚠️  PyTorch installed but GPU acceleration not working")
            print("You can still use CPU mode with improved PyTorch")
    else:
        print("\n❌ All PyTorch installation strategies failed")
        print("\nManual recovery options:")
        print("1. Try: pip install torch torchvision torchaudio")
        print("2. Use CPU-only mode: .\\webui_compatible.bat")
        print("3. Check Python version compatibility")
    
    # Create recovery script
    create_recovery_script()
    
    print(f"\nPython version: {sys.version}")
    print("Recovery script created: pytorch_recovery.bat")

if __name__ == "__main__":
    main()
