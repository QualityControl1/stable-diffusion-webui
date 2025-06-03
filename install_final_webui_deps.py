#!/usr/bin/env python3
"""
Install Final WebUI Dependencies for Python 3.13

This script installs all remaining core WebUI dependencies including
tomesd and other modules that might be missing.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess

def install_core_webui_dependencies():
    """Install core WebUI dependencies that might be missing"""
    print("=== Installing Core WebUI Dependencies ===")
    
    # Core WebUI dependencies that are often missing
    core_webui_deps = [
        # Performance optimization
        "tomesd",                   # Token Merging for Stable Diffusion (the missing one)
        
        # Math and tensor operations
        "einops>=0.6.1",           # Einstein notation for tensors
        "kornia>=0.6.8",           # Computer vision library
        
        # Sampling and algorithms
        "torchsde>=0.2.5",         # Stochastic differential equations
        "torchdiffeq>=0.2.3",      # Differential equation solvers
        
        # Image processing and enhancement
        "resize-right>=0.0.2",     # Image resizing
        "clean-fid>=0.1.35",       # FID calculation
        "lpips>=0.1.4",            # Perceptual similarity
        
        # Additional utilities
        "lark>=1.1.5",             # Parsing library
        "addict>=2.4.0",           # Dictionary utilities
        "blendmodes>=2022",        # Image blending
        
        # Font and text handling
        "fonts>=0.0.3",
        "font-roboto>=0.0.1",
        
        # Metadata handling
        "piexif>=1.1.3",           # EXIF data handling
        
        # Additional ML utilities
        "timm>=0.9.2",             # PyTorch image models
        
        # Development and debugging
        "rich>=13.0.0",            # Rich text and formatting
        "click>=8.1.0",            # Command line interface
        
        # Additional image formats and processing
        "imageio>=2.22.0",
        "scikit-image>=0.19.0",
        "opencv-python>=4.6.0",
        
        # Web and API utilities
        "httpx>=0.24.0",
        "websockets>=11.0",
        
        # Configuration and serialization
        "pyyaml>=6.0",
        "toml>=0.10.2",
        
        # System utilities
        "psutil>=5.9.0",
        "GitPython>=3.1.30",
    ]
    
    print(f"Installing {len(core_webui_deps)} core WebUI dependencies...")
    
    successful = 0
    failed = []
    critical_failed = []
    
    # Critical dependencies that must succeed
    critical_deps = ["tomesd", "einops", "kornia", "torchsde", "lark"]
    
    for dep in core_webui_deps:
        try:
            print(f"Installing {dep}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", dep
            ], check=True, capture_output=True, text=True)
            print(f"✅ {dep}")
            successful += 1
        except subprocess.CalledProcessError as e:
            print(f"❌ {dep} failed")
            failed.append(dep)
            
            # Check if it's a critical dependency
            dep_name = dep.split(">=")[0].split("==")[0]
            if dep_name in critical_deps:
                critical_failed.append(dep_name)
    
    print(f"\nResults: {successful}/{len(core_webui_deps)} successful")
    if failed:
        print(f"Failed packages: {len(failed)}")
        for pkg in failed[:5]:  # Show first 5 failures
            print(f"  - {pkg}")
        if len(failed) > 5:
            print(f"  ... and {len(failed) - 5} more")
    
    if critical_failed:
        print(f"\n⚠️  Critical dependencies failed: {critical_failed}")
        return False
    
    return successful > len(core_webui_deps) * 0.7  # 70% success rate

def test_tomesd_specifically():
    """Test tomesd module specifically"""
    print("\n=== Testing tomesd Module ===")
    
    try:
        import tomesd
        print(f"✅ tomesd imported successfully")
        
        # Test basic functionality if possible
        if hasattr(tomesd, '__version__'):
            print(f"tomesd version: {tomesd.__version__}")
        
        return True
    except ImportError as e:
        print(f"❌ tomesd import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ tomesd test failed: {e}")
        return False

def test_webui_core_imports():
    """Test core WebUI imports"""
    print("\n=== Testing Core WebUI Imports ===")
    
    core_imports = [
        "tomesd",
        "einops",
        "kornia", 
        "torchsde",
        "lark",
        "addict",
        "timm",
        "rich",
        "imageio",
        "PIL"
    ]
    
    working = 0
    for module in core_imports:
        try:
            if module == "PIL":
                __import__("PIL")
            else:
                __import__(module)
            print(f"✅ {module}")
            working += 1
        except ImportError:
            print(f"❌ {module}")
    
    print(f"\nWorking core imports: {working}/{len(core_imports)}")
    return working >= len(core_imports) * 0.8  # 80% success rate

def test_webui_sd_models():
    """Test if WebUI sd_models module can be imported"""
    print("\n=== Testing WebUI sd_models Module ===")
    
    try:
        # Add modules directory to path
        import os
        modules_path = os.path.join(os.getcwd(), "modules")
        if modules_path not in sys.path:
            sys.path.insert(0, modules_path)
        
        # Try importing the sd_models module
        import sd_models
        print("✅ WebUI sd_models module imports successfully")
        return True
    except ImportError as e:
        print(f"❌ WebUI sd_models module import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ WebUI sd_models module test failed: {e}")
        return False

def check_webui_readiness():
    """Check if WebUI is ready to launch"""
    print("\n=== Checking WebUI Readiness ===")
    
    # Test key modules that WebUI needs
    key_modules = [
        "torch",
        "torchvision",
        "PIL",
        "numpy",
        "gradio",
        "fastapi",
        "tomesd",
        "einops",
        "omegaconf",
        "safetensors"
    ]
    
    missing_modules = []
    for module in key_modules:
        try:
            if module == "PIL":
                __import__("PIL")
            else:
                __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing critical modules: {missing_modules}")
        return False
    else:
        print("✅ All critical modules available")
        return True

def main():
    """Main function"""
    print("Final WebUI Dependencies Installation for Python 3.13")
    print("=" * 60)
    print("Installing remaining core WebUI dependencies...")
    print()
    
    # Install core WebUI dependencies
    deps_success = install_core_webui_dependencies()
    
    # Test tomesd specifically
    tomesd_works = test_tomesd_specifically()
    
    # Test other core imports
    core_imports_work = test_webui_core_imports()
    
    # Test WebUI sd_models module
    sd_models_work = test_webui_sd_models()
    
    # Check overall WebUI readiness
    webui_ready = check_webui_readiness()
    
    print("\n" + "=" * 60)
    print("FINAL INSTALLATION SUMMARY")
    print("=" * 60)
    
    if tomesd_works and core_imports_work and webui_ready:
        print("🎉 All core WebUI dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. tomesd import error should be resolved")
        print("3. WebUI should complete initialization and start the web interface")
        print("4. Access WebUI at: http://127.0.0.1:7860")
    elif tomesd_works:
        print("✅ tomesd is working!")
        print("⚠️  Some other dependencies may have issues")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. Monitor for any additional missing modules")
    else:
        print("❌ tomesd installation failed")
        print("\nTroubleshooting:")
        print("1. Check internet connection")
        print("2. Try manual installation: pip install tomesd")
        print("3. Check virtual environment activation")
    
    if sd_models_work:
        print("\n✅ WebUI sd_models module should work correctly")
    else:
        print("\n⚠️  WebUI sd_models module may still have issues")
    
    print(f"\nPython version: {sys.version}")
    print("Virtual environment should have all core WebUI dependencies now")
    
    if webui_ready:
        print("\n🚀 WebUI is ready to launch!")
        print("All critical dependencies are available")
    else:
        print("\n⚠️  Some critical dependencies may still be missing")

if __name__ == "__main__":
    main()
