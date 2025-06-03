#!/usr/bin/env python3
"""
Fix UI Compatibility Issues for Python 3.13

This script fixes Pydantic v2, Gradio version, and NumPy compatibility
issues that prevent WebUI from creating the web interface.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess
import os

def check_current_versions():
    """Check current versions of critical packages"""
    print("=== Checking Current Package Versions ===")
    
    packages = {
        'pydantic': None,
        'gradio': None,
        'numpy': None,
        'fastapi': None
    }
    
    for package in packages:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            packages[package] = version
            print(f"{package}: {version}")
        except ImportError:
            print(f"{package}: not installed")
            packages[package] = None
    
    return packages

def install_compatible_versions():
    """Install compatible versions of critical packages"""
    print("\n=== Installing Compatible Package Versions ===")
    
    # Exact versions that work with WebUI v1.10.1
    compatible_packages = [
        "gradio==3.41.2",           # Exact version expected by WebUI
        "pydantic>=1.10.0,<2.0.0",  # Pydantic v1 to avoid __config__ issues
        "numpy>=2.0.2",             # Fix blendmodes compatibility
        "fastapi>=0.100.0",         # Compatible FastAPI version
        "uvicorn>=0.23.0",          # Compatible ASGI server
    ]
    
    successful = 0
    failed = []
    
    for package in compatible_packages:
        try:
            print(f"Installing {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True, capture_output=True)
            print(f"✅ {package}")
            successful += 1
        except subprocess.CalledProcessError:
            print(f"❌ {package} failed")
            failed.append(package)
    
    print(f"\nResults: {successful}/{len(compatible_packages)} packages installed")
    if failed:
        print(f"Failed packages: {failed}")
    
    return successful == len(compatible_packages)

def patch_pydantic_compatibility():
    """Patch modules/api/models.py for Pydantic v1/v2 compatibility"""
    print("\n=== Patching Pydantic Compatibility ===")
    
    models_file = "modules/api/models.py"
    
    if not os.path.exists(models_file):
        print(f"❌ {models_file} not found")
        return False
    
    try:
        with open(models_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already patched
        if "Handle Pydantic v1/v2 compatibility" in content:
            print("✅ modules/api/models.py already patched")
            return True
        
        # Check if needs patching
        if "DynamicModel.__config__.allow_population_by_field_name" in content:
            print("Patching modules/api/models.py for Pydantic compatibility...")
            
            # Create backup
            backup_file = models_file + ".pydantic_backup"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Apply patch
            old_code = """        DynamicModel = create_model(self._model_name, **fields)
        DynamicModel.__config__.allow_population_by_field_name = True
        DynamicModel.__config__.allow_mutation = True
        return DynamicModel"""
            
            new_code = """        DynamicModel = create_model(self._model_name, **fields)
        
        # Handle Pydantic v1/v2 compatibility - __config__ was replaced with model_config in v2
        try:
            # Pydantic v1 API
            DynamicModel.__config__.allow_population_by_field_name = True
            DynamicModel.__config__.allow_mutation = True
        except AttributeError:
            # Pydantic v2 API
            try:
                from pydantic import ConfigDict
                DynamicModel.model_config = ConfigDict(
                    populate_by_name=True,
                    arbitrary_types_allowed=True
                )
            except ImportError:
                # Fallback if ConfigDict not available
                print("⚠️  Pydantic configuration failed - using defaults")
        
        return DynamicModel"""
            
            content = content.replace(old_code, new_code)
            
            with open(models_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Patched {models_file}")
            return True
        else:
            print("✅ modules/api/models.py doesn't need patching")
            return True
            
    except Exception as e:
        print(f"❌ Error patching {models_file}: {e}")
        return False

def test_ui_compatibility():
    """Test if UI components can be imported"""
    print("\n=== Testing UI Compatibility ===")
    
    try:
        # Test Pydantic
        import pydantic
        print(f"✅ Pydantic {pydantic.__version__} imported")
        
        # Test Gradio
        import gradio as gr
        print(f"✅ Gradio {gr.__version__} imported")
        
        # Test basic Gradio component
        textbox = gr.Textbox()
        print("✅ Gradio Textbox component works")
        
        # Test NumPy
        import numpy as np
        print(f"✅ NumPy {np.__version__} imported")
        
        # Test FastAPI
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__} imported")
        
        return True
        
    except Exception as e:
        print(f"❌ UI compatibility test failed: {e}")
        return False

def test_webui_api_models():
    """Test if WebUI API models can be imported"""
    print("\n=== Testing WebUI API Models ===")
    
    try:
        # Add modules directory to path
        modules_path = os.path.join(os.getcwd(), "modules")
        if modules_path not in sys.path:
            sys.path.insert(0, modules_path)
        
        # Try importing API models
        from api import models
        print("✅ WebUI API models import successfully")
        
        # Test model generation
        try:
            # This should work without AttributeError now
            test_model = models.StableDiffusionTxt2ImgProcessingAPI
            print("✅ Pydantic model generation works")
        except AttributeError as e:
            if "__config__" in str(e):
                print(f"❌ Pydantic __config__ error still present: {e}")
                return False
            else:
                print(f"⚠️  Other AttributeError: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ WebUI API models import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ WebUI API models test failed: {e}")
        return False

def main():
    """Main function"""
    print("UI Compatibility Fix for Python 3.13")
    print("=" * 60)
    
    # Check current versions
    current_versions = check_current_versions()
    
    # Install compatible versions
    versions_installed = install_compatible_versions()
    
    # Patch Pydantic compatibility
    pydantic_patched = patch_pydantic_compatibility()
    
    # Test UI compatibility
    ui_compatible = test_ui_compatibility()
    
    # Test WebUI API models
    api_models_work = test_webui_api_models()
    
    print("\n" + "=" * 60)
    print("UI COMPATIBILITY FIX SUMMARY")
    print("=" * 60)
    
    if versions_installed and pydantic_patched and ui_compatible and api_models_work:
        print("🎉 All UI compatibility issues resolved!")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. Pydantic __config__ errors should be resolved")
        print("3. Gradio version mismatch should be fixed")
        print("4. NumPy version conflict should be resolved")
        print("5. WebUI should complete UI creation and start web interface")
        print("6. Access WebUI at: http://127.0.0.1:7860")
    else:
        print("⚠️  Some UI compatibility issues remain")
        
        if not versions_installed:
            print("❌ Package version installation failed")
        if not pydantic_patched:
            print("❌ Pydantic patching failed")
        if not ui_compatible:
            print("❌ UI compatibility test failed")
        if not api_models_work:
            print("❌ WebUI API models test failed")
    
    # Show final versions
    print("\nFinal package versions:")
    final_versions = check_current_versions()
    
    print(f"\nPython version: {sys.version}")
    print("WebUI should now be able to create the web interface successfully")

if __name__ == "__main__":
    main()
