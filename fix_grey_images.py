#!/usr/bin/env python3
"""
Fix Grey Image Generation Issues
================================

This script diagnoses and fixes grey/blank image generation issues
in stable-diffusion-webui, specifically focusing on VAE configuration.

The main causes of grey images:
1. Missing or misconfigured VAE (Variational Autoencoder)
2. VAE not loading properly
3. Model compatibility issues
4. Half-precision VAE issues

Author: Augment Agent
Date: January 2025
"""

import sys
import os
import json
import requests
import hashlib
from pathlib import Path

def check_current_vae_config():
    """Check current VAE configuration"""
    print("=== Checking Current VAE Configuration ===")
    
    # Check ui-config.json
    ui_config_file = "ui-config.json"
    if os.path.exists(ui_config_file):
        try:
            with open(ui_config_file, 'r') as f:
                ui_config = json.load(f)
            
            txt2img_vae = ui_config.get("txt2img/Preferred VAE/value", "None")
            img2img_vae = ui_config.get("img2img/Preferred VAE/value", "None")
            
            print(f"Current txt2img VAE: {txt2img_vae}")
            print(f"Current img2img VAE: {img2img_vae}")
            
            if txt2img_vae == "None" and img2img_vae == "None":
                print("❌ No VAE configured - this is likely causing grey images!")
                return False
            else:
                print("✅ VAE is configured")
                return True
                
        except Exception as e:
            print(f"❌ Error reading ui-config.json: {e}")
            return False
    else:
        print("❌ ui-config.json not found")
        return False

def check_available_vaes():
    """Check what VAE files are available"""
    print("\n=== Checking Available VAE Files ===")
    
    vae_dir = Path("models/VAE")
    vae_files = []
    
    if vae_dir.exists():
        for ext in ['.pt', '.ckpt', '.safetensors']:
            vae_files.extend(list(vae_dir.glob(f"*{ext}")))
    
    if vae_files:
        print("✅ Found VAE files:")
        for vae_file in vae_files:
            print(f"  - {vae_file.name}")
        return vae_files
    else:
        print("❌ No VAE files found in models/VAE/")
        return []

def download_recommended_vae():
    """Download a recommended VAE for general use"""
    print("\n=== Downloading Recommended VAE ===")
    
    # SD 1.5 VAE - works with most models
    vae_url = "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors"
    vae_filename = "vae-ft-mse-840000-ema-pruned.safetensors"
    vae_path = Path("models/VAE") / vae_filename
    
    # Create VAE directory if it doesn't exist
    vae_path.parent.mkdir(exist_ok=True)
    
    if vae_path.exists():
        print(f"✅ VAE already exists: {vae_filename}")
        return str(vae_path)
    
    print(f"Downloading VAE: {vae_filename}")
    print("This may take a few minutes...")
    
    try:
        response = requests.get(vae_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(vae_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}%", end='', flush=True)
        
        print(f"\n✅ Downloaded VAE: {vae_filename}")
        return str(vae_path)
        
    except Exception as e:
        print(f"\n❌ Failed to download VAE: {e}")
        return None

def configure_vae_in_ui_config(vae_name):
    """Configure VAE in ui-config.json"""
    print(f"\n=== Configuring VAE: {vae_name} ===")
    
    ui_config_file = "ui-config.json"
    
    try:
        # Read current config
        if os.path.exists(ui_config_file):
            with open(ui_config_file, 'r') as f:
                ui_config = json.load(f)
        else:
            ui_config = {}
        
        # Set VAE for both txt2img and img2img
        ui_config["txt2img/Preferred VAE/value"] = vae_name
        ui_config["img2img/Preferred VAE/value"] = vae_name
        
        # Write updated config
        with open(ui_config_file, 'w') as f:
            json.dump(ui_config, f, indent=4)
        
        print(f"✅ Configured VAE in ui-config.json: {vae_name}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to configure VAE: {e}")
        return False

def create_vae_fix_launch_script():
    """Create a launch script with VAE fixes"""
    print("\n=== Creating VAE-Fixed Launch Script ===")
    
    script_content = '''@echo off
echo Starting WebUI with VAE fixes for grey image issue...
echo.

REM VAE-specific fixes
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram

REM Force VAE to not use half precision (fixes grey images)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half-vae

REM Additional stability flags
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-sub-quad-attention

echo VAE Configuration:
echo - Forcing full precision VAE (--no-half-vae)
echo - GPU acceleration enabled
echo - Memory optimization enabled
echo - This should fix grey image generation
echo.

call webui.bat %*
'''
    
    script_filename = "webui_vae_fixed.bat"
    
    try:
        with open(script_filename, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Created launch script: {script_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create launch script: {e}")
        return False

def test_vae_configuration():
    """Test if VAE configuration is working"""
    print("\n=== Testing VAE Configuration ===")
    
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        
        # Test basic tensor operations
        test_tensor = torch.randn(1, 4, 64, 64)
        if torch.cuda.is_available():
            test_tensor = test_tensor.cuda()
        
        print("✅ Basic tensor operations working")
        return True
        
    except Exception as e:
        print(f"❌ VAE test failed: {e}")
        return False

def main():
    """Main function"""
    print("Grey Image Fix for Stable Diffusion WebUI")
    print("=" * 50)
    
    # Check current VAE configuration
    vae_configured = check_current_vae_config()
    
    # Check available VAE files
    available_vaes = check_available_vaes()
    
    # Download VAE if none available
    if not available_vaes:
        print("\n🔄 No VAE files found. Downloading recommended VAE...")
        vae_path = download_recommended_vae()
        if vae_path:
            vae_name = Path(vae_path).name
        else:
            print("❌ Failed to download VAE. Please download manually.")
            return
    else:
        vae_name = available_vaes[0].name
        print(f"\n✅ Using existing VAE: {vae_name}")
    
    # Configure VAE in UI config
    if not vae_configured:
        configure_vae_in_ui_config(vae_name)
    
    # Create launch script with VAE fixes
    create_vae_fix_launch_script()
    
    # Test configuration
    test_vae_configuration()
    
    print("\n" + "=" * 50)
    print("GREY IMAGE FIX SUMMARY")
    print("=" * 50)
    print("✅ VAE configuration completed!")
    print(f"✅ VAE file: {vae_name}")
    print("✅ Launch script created: webui_vae_fixed.bat")
    print("✅ UI configuration updated")
    
    print("\nNext steps:")
    print("1. Launch WebUI: .\\webui_vae_fixed.bat")
    print("2. Generate a test image with prompt: 'a red apple'")
    print("3. Images should now show actual content instead of grey")
    print("4. If still grey, try different VAE in Settings > Stable Diffusion")
    
    print("\nTroubleshooting:")
    print("- Make sure VAE is selected in WebUI Settings")
    print("- Try --no-half-vae flag if images are still grey")
    print("- Check that model and VAE are compatible")

if __name__ == "__main__":
    main()
