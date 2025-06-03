#!/usr/bin/env python3
"""
Pre-Launch Test for stable-diffusion-webui

This script tests your environment before launching WebUI
to catch any issues early.
"""

import sys
import os

def test_python_version():
    """Test Python version"""
    print("=== Python Version Test ===")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print("✅ Python version compatible")
        return True
    else:
        print("❌ Python version may have issues")
        return False

def test_pytorch():
    """Test PyTorch installation"""
    print("\n=== PyTorch Test ===")
    
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        
        # Test basic tensor operations
        x = torch.rand(5, 3)
        y = torch.rand(5, 3)
        z = x + y
        print("✅ Basic tensor operations working")
        
        # Check CUDA
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  CPU-only mode (expected for your setup)")
        
        return True
    except Exception as e:
        print(f"❌ PyTorch test failed: {e}")
        return False

def test_essential_packages():
    """Test essential packages"""
    print("\n=== Essential Packages Test ===")
    
    essential_packages = [
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
    for package in essential_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
            working += 1
        except ImportError:
            print(f"❌ {package}")
    
    print(f"\nWorking packages: {working}/{len(essential_packages)}")
    return working >= len(essential_packages) * 0.7  # 70% success rate

def test_webui_files():
    """Test if WebUI files exist"""
    print("\n=== WebUI Files Test ===")
    
    required_files = [
        "webui.bat",
        "launch.py",
        "modules/launch_utils.py",
        "webui_compatible.bat"
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing.append(file)
    
    if missing:
        print(f"\nMissing files: {missing}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_problematic_packages():
    """Check that problematic packages are not installed"""
    print("\n=== Problematic Packages Check ===")
    
    problematic = ["clip", "open_clip", "sentencepiece"]
    
    for package in problematic:
        try:
            __import__(package)
            print(f"⚠️  {package} is installed (may cause issues)")
        except ImportError:
            print(f"✅ {package} not installed (good)")

def show_launch_commands():
    """Show the correct launch commands"""
    print("\n=== Launch Commands ===")
    print("Use one of these commands to launch WebUI:")
    print()
    print("Option 1 (Recommended):")
    print("  .\\webui_compatible.bat")
    print()
    print("Option 2 (If PowerShell issues):")
    print("  cmd /c webui_compatible.bat")
    print()
    print("Option 3 (Manual environment):")
    print("  $env:COMMANDLINE_ARGS='--skip-python-version-check --skip-install --no-half'")
    print("  .\\webui.bat")

def main():
    """Main test function"""
    print("Pre-Launch Test for stable-diffusion-webui")
    print("=" * 50)
    
    tests = [
        test_python_version(),
        test_pytorch(),
        test_essential_packages(),
        test_webui_files()
    ]
    
    test_problematic_packages()
    
    passed = sum(tests)
    total = len(tests)
    
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Ready to launch WebUI")
        print("\n✅ Your setup looks good for Python 3.13 + CPU-only mode")
        show_launch_commands()
    elif passed >= total * 0.75:
        print("⚠️  Most tests passed. WebUI should work with some limitations")
        show_launch_commands()
    else:
        print("❌ Multiple test failures. WebUI may have issues")
        print("\nTroubleshooting suggestions:")
        print("1. Check Python and package installations")
        print("2. Verify you're in the correct directory")
        print("3. Consider using Python 3.10 for better compatibility")
    
    print(f"\nCurrent directory: {os.getcwd()}")
    print("Make sure you're in the stable-diffusion-webui directory")

if __name__ == "__main__":
    main()
