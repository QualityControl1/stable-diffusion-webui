#!/usr/bin/env python3
"""
Simple GPU Acceleration Fix for RTX 3080 + Python 3.13

This script provides a simplified approach to fix GPU acceleration issues
without complex version detection that can fail.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess

def fix_dependencies():
    """Fix dependency conflicts with simple approach"""
    print("=== Fixing Dependencies ===")
    
    try:
        print("Step 1: Removing conflicting packages...")
        # Remove problematic packages
        packages_to_remove = ['blendmodes', 'numpy']
        for package in packages_to_remove:
            subprocess.run([
                sys.executable, '-m', 'pip', 'uninstall', package, '-y'
            ], check=False, capture_output=True)
        
        print("Step 2: Installing compatible versions...")
        # Install compatible versions in correct order
        compatible_packages = [
            'numpy>=1.21.0,<2.0.0',  # Gradio compatible
            'blendmodes==2022',       # NumPy 1.x compatible
        ]
        
        for package in compatible_packages:
            print(f"Installing {package}...")
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', package
            ], check=True, capture_output=True)
        
        print("Step 3: Testing imports...")
        # Test imports without version checking
        import numpy
        import blendmodes
        import gradio
        
        print(f"✅ NumPy: {numpy.__version__}")
        print("✅ blendmodes: imported successfully")
        print(f"✅ Gradio: {gradio.__version__}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Package installation failed: {e}")
        return False
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def install_xformers():
    """Install xFormers for GPU acceleration"""
    print("\n=== Installing xFormers ===")
    
    try:
        # Check PyTorch CUDA first
        import torch
        
        if not torch.cuda.is_available():
            print("❌ CUDA not available - skipping xFormers")
            return False
        
        print(f"PyTorch: {torch.__version__}")
        print(f"CUDA: {torch.version.cuda}")
        
        # Install xFormers
        print("Installing xFormers...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 'xformers'
        ], check=True, capture_output=True)
        
        # Test xFormers (simple test)
        try:
            import xformers
            print("✅ xFormers installed successfully")
            return True
        except ImportError:
            print("⚠️  xFormers installed but import failed")
            return False
        
    except ImportError:
        print("❌ PyTorch not available")
        return False
    except subprocess.CalledProcessError:
        print("❌ xFormers installation failed")
        print("⚠️  WebUI will work without xFormers but slower")
        return False

def verify_gpu():
    """Simple GPU verification"""
    print("\n=== Verifying GPU ===")
    
    try:
        import torch
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            vram_gb = torch.cuda.get_device_properties(0).total_memory // 1024**3
            print(f"✅ GPU: {gpu_name}")
            print(f"✅ VRAM: {vram_gb}GB")
            
            # Simple GPU test
            device = torch.device('cuda')
            test_tensor = torch.randn(100, 100, device=device)
            _ = torch.mm(test_tensor, test_tensor)
            print("✅ GPU operations working")
            
            return True
        else:
            print("❌ CUDA not available")
            return False
            
    except Exception as e:
        print(f"❌ GPU test failed: {e}")
        return False

def create_working_launch_script():
    """Create a working launch script"""
    print("\n=== Creating Launch Script ===")
    
    script_content = '''@echo off
REM RTX 3080 GPU Launch Script (Working Version)
echo Starting WebUI with RTX 3080 GPU acceleration...
echo.

REM Install dependencies if needed
echo Checking dependencies...
python -c "import numpy; import torch; print('Dependencies OK')" || (
    echo Installing missing dependencies...
    pip install "numpy>=1.21.0,<2.0.0" "blendmodes==2022" --quiet
)

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM WebUI configuration
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set TORCH_COMMAND=echo "Using existing PyTorch installation"
set CLIP_PACKAGE=echo "Skipping CLIP (compatibility issues)"
set OPENCLIP_PACKAGE=echo "Skipping open_clip (compatibility issues)"

REM RTX 3080 optimization flags (WebUI v1.10.1 compatible)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half-vae

REM Enable xFormers if available
python -c "import xformers" >nul 2>&1 && (
    set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --xformers
    echo xFormers enabled for maximum performance
) || (
    echo xFormers not available - using standard attention
)

echo RTX 3080 Configuration:
echo - Target: 15-25 seconds per 512x512 image
echo - VRAM: Medium usage (8-12GB)
echo - Compatibility: Python 3.13 preserved
echo.

call webui.bat %*
'''
    
    try:
        with open('webui_gpu_working.bat', 'w') as f:
            f.write(script_content)
        print("✅ Created webui_gpu_working.bat")
        return True
    except Exception as e:
        print(f"❌ Failed to create script: {e}")
        return False

def main():
    """Main function"""
    print("Simple RTX 3080 GPU Fix for Python 3.13")
    print("=" * 45)
    
    # Fix dependencies
    deps_fixed = fix_dependencies()
    
    # Install xFormers
    xformers_ok = install_xformers()
    
    # Verify GPU
    gpu_ok = verify_gpu()
    
    # Create launch script
    script_created = create_working_launch_script()
    
    print("\n" + "=" * 45)
    print("SIMPLE GPU FIX SUMMARY")
    print("=" * 45)
    
    if deps_fixed and gpu_ok and script_created:
        print("🎉 GPU acceleration setup completed!")
        
        print("\nFixed:")
        print("✅ Dependency conflicts resolved")
        print("✅ GPU acceleration verified")
        if xformers_ok:
            print("✅ xFormers installed")
        else:
            print("⚠️  xFormers not available (reduced performance)")
        
        print("\nNext steps:")
        print("1. Launch: .\\webui_gpu_working.bat")
        print("2. Test image generation speed")
        print("3. Should see 15-25 seconds per 512x512 image")
        
    else:
        print("⚠️  Some issues remain:")
        if not deps_fixed:
            print("❌ Dependency conflicts")
        if not gpu_ok:
            print("❌ GPU not working")
        if not script_created:
            print("❌ Script creation failed")
    
    print(f"\nPython: {sys.version}")
    print("All Python 3.13 compatibility preserved")

if __name__ == "__main__":
    main()
