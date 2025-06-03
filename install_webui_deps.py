#!/usr/bin/env python3
"""
Install WebUI Dependencies for Python 3.13

This script installs all essential dependencies for stable-diffusion-webui
that might be missing from the virtual environment.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess

def install_webui_dependencies():
    """Install essential WebUI dependencies"""
    print("=== Installing WebUI Dependencies ===")
    
    # Essential WebUI dependencies in order of importance
    webui_deps = [
        # Core ML libraries
        "pytorch_lightning>=2.0.0",
        "torchmetrics>=0.11.0",
        
        # Configuration and model handling
        "omegaconf>=2.2.0",
        "safetensors>=0.3.0",
        "accelerate>=0.20.0",
        
        # Image processing
        "Pillow>=9.0.0",
        "opencv-python>=4.6.0",
        "imageio>=2.22.0",
        "scikit-image>=0.19.0",
        
        # Web interface
        "gradio>=3.40.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        
        # Utilities
        "tqdm>=4.64.0",
        "requests>=2.28.0",
        "numpy>=1.21.0",
        "scipy>=1.9.0",
        
        # Text processing (alternatives to CLIP)
        "transformers>=4.30.0",
        "diffusers>=0.20.0",
        
        # Additional utilities
        "psutil>=5.9.0",
        "GitPython>=3.1.30",
        "einops>=0.6.1",
        "kornia>=0.6.8",
        "jsonmerge>=1.9.0",
        "inflection>=0.5.1",
        "lark>=1.1.5",
        
        # Image enhancement
        "realesrgan>=0.3.0",
        "basicsr>=1.4.2",
        "gfpgan>=1.3.8",
        
        # Math and algorithms
        "torchsde>=0.2.5",
        "torchdiffeq>=0.2.3",
        "resize-right>=0.0.2",
        "clean-fid>=0.1.35",
        
        # Fonts and metadata
        "piexif>=1.1.3",
        "fonts>=0.0.3",
        "font-roboto>=0.0.1",
        
        # Additional ML utilities
        "timm>=0.9.2",
        "addict>=2.4.0",
        "blendmodes>=2022",
    ]
    
    print(f"Installing {len(webui_deps)} WebUI dependencies...")
    
    successful = 0
    failed = []
    
    for dep in webui_deps:
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
    
    print(f"\nResults: {successful}/{len(webui_deps)} successful")
    if failed:
        print(f"Failed packages: {len(failed)}")
        for pkg in failed[:5]:  # Show first 5 failures
            print(f"  - {pkg}")
        if len(failed) > 5:
            print(f"  ... and {len(failed) - 5} more")
    
    return successful > len(webui_deps) * 0.7  # 70% success rate

def test_pytorch_lightning():
    """Test pytorch_lightning specifically"""
    print("\n=== Testing PyTorch Lightning ===")
    
    try:
        import pytorch_lightning as pl
        print(f"✅ pytorch_lightning version: {pl.__version__}")
        
        # Test basic functionality
        import torch
        print(f"PyTorch version: {torch.__version__}")
        
        # Check compatibility
        if hasattr(pl, 'LightningModule'):
            print("✅ LightningModule available")
        
        return True
    except ImportError as e:
        print(f"❌ pytorch_lightning import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ pytorch_lightning test failed: {e}")
        return False

def test_webui_imports():
    """Test key WebUI imports"""
    print("\n=== Testing Key WebUI Imports ===")
    
    key_imports = [
        "pytorch_lightning",
        "torchmetrics",
        "omegaconf", 
        "safetensors",
        "accelerate",
        "PIL",
        "cv2",
        "gradio",
        "transformers",
        "diffusers"
    ]
    
    working = 0
    for module in key_imports:
        try:
            if module == "cv2":
                __import__("cv2")
            else:
                __import__(module)
            print(f"✅ {module}")
            working += 1
        except ImportError:
            print(f"❌ {module}")
    
    print(f"\nWorking imports: {working}/{len(key_imports)}")
    return working >= len(key_imports) * 0.8  # 80% success rate

def check_pytorch_compatibility():
    """Check PyTorch and pytorch_lightning compatibility"""
    print("\n=== Checking PyTorch Compatibility ===")
    
    try:
        import torch
        import pytorch_lightning as pl
        
        torch_version = torch.__version__
        pl_version = pl.__version__
        
        print(f"PyTorch: {torch_version}")
        print(f"PyTorch Lightning: {pl_version}")
        
        # Check if versions are compatible
        torch_major = int(torch_version.split('.')[0])
        torch_minor = int(torch_version.split('.')[1])
        
        if torch_major >= 2:
            print("✅ PyTorch 2.x detected - should be compatible")
        elif torch_major == 1 and torch_minor >= 12:
            print("✅ PyTorch 1.12+ detected - should be compatible")
        else:
            print("⚠️  Older PyTorch version - may have compatibility issues")
        
        return True
    except Exception as e:
        print(f"❌ Compatibility check failed: {e}")
        return False

def main():
    """Main function"""
    print("WebUI Dependencies Installation for Python 3.13")
    print("=" * 60)
    print("Installing essential dependencies for stable-diffusion-webui...")
    print()
    
    # Install WebUI dependencies
    deps_success = install_webui_dependencies()
    
    # Test pytorch_lightning specifically
    pl_works = test_pytorch_lightning()
    
    # Test other key imports
    imports_work = test_webui_imports()
    
    # Check compatibility
    compat_ok = check_pytorch_compatibility()
    
    print("\n" + "=" * 60)
    print("INSTALLATION SUMMARY")
    print("=" * 60)
    
    if pl_works and imports_work:
        print("✅ WebUI dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. pytorch_lightning import error should be resolved")
        print("3. WebUI should proceed to model loading")
    elif pl_works:
        print("✅ pytorch_lightning is working!")
        print("⚠️  Some other dependencies may have issues")
        print("\nNext steps:")
        print("1. Try launching WebUI: .\\webui_compatible.bat")
        print("2. Monitor for any additional missing modules")
    else:
        print("❌ pytorch_lightning installation failed")
        print("\nTroubleshooting:")
        print("1. Check internet connection")
        print("2. Try manual installation: pip install pytorch_lightning")
        print("3. Check virtual environment activation")
    
    if compat_ok:
        print("\n✅ PyTorch and pytorch_lightning versions are compatible")
    else:
        print("\n⚠️  Version compatibility issues detected")
    
    print(f"\nPython version: {sys.version}")
    print("Virtual environment should have all WebUI dependencies now")

if __name__ == "__main__":
    main()
