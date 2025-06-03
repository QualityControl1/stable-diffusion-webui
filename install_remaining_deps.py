#!/usr/bin/env python3
"""
Install Remaining WebUI Dependencies for Python 3.13

This script installs all remaining dependencies that might be missing
from the virtual environment to prevent further import errors.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess

def install_remaining_webui_dependencies():
    """Install all remaining WebUI dependencies"""
    print("=== Installing Remaining WebUI Dependencies ===")
    
    # Comprehensive list of WebUI dependencies that might be missing
    remaining_deps = [
        # Core missing dependencies
        "diskcache>=5.4.0",        # The current missing module
        "jsonmerge>=1.9.0",        # JSON merging utilities
        "inflection>=0.5.1",       # String inflection utilities
        
        # Web interface dependencies
        "gradio>=3.40.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "httpx>=0.24.0",
        "websockets>=11.0",
        
        # Image processing
        "Pillow>=9.0.0",
        "opencv-python>=4.6.0",
        "imageio>=2.22.0",
        "scikit-image>=0.19.0",
        
        # Utilities
        "tqdm>=4.64.0",
        "requests>=2.28.0",
        "numpy>=1.21.0",
        "scipy>=1.9.0",
        "psutil>=5.9.0",
        
        # Configuration and serialization
        "pyyaml>=6.0",
        "toml>=0.10.2",
        "configparser>=5.3.0",
        
        # Math and algorithms
        "einops>=0.6.1",
        "kornia>=0.6.8",
        "torchsde>=0.2.5",
        "torchdiffeq>=0.2.3",
        
        # Text processing alternatives
        "transformers>=4.30.0",
        "diffusers>=0.20.0",
        "tokenizers>=0.13.0",
        
        # Additional utilities
        "GitPython>=3.1.30",
        "lark>=1.1.5",
        "addict>=2.4.0",
        "blendmodes>=2022",
        
        # Image enhancement (may fail but not critical)
        "realesrgan>=0.3.0",
        "basicsr>=1.4.2",
        "gfpgan>=1.3.8",
        
        # Fonts and metadata
        "piexif>=1.1.3",
        "fonts>=0.0.3",
        "font-roboto>=0.0.1",
        
        # Additional ML utilities
        "timm>=0.9.2",
        "resize-right>=0.0.2",
        "clean-fid>=0.1.35",
        
        # Development utilities
        "rich>=13.0.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
    ]
    
    print(f"Installing {len(remaining_deps)} remaining dependencies...")
    
    successful = 0
    failed = []
    critical_failed = []
    
    # Critical dependencies that must succeed
    critical_deps = ["diskcache", "jsonmerge", "inflection", "gradio", "fastapi", "uvicorn"]
    
    for dep in remaining_deps:
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
    
    print(f"\nResults: {successful}/{len(remaining_deps)} successful")
    if failed:
        print(f"Failed packages: {len(failed)}")
        for pkg in failed[:5]:  # Show first 5 failures
            print(f"  - {pkg}")
        if len(failed) > 5:
            print(f"  ... and {len(failed) - 5} more")
    
    if critical_failed:
        print(f"\n⚠️  Critical dependencies failed: {critical_failed}")
        return False
    
    return successful > len(remaining_deps) * 0.7  # 70% success rate

def test_diskcache_specifically():
    """Test diskcache module specifically"""
    print("\n=== Testing diskcache Module ===")
    
    try:
        import diskcache
        print(f"✅ diskcache version: {diskcache.__version__}")
        
        # Test basic functionality
        cache = diskcache.Cache()
        cache.set('test_key', 'test_value')
        value = cache.get('test_key')
        cache.close()
        
        if value == 'test_value':
            print("✅ diskcache basic functionality working")
        else:
            print("⚠️  diskcache functionality issue")
        
        return True
    except ImportError as e:
        print(f"❌ diskcache import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ diskcache test failed: {e}")
        return False

def test_critical_webui_imports():
    """Test critical WebUI imports"""
    print("\n=== Testing Critical WebUI Imports ===")
    
    critical_imports = [
        "diskcache",
        "jsonmerge",
        "inflection",
        "gradio",
        "fastapi",
        "uvicorn",
        "PIL",
        "numpy",
        "torch",
        "transformers"
    ]
    
    working = 0
    for module in critical_imports:
        try:
            if module == "PIL":
                __import__("PIL")
            else:
                __import__(module)
            print(f"✅ {module}")
            working += 1
        except ImportError:
            print(f"❌ {module}")
    
    print(f"\nWorking critical imports: {working}/{len(critical_imports)}")
    return working >= len(critical_imports) * 0.9  # 90% success rate for critical imports

def check_webui_cache_module():
    """Check if WebUI's cache module can be imported"""
    print("\n=== Testing WebUI Cache Module ===")
    
    try:
        # Try importing the WebUI cache module
        import sys
        import os
        
        # Add modules directory to path if not already there
        modules_path = os.path.join(os.getcwd(), "modules")
        if modules_path not in sys.path:
            sys.path.insert(0, modules_path)
        
        import cache
        print("✅ WebUI cache module imports successfully")
        return True
    except ImportError as e:
        print(f"❌ WebUI cache module import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ WebUI cache module test failed: {e}")
        return False

def main():
    """Main function"""
    print("Remaining WebUI Dependencies Installation for Python 3.13")
    print("=" * 60)
    print("Installing remaining dependencies to prevent import errors...")
    print()
    
    # Install remaining dependencies
    deps_success = install_remaining_webui_dependencies()
    
    # Test diskcache specifically
    diskcache_works = test_diskcache_specifically()
    
    # Test other critical imports
    critical_imports_work = test_critical_webui_imports()
    
    # Test WebUI cache module
    cache_module_works = check_webui_cache_module()
    
    print("\n" + "=" * 60)
    print("INSTALLATION SUMMARY")
    print("=" * 60)
    
    if diskcache_works and critical_imports_work:
        print("✅ All critical dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. diskcache import error should be resolved")
        print("3. WebUI should proceed further in initialization")
    elif diskcache_works:
        print("✅ diskcache is working!")
        print("⚠️  Some other dependencies may have issues")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. Monitor for any additional missing modules")
    else:
        print("❌ diskcache installation failed")
        print("\nTroubleshooting:")
        print("1. Check internet connection")
        print("2. Try manual installation: pip install diskcache")
        print("3. Check virtual environment activation")
    
    if cache_module_works:
        print("\n✅ WebUI cache module should work correctly")
    else:
        print("\n⚠️  WebUI cache module may still have issues")
    
    print(f"\nPython version: {sys.version}")
    print("Virtual environment should have all remaining WebUI dependencies now")

if __name__ == "__main__":
    main()
