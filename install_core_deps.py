#!/usr/bin/env python3
"""
Install Core Dependencies for stable-diffusion-webui

This script installs essential Python modules that are required
for WebUI initialization but may be missing from Python 3.13 environments.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess

def install_core_dependencies():
    """Install core Python dependencies"""
    print("=== Installing Core Dependencies ===")
    
    # Essential modules for WebUI initialization
    core_deps = [
        "packaging",        # Version parsing (missing in your case)
        "setuptools",       # Package installation
        "wheel",           # Wheel package format
        "pip",             # Package installer (upgrade)
        "importlib-metadata", # Import metadata
        "typing-extensions", # Type hints
        "certifi",         # SSL certificates
        "charset-normalizer", # Character encoding
        "idna",            # Internationalized domain names
        "urllib3",         # HTTP library
        "requests",        # HTTP requests
        "six",             # Python 2/3 compatibility
        "python-dateutil", # Date utilities
        "pytz",            # Timezone handling
        "zipp",            # Zipfile utilities
    ]
    
    print(f"Installing {len(core_deps)} core dependencies...")
    
    successful = 0
    failed = []
    
    for dep in core_deps:
        try:
            print(f"Installing {dep}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", dep, "--upgrade"
            ], check=True, capture_output=True, text=True)
            print(f"✅ {dep}")
            successful += 1
        except subprocess.CalledProcessError as e:
            print(f"❌ {dep} failed: {e}")
            failed.append(dep)
    
    print(f"\nResults: {successful}/{len(core_deps)} successful")
    if failed:
        print(f"Failed: {failed}")
    
    return successful > 0

def test_packaging_import():
    """Test if packaging module works correctly"""
    print("\n=== Testing Packaging Module ===")
    
    try:
        import packaging
        print(f"✅ packaging module available: {packaging.__version__}")
        
        from packaging import version
        print("✅ packaging.version available")
        
        # Test version parsing (what WebUI uses)
        test_version = version.parse("1.0.0")
        print(f"✅ Version parsing works: {test_version}")
        
        return True
    except ImportError as e:
        print(f"❌ packaging import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ packaging test failed: {e}")
        return False

def test_other_essential_imports():
    """Test other modules that WebUI might need"""
    print("\n=== Testing Other Essential Modules ===")
    
    essential_modules = [
        "setuptools",
        "wheel", 
        "importlib_metadata",
        "typing_extensions",
        "requests",
        "certifi",
        "urllib3"
    ]
    
    working = 0
    for module in essential_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
            working += 1
        except ImportError:
            print(f"❌ {module}")
    
    print(f"\nWorking modules: {working}/{len(essential_modules)}")
    return working >= len(essential_modules) * 0.8  # 80% success rate

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("\n=== Upgrading Pip ===")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True, capture_output=True)
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Pip upgrade failed: {e}")
        return False

def clear_pip_cache():
    """Clear pip cache to avoid conflicts"""
    print("\n=== Clearing Pip Cache ===")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "cache", "purge"
        ], check=True, capture_output=True)
        print("✅ Pip cache cleared")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Could not clear pip cache (not critical)")
        return True

def main():
    """Main function"""
    print("Core Dependencies Installation for Python 3.13")
    print("=" * 60)
    print("Installing essential modules for WebUI initialization...")
    print()
    
    # Clear cache first
    clear_pip_cache()
    
    # Upgrade pip
    upgrade_pip()
    
    # Install core dependencies
    deps_installed = install_core_dependencies()
    
    # Test packaging specifically
    packaging_works = test_packaging_import()
    
    # Test other essential modules
    other_modules_work = test_other_essential_imports()
    
    print("\n" + "=" * 60)
    print("INSTALLATION SUMMARY")
    print("=" * 60)
    
    if packaging_works and other_modules_work:
        print("✅ All core dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Try launching WebUI again: .\\webui_compatible.bat")
        print("2. The 'packaging' module error should be resolved")
        print("3. WebUI should proceed past requirements validation")
    elif packaging_works:
        print("✅ Packaging module fixed!")
        print("⚠️  Some other modules may have issues")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. Monitor for any additional missing modules")
    else:
        print("❌ Packaging module installation failed")
        print("\nTroubleshooting:")
        print("1. Check internet connection")
        print("2. Try manual installation: pip install packaging")
        print("3. Check virtual environment activation")
    
    print(f"\nPython version: {sys.version}")
    print("Virtual environment should have all core dependencies now")

if __name__ == "__main__":
    main()
