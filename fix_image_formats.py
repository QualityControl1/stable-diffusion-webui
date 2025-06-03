#!/usr/bin/env python3
"""
Fix Image Format Dependencies for Python 3.13

This script handles pillow_avif and other image format dependencies
that might have compilation issues on Python 3.13.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess

def test_pillow_formats():
    """Test which image formats are supported by Pillow"""
    print("=== Testing Pillow Image Format Support ===")
    
    try:
        from PIL import Image
        print(f"Pillow version: {Image.__version__}")
        
        # Test basic formats
        basic_formats = ['JPEG', 'PNG', 'BMP', 'GIF', 'TIFF', 'WEBP']
        supported_formats = []
        
        for fmt in basic_formats:
            if fmt in Image.registered_extensions().values():
                supported_formats.append(fmt)
                print(f"✅ {fmt} supported")
            else:
                print(f"❌ {fmt} not supported")
        
        # Test AVIF specifically
        try:
            import pillow_avif
            print(f"✅ AVIF supported via pillow_avif")
            supported_formats.append('AVIF')
        except ImportError:
            print(f"❌ AVIF not supported (pillow_avif not installed)")
        
        return supported_formats
        
    except ImportError:
        print("❌ Pillow not installed")
        return []

def install_image_format_dependencies():
    """Install image format dependencies"""
    print("\n=== Installing Image Format Dependencies ===")
    
    # Image format packages to try
    image_packages = [
        "pillow_avif",      # AVIF support (may fail on Python 3.13)
        "pillow_heif",      # HEIF support (may fail on Python 3.13)
        "pillow_webp",      # Enhanced WebP support
    ]
    
    successful = 0
    failed = []
    
    for package in image_packages:
        try:
            print(f"Installing {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True, capture_output=True, text=True)
            print(f"✅ {package} installed successfully")
            successful += 1
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} installation failed")
            failed.append(package)
    
    print(f"\nResults: {successful}/{len(image_packages)} image format packages installed")
    if failed:
        print(f"Failed packages: {failed}")
    
    return successful > 0

def patch_image_imports():
    """Patch image-related imports to be optional"""
    print("\n=== Patching Image Format Imports ===")
    
    # Check if modules/images.py needs patching
    images_file = "modules/images.py"
    
    try:
        with open(images_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already patched
        if "AVIF_SUPPORT = True" in content:
            print("✅ modules/images.py already patched for pillow_avif")
            return True
        
        # Check if needs patching
        if "import pillow_avif" in content and "try:" not in content.split("import pillow_avif")[0].split('\n')[-1]:
            print("⚠️  modules/images.py needs pillow_avif patching")
            
            # Create backup
            backup_file = images_file + ".avif_backup"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Apply patch
            old_import = "import pillow_avif # noqa: F401"
            new_import = """try:
    import pillow_avif # noqa: F401
    AVIF_SUPPORT = True
except ImportError:
    print("⚠️  pillow_avif not available - AVIF image format support disabled")
    AVIF_SUPPORT = False"""
            
            content = content.replace(old_import, new_import)
            
            with open(images_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Patched {images_file}")
            return True
        else:
            print("✅ modules/images.py doesn't need patching")
            return True
            
    except FileNotFoundError:
        print(f"❌ {images_file} not found")
        return False
    except Exception as e:
        print(f"❌ Error patching {images_file}: {e}")
        return False

def test_webui_image_imports():
    """Test if WebUI image module can be imported"""
    print("\n=== Testing WebUI Image Module ===")
    
    try:
        # Add modules directory to path
        import os
        modules_path = os.path.join(os.getcwd(), "modules")
        if modules_path not in sys.path:
            sys.path.insert(0, modules_path)
        
        # Try importing the images module
        import images
        print("✅ WebUI images module imports successfully")
        
        # Check AVIF support
        if hasattr(images, 'AVIF_SUPPORT'):
            if images.AVIF_SUPPORT:
                print("✅ AVIF support enabled")
            else:
                print("⚠️  AVIF support disabled (pillow_avif not available)")
        
        return True
    except ImportError as e:
        print(f"❌ WebUI images module import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ WebUI images module test failed: {e}")
        return False

def create_image_format_test():
    """Create a simple test for image format support"""
    print("\n=== Creating Image Format Test ===")
    
    test_code = '''
import sys
import os

# Add modules to path
modules_path = os.path.join(os.getcwd(), "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

try:
    from PIL import Image
    print(f"Pillow version: {Image.__version__}")
    
    # Test AVIF support
    try:
        import pillow_avif
        print("✅ AVIF support available")
    except ImportError:
        print("⚠️  AVIF support not available")
    
    # Test WebUI images module
    try:
        import images
        print("✅ WebUI images module working")
        
        if hasattr(images, 'AVIF_SUPPORT'):
            print(f"AVIF support in WebUI: {images.AVIF_SUPPORT}")
    except ImportError as e:
        print(f"❌ WebUI images module failed: {e}")
    
except ImportError:
    print("❌ Pillow not available")
'''
    
    try:
        with open("test_image_formats.py", "w") as f:
            f.write(test_code)
        print("✅ Created test_image_formats.py")
        return True
    except Exception as e:
        print(f"❌ Could not create test file: {e}")
        return False

def main():
    """Main function"""
    print("Image Format Dependencies Fix for Python 3.13")
    print("=" * 60)
    
    # Test current Pillow support
    supported_formats = test_pillow_formats()
    
    # Try installing image format dependencies
    deps_installed = install_image_format_dependencies()
    
    # Patch image imports
    imports_patched = patch_image_imports()
    
    # Test WebUI image module
    webui_images_work = test_webui_image_imports()
    
    # Create test script
    test_created = create_image_format_test()
    
    print("\n" + "=" * 60)
    print("IMAGE FORMAT FIX SUMMARY")
    print("=" * 60)
    
    print(f"Supported formats: {', '.join(supported_formats) if supported_formats else 'None detected'}")
    print(f"Dependencies installed: {'Yes' if deps_installed else 'No'}")
    print(f"Imports patched: {'Yes' if imports_patched else 'No'}")
    print(f"WebUI images module: {'Working' if webui_images_work else 'Failed'}")
    
    if webui_images_work:
        print("\n✅ Image format issues resolved!")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. pillow_avif import error should be resolved")
        print("3. WebUI should proceed to model loading")
        
        if 'AVIF' not in supported_formats:
            print("\n⚠️  Note: AVIF support is disabled but WebUI will work normally")
    else:
        print("\n⚠️  Some image format issues remain")
        print("But WebUI should still work with basic image formats")
    
    if test_created:
        print("\n📋 Test script created: test_image_formats.py")
        print("Run it to verify image format support")
    
    print(f"\nPython version: {sys.version}")
    print("WebUI should now handle image format dependencies gracefully")

if __name__ == "__main__":
    main()
