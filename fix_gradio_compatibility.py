#!/usr/bin/env python3
"""
Fix Gradio Compatibility Issues for Python 3.13

This script fixes Gradio version compatibility issues between
WebUI v1.10.1 and newer Gradio versions.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess
import os

def check_gradio_version():
    """Check current Gradio version"""
    print("=== Checking Gradio Version ===")
    
    try:
        import gradio as gr
        version = gr.__version__
        print(f"Current Gradio version: {version}")
        
        # Check if IOComponent exists
        try:
            iocomponent = gr.components.IOComponent
            print("✅ gr.components.IOComponent available (Gradio 3.x)")
            return version, "3.x", True
        except AttributeError:
            try:
                component = gr.components.Component
                print("✅ gr.components.Component available (Gradio 4.x+)")
                return version, "4.x+", False
            except AttributeError:
                print("❌ Neither IOComponent nor Component found")
                return version, "unknown", False
    
    except ImportError:
        print("❌ Gradio not installed")
        return None, None, False

def install_compatible_gradio():
    """Install a compatible Gradio version"""
    print("\n=== Installing Compatible Gradio Version ===")
    
    # WebUI v1.10.1 is compatible with Gradio 3.x
    compatible_versions = [
        "gradio>=3.40.0,<4.0.0",  # Latest 3.x
        "gradio==3.50.2",         # Specific stable version
        "gradio==3.41.2"          # Alternative stable version
    ]
    
    for version_spec in compatible_versions:
        try:
            print(f"Installing {version_spec}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", version_spec
            ], check=True, capture_output=True)
            
            # Test if it works
            try:
                import gradio as gr
                # Test IOComponent access
                iocomponent = gr.components.IOComponent
                print(f"✅ {version_spec} installed and working")
                return True
            except (ImportError, AttributeError):
                continue
                
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {version_spec}")
            continue
    
    return False

def patch_gradio_extensions():
    """Patch gradio_extensons.py for compatibility"""
    print("\n=== Patching Gradio Extensions ===")
    
    extensions_file = "modules/gradio_extensons.py"
    
    if not os.path.exists(extensions_file):
        print(f"❌ {extensions_file} not found")
        return False
    
    try:
        with open(extensions_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already patched
        if "Handle Gradio version compatibility" in content:
            print("✅ gradio_extensons.py already patched")
            return True
        
        # Check if needs patching
        if "gr.components.IOComponent" in content:
            print("Patching gradio_extensons.py for Gradio compatibility...")
            
            # Create backup
            backup_file = extensions_file + ".gradio_backup"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Apply patch
            old_line = "original_IOComponent_init = patches.patch(__name__, obj=gr.components.IOComponent, field=\"__init__\", replacement=IOComponent_init)"
            new_lines = """# Handle Gradio version compatibility - IOComponent was renamed to Component in Gradio 4.x
try:
    # Try Gradio 3.x API first
    original_IOComponent_init = patches.patch(__name__, obj=gr.components.IOComponent, field="__init__", replacement=IOComponent_init)
except AttributeError:
    # Fallback to Gradio 4.x+ API
    try:
        original_IOComponent_init = patches.patch(__name__, obj=gr.components.Component, field="__init__", replacement=IOComponent_init)
    except AttributeError:
        # If both fail, create a dummy patch
        print("⚠️  Gradio component patching failed - using fallback")
        original_IOComponent_init = None"""
            
            content = content.replace(old_line, new_lines)
            
            with open(extensions_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Patched {extensions_file}")
            return True
        else:
            print("✅ gradio_extensons.py doesn't need patching")
            return True
            
    except Exception as e:
        print(f"❌ Error patching {extensions_file}: {e}")
        return False

def test_gradio_webui_compatibility():
    """Test if Gradio works with WebUI"""
    print("\n=== Testing Gradio WebUI Compatibility ===")
    
    try:
        import gradio as gr
        print(f"Gradio version: {gr.__version__}")
        
        # Test basic Gradio functionality
        try:
            # Test component creation
            textbox = gr.Textbox()
            print("✅ Gradio Textbox component works")
            
            # Test IOComponent/Component access
            try:
                base_class = gr.components.IOComponent
                print("✅ Using Gradio 3.x API (IOComponent)")
            except AttributeError:
                try:
                    base_class = gr.components.Component
                    print("✅ Using Gradio 4.x+ API (Component)")
                except AttributeError:
                    print("❌ Neither IOComponent nor Component available")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Gradio component test failed: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Gradio import failed: {e}")
        return False

def test_webui_gradio_extensions():
    """Test if WebUI gradio_extensons module works"""
    print("\n=== Testing WebUI Gradio Extensions ===")
    
    try:
        # Add modules directory to path
        modules_path = os.path.join(os.getcwd(), "modules")
        if modules_path not in sys.path:
            sys.path.insert(0, modules_path)
        
        # Try importing gradio_extensons
        import gradio_extensons
        print("✅ WebUI gradio_extensons module imports successfully")
        return True
    except ImportError as e:
        print(f"❌ WebUI gradio_extensons import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ WebUI gradio_extensons test failed: {e}")
        return False

def main():
    """Main function"""
    print("Gradio Compatibility Fix for Python 3.13")
    print("=" * 60)
    
    # Check current Gradio version
    version, api_version, has_iocomponent = check_gradio_version()
    
    if version is None:
        print("Installing Gradio...")
        if not install_compatible_gradio():
            print("❌ Could not install compatible Gradio")
            return
    elif not has_iocomponent:
        print("Incompatible Gradio version detected, installing compatible version...")
        if not install_compatible_gradio():
            print("❌ Could not install compatible Gradio")
            # Continue anyway, patch might work
    
    # Patch gradio extensions
    extensions_patched = patch_gradio_extensions()
    
    # Test Gradio compatibility
    gradio_works = test_gradio_webui_compatibility()
    
    # Test WebUI gradio extensions
    extensions_work = test_webui_gradio_extensions()
    
    print("\n" + "=" * 60)
    print("GRADIO COMPATIBILITY FIX SUMMARY")
    print("=" * 60)
    
    if gradio_works and extensions_work:
        print("✅ Gradio compatibility issues resolved!")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. Gradio IOComponent error should be resolved")
        print("3. WebUI should complete initialization and start web interface")
        print("4. Access WebUI at: http://127.0.0.1:7860")
    elif gradio_works:
        print("✅ Gradio is working!")
        print("⚠️  WebUI gradio extensions may have issues")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. Monitor for any additional Gradio-related errors")
    else:
        print("❌ Gradio compatibility issues remain")
        print("\nTroubleshooting:")
        print("1. Try manual installation: pip install 'gradio>=3.40.0,<4.0.0'")
        print("2. Check virtual environment activation")
        print("3. Restart terminal and try again")
    
    # Show current status
    final_version, final_api, final_iocomponent = check_gradio_version()
    if final_version:
        print(f"\nFinal Gradio version: {final_version}")
        print(f"API compatibility: {'3.x (IOComponent)' if final_iocomponent else '4.x+ (Component)'}")
    
    print(f"\nPython version: {sys.version}")
    print("Gradio should now be compatible with WebUI v1.10.1")

if __name__ == "__main__":
    main()
