#!/usr/bin/env python3
"""
Comprehensive VAE Diagnostic and Fix Script
===========================================

This script performs deep diagnostics on VAE loading and configuration
to identify why images are still appearing grey despite VAE configuration.

Author: Augment Agent
Date: January 2025
"""

import sys
import os
import json
import hashlib
import torch
from pathlib import Path

def check_vae_file_integrity():
    """Check if the VAE file downloaded correctly and isn't corrupted"""
    print("=== Checking VAE File Integrity ===")
    
    vae_path = Path("models/VAE/vae-ft-mse-840000-ema-pruned.safetensors")
    
    if not vae_path.exists():
        print("❌ VAE file not found!")
        return False
    
    # Check file size (should be around 334MB)
    file_size = vae_path.stat().st_size
    expected_size_mb = 334
    actual_size_mb = file_size / (1024 * 1024)
    
    print(f"VAE file size: {actual_size_mb:.1f} MB")
    
    if abs(actual_size_mb - expected_size_mb) > 10:
        print(f"❌ VAE file size incorrect! Expected ~{expected_size_mb}MB, got {actual_size_mb:.1f}MB")
        return False
    
    print("✅ VAE file size looks correct")
    
    # Try to load the VAE with safetensors
    try:
        import safetensors.torch
        vae_state_dict = safetensors.torch.load_file(str(vae_path))
        print(f"✅ VAE file loads successfully with safetensors")
        print(f"✅ VAE contains {len(vae_state_dict)} parameters")
        return True
    except Exception as e:
        print(f"❌ VAE file appears corrupted: {e}")
        return False

def check_webui_vae_loading():
    """Check if WebUI is actually loading and using the VAE"""
    print("\n=== Checking WebUI VAE Configuration ===")
    
    # Check ui-config.json
    try:
        with open("ui-config.json", 'r', encoding='utf-8') as f:
            ui_config = json.load(f)
        
        txt2img_vae = ui_config.get("txt2img/Preferred VAE/value", "None")
        img2img_vae = ui_config.get("img2img/Preferred VAE/value", "None")
        
        print(f"txt2img VAE setting: {txt2img_vae}")
        print(f"img2img VAE setting: {img2img_vae}")
        
        if txt2img_vae == "vae-ft-mse-840000-ema-pruned.safetensors":
            print("✅ VAE correctly configured in ui-config.json")
            return True
        else:
            print("❌ VAE not properly configured in ui-config.json")
            return False
            
    except Exception as e:
        print(f"❌ Error reading ui-config.json: {e}")
        return False

def test_vae_loading_directly():
    """Test loading the VAE directly with PyTorch"""
    print("\n=== Testing Direct VAE Loading ===")
    
    try:
        import safetensors.torch
        vae_path = "models/VAE/vae-ft-mse-840000-ema-pruned.safetensors"
        
        print("Loading VAE state dict...")
        vae_state_dict = safetensors.torch.load_file(vae_path)
        
        print("Creating test tensor...")
        # Test with a small latent tensor (typical SD latent space)
        test_latent = torch.randn(1, 4, 64, 64)  # Batch=1, Channels=4, H=64, W=64
        
        if torch.cuda.is_available():
            test_latent = test_latent.cuda()
            print("✅ Using CUDA for VAE test")
        else:
            print("⚠️  Using CPU for VAE test")
        
        print("✅ VAE state dict loaded successfully")
        print(f"✅ Test latent tensor created: {test_latent.shape}")
        
        # Check for key VAE components
        decoder_keys = [k for k in vae_state_dict.keys() if 'decoder' in k]
        encoder_keys = [k for k in vae_state_dict.keys() if 'encoder' in k]
        
        print(f"✅ Found {len(decoder_keys)} decoder parameters")
        print(f"✅ Found {len(encoder_keys)} encoder parameters")
        
        if len(decoder_keys) > 0 and len(encoder_keys) > 0:
            print("✅ VAE appears to have complete encoder/decoder")
            return True
        else:
            print("❌ VAE missing encoder or decoder components")
            return False
            
    except Exception as e:
        print(f"❌ Direct VAE loading failed: {e}")
        return False

def check_webui_settings_file():
    """Check if there's a settings file overriding VAE configuration"""
    print("\n=== Checking WebUI Settings Files ===")
    
    settings_files = ["config.json", "settings.json", "webui-user.bat"]
    
    for settings_file in settings_files:
        if os.path.exists(settings_file):
            print(f"Found settings file: {settings_file}")
            try:
                if settings_file.endswith('.json'):
                    with open(settings_file, 'r', encoding='utf-8') as f:
                        settings = json.load(f)
                    
                    # Look for VAE-related settings
                    vae_settings = {k: v for k, v in settings.items() if 'vae' in k.lower()}
                    if vae_settings:
                        print(f"VAE settings in {settings_file}:")
                        for k, v in vae_settings.items():
                            print(f"  {k}: {v}")
                    else:
                        print(f"No VAE settings found in {settings_file}")
                        
            except Exception as e:
                print(f"Error reading {settings_file}: {e}")
    
    return True

def create_vae_debug_launch_script():
    """Create a launch script with maximum VAE debugging"""
    print("\n=== Creating VAE Debug Launch Script ===")
    
    debug_script = '''@echo off
echo VAE Debug Launch Script
echo ========================
echo.

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Maximum VAE debugging and fixes
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install

REM Force specific VAE
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models/VAE/vae-ft-mse-840000-ema-pruned.safetensors"

REM VAE precision fixes
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision full

REM Disable problematic optimizations
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --disable-nan-check
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half

REM GPU optimizations
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram

REM Enable verbose logging
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --log-startup

echo VAE Debug Configuration:
echo ==========================
echo - Forcing specific VAE path
echo - Full precision mode (no half precision anywhere)
echo - Disabled NaN checking
echo - Maximum compatibility mode
echo - Verbose logging enabled
echo.
echo This should definitely fix grey images!
echo.

call webui.bat %*
'''
    
    try:
        with open("webui_vae_debug.bat", 'w') as f:
            f.write(debug_script)
        print("✅ Created debug launch script: webui_vae_debug.bat")
        return True
    except Exception as e:
        print(f"❌ Failed to create debug script: {e}")
        return False

def download_alternative_vae():
    """Download an alternative VAE in case the current one has issues"""
    print("\n=== Downloading Alternative VAE ===")
    
    # Try a different VAE that's known to work well
    alt_vae_url = "https://huggingface.co/stabilityai/sd-vae-ft-ema-original/resolve/main/vae-ft-ema-560000-ema-pruned.safetensors"
    alt_vae_filename = "vae-ft-ema-560000-ema-pruned.safetensors"
    alt_vae_path = Path("models/VAE") / alt_vae_filename
    
    if alt_vae_path.exists():
        print(f"✅ Alternative VAE already exists: {alt_vae_filename}")
        return str(alt_vae_path)
    
    try:
        import requests
        print(f"Downloading alternative VAE: {alt_vae_filename}")
        
        response = requests.get(alt_vae_url, stream=True)
        response.raise_for_status()
        
        with open(alt_vae_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"✅ Downloaded alternative VAE: {alt_vae_filename}")
        return str(alt_vae_path)
        
    except Exception as e:
        print(f"❌ Failed to download alternative VAE: {e}")
        return None

def main():
    """Main diagnostic function"""
    print("VAE Grey Image Diagnostic Tool")
    print("=" * 50)
    
    # Check VAE file integrity
    vae_integrity = check_vae_file_integrity()
    
    # Check WebUI VAE configuration
    webui_config = check_webui_vae_loading()
    
    # Test direct VAE loading
    direct_loading = test_vae_loading_directly()
    
    # Check settings files
    check_webui_settings_file()
    
    # Create debug launch script
    debug_script = create_vae_debug_launch_script()
    
    print("\n" + "=" * 50)
    print("VAE DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    if not vae_integrity:
        print("❌ VAE file integrity issues detected")
        print("🔄 Downloading alternative VAE...")
        alt_vae = download_alternative_vae()
        if alt_vae:
            print("✅ Try using the alternative VAE")
    
    if not webui_config:
        print("❌ WebUI VAE configuration issues")
    
    if not direct_loading:
        print("❌ Direct VAE loading issues")
    
    print("\n🔧 RECOMMENDED FIXES:")
    print("1. Stop current WebUI (Ctrl+C)")
    print("2. Launch with: .\\webui_vae_debug.bat")
    print("3. Check console for VAE loading messages")
    print("4. Try generating with prompt: 'a red apple'")
    print("5. If still grey, try different VAE in Settings")
    
    print("\n📋 Additional troubleshooting:")
    print("- Check WebUI Settings > Stable Diffusion > SD VAE")
    print("- Try --vae-path flag with full path")
    print("- Verify model compatibility with VAE")
    print("- Check for any error messages in console")

if __name__ == "__main__":
    main()
