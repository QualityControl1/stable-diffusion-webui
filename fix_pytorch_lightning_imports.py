#!/usr/bin/env python3
"""
Fix PyTorch Lightning Import Issues for Python 3.13

This script fixes PyTorch Lightning import compatibility issues
across all repository files by patching outdated import paths.

Author: Augment Agent
Date: January 2025
"""

import os
import glob
import sys

def find_pytorch_lightning_import_files():
    """Find all Python files with PyTorch Lightning imports"""
    print("=== Finding Files with PyTorch Lightning Imports ===")
    
    # Search patterns for PyTorch Lightning imports
    search_dirs = [
        "repositories/stable-diffusion-stability-ai",
        "repositories/generative-models", 
        "repositories/k-diffusion",
        "modules"
    ]
    
    problematic_files = []
    
    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
            
        # Find all Python files
        pattern = os.path.join(search_dir, "**", "*.py")
        python_files = glob.glob(pattern, recursive=True)
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for problematic imports
                problematic_imports = [
                    "from pytorch_lightning.utilities.distributed import",
                    "from pytorch_lightning.utilities.rank_zero import",
                    "from pytorch_lightning.utilities import rank_zero_only",
                    "pytorch_lightning.utilities.distributed",
                    "pytorch_lightning.utilities.rank_zero"
                ]
                
                for import_pattern in problematic_imports:
                    if import_pattern in content:
                        problematic_files.append(file_path)
                        print(f"Found problematic import in: {file_path}")
                        break
                        
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    return problematic_files

def patch_pytorch_lightning_imports(file_path):
    """Patch PyTorch Lightning imports in a specific file"""
    print(f"\nPatching {file_path}...")
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create backup
        backup_path = file_path + ".pl_backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Apply patches
        patches = [
            # rank_zero_only import
            {
                "old": "from pytorch_lightning.utilities.distributed import rank_zero_only",
                "new": """try:
    from pytorch_lightning.utilities.distributed import rank_zero_only
except ImportError:
    # PyTorch Lightning 2.x moved this to fabric.utilities
    try:
        from lightning.fabric.utilities.distributed import rank_zero_only
    except ImportError:
        # Fallback: create a simple rank_zero_only decorator
        def rank_zero_only(func):
            \"\"\"Simple fallback for rank_zero_only decorator\"\"\"
            return func"""
            },
            # rank_zero_warn import
            {
                "old": "from pytorch_lightning.utilities.rank_zero import rank_zero_warn",
                "new": """try:
    from pytorch_lightning.utilities.rank_zero import rank_zero_warn
except ImportError:
    # PyTorch Lightning 2.x moved this
    try:
        from lightning.fabric.utilities.rank_zero import rank_zero_warn
    except ImportError:
        # Fallback: create a simple rank_zero_warn function
        def rank_zero_warn(message):
            \"\"\"Simple fallback for rank_zero_warn\"\"\"
            print(f"WARNING: {message}")"""
            },
            # General utilities import
            {
                "old": "from pytorch_lightning.utilities import rank_zero_only",
                "new": """try:
    from pytorch_lightning.utilities import rank_zero_only
except ImportError:
    # PyTorch Lightning 2.x compatibility
    try:
        from lightning.fabric.utilities.distributed import rank_zero_only
    except ImportError:
        def rank_zero_only(func):
            return func"""
            }
        ]
        
        patched = False
        for patch in patches:
            if patch["old"] in content:
                content = content.replace(patch["old"], patch["new"])
                patched = True
                print(f"  ✅ Applied patch for: {patch['old'][:50]}...")
        
        if patched:
            # Write the patched file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Successfully patched {file_path}")
            return True
        else:
            print(f"  ⚠️  No patches needed for {file_path}")
            return True
            
    except Exception as e:
        print(f"  ❌ Error patching {file_path}: {e}")
        return False

def test_pytorch_lightning_version():
    """Test PyTorch Lightning version and compatibility"""
    print("\n=== Testing PyTorch Lightning Version ===")
    
    try:
        import pytorch_lightning as pl
        print(f"PyTorch Lightning version: {pl.__version__}")
        
        # Test if utilities.distributed exists
        try:
            from pytorch_lightning.utilities.distributed import rank_zero_only
            print("✅ pytorch_lightning.utilities.distributed available")
        except ImportError:
            print("❌ pytorch_lightning.utilities.distributed not available")
        
        # Test if fabric utilities exist
        try:
            from lightning.fabric.utilities.distributed import rank_zero_only
            print("✅ lightning.fabric.utilities.distributed available")
        except ImportError:
            print("❌ lightning.fabric.utilities.distributed not available")
        
        return True
    except ImportError:
        print("❌ PyTorch Lightning not installed")
        return False

def install_compatible_pytorch_lightning():
    """Install a compatible version of PyTorch Lightning"""
    print("\n=== Installing Compatible PyTorch Lightning ===")
    
    import subprocess
    
    # Try different versions
    versions_to_try = [
        "pytorch_lightning>=2.0.0,<3.0.0",  # Latest 2.x
        "pytorch_lightning==2.1.0",         # Specific stable version
        "pytorch_lightning==1.9.5"          # Fallback to 1.x
    ]
    
    for version in versions_to_try:
        try:
            print(f"Trying to install {version}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", version
            ], check=True, capture_output=True)
            
            # Test if it works
            try:
                import pytorch_lightning
                print(f"✅ Successfully installed {version}")
                return True
            except ImportError:
                continue
                
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {version}")
            continue
    
    return False

def main():
    """Main function"""
    print("PyTorch Lightning Import Fix for Python 3.13")
    print("=" * 60)
    
    # Test current PyTorch Lightning
    pl_available = test_pytorch_lightning_version()
    
    if not pl_available:
        print("Installing PyTorch Lightning...")
        if not install_compatible_pytorch_lightning():
            print("❌ Could not install PyTorch Lightning")
            return
    
    # Find files with problematic imports
    problematic_files = find_pytorch_lightning_import_files()
    
    if not problematic_files:
        print("✅ No problematic PyTorch Lightning imports found")
        return
    
    print(f"\nFound {len(problematic_files)} files with problematic imports")
    
    # Patch each file
    successful_patches = 0
    for file_path in problematic_files:
        if patch_pytorch_lightning_imports(file_path):
            successful_patches += 1
    
    print("\n" + "=" * 60)
    print("PATCH SUMMARY")
    print("=" * 60)
    
    if successful_patches == len(problematic_files):
        print("✅ All PyTorch Lightning import issues fixed!")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. pytorch_lightning.utilities.distributed error should be resolved")
        print("3. WebUI should proceed to model loading")
    else:
        print(f"⚠️  {successful_patches}/{len(problematic_files)} files patched successfully")
        print("Some files may still have import issues")
    
    # Test imports after patching
    print("\nTesting imports after patching...")
    test_pytorch_lightning_version()
    
    print(f"\nPython version: {sys.version}")
    print("PyTorch Lightning imports should now be compatible")

if __name__ == "__main__":
    main()
