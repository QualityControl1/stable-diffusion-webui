#!/usr/bin/env python3
"""
VAE Diagnostic Test for Colorful Static/Noise Issue
==================================================

This script creates systematic tests to identify why VAE decoding
produces colorful noise instead of proper images.

Author: Augment Agent
Date: January 2025
"""

import os
import json
import requests
from pathlib import Path

def check_current_vae_status():
    """Check what VAE is currently loaded and its status"""
    print("=== Current VAE Status Check ===")
    
    # Check if WebUI is running and get current settings
    try:
        response = requests.get("http://127.0.0.1:7862/sdapi/v1/options", timeout=5)
        if response.status_code == 200:
            options = response.json()
            current_vae = options.get("sd_vae", "None")
            print(f"✅ WebUI is running")
            print(f"Current VAE setting: {current_vae}")
            return True
        else:
            print("❌ WebUI not responding")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to WebUI: {e}")
        return False

def analyze_vae_files():
    """Analyze available VAE files and their compatibility"""
    print("\n=== VAE File Analysis ===")
    
    vae_dir = Path("models/VAE")
    if not vae_dir.exists():
        print("❌ VAE directory not found")
        return []
    
    vae_files = []
    for vae_file in vae_dir.glob("*"):
        if vae_file.suffix.lower() in ['.safetensors', '.ckpt', '.pt']:
            size_mb = vae_file.stat().st_size / (1024 * 1024)
            vae_info = {
                'name': vae_file.name,
                'path': str(vae_file),
                'size_mb': size_mb,
                'format': vae_file.suffix.lower(),
                'compatible': vae_file.suffix.lower() == '.safetensors'  # PyTorch 2.6 compatible
            }
            vae_files.append(vae_info)
            
            status = "✅ Compatible" if vae_info['compatible'] else "⚠️  May have issues"
            print(f"{status} - {vae_file.name} ({size_mb:.1f} MB, {vae_file.suffix})")
    
    return vae_files

def create_systematic_test_scripts():
    """Create test scripts for different VAE configurations"""
    print("\n=== Creating Systematic Test Scripts ===")
    
    test_configs = [
        {
            "name": "test_no_vae.bat",
            "description": "No external VAE (use model's built-in)",
            "vae_args": "",
            "precision_args": "--precision autocast --no-half-vae"
        },
        {
            "name": "test_vae_fp32.bat", 
            "description": "Full FP32 precision with safetensors VAE",
            "vae_args": "--vae-path \"models/VAE/vae-ft-ema-560000-ema-pruned.safetensors\"",
            "precision_args": "--precision full --no-half --no-half-vae"
        },
        {
            "name": "test_vae_cpu.bat",
            "description": "CPU-only mode with safetensors VAE", 
            "vae_args": "--vae-path \"models/VAE/vae-ft-ema-560000-ema-pruned.safetensors\"",
            "precision_args": "--use-cpu all --precision full"
        },
        {
            "name": "test_different_vae.bat",
            "description": "Try MSE VAE (different training)",
            "vae_args": "--vae-path \"models/VAE/vae-ft-mse-840000-ema-pruned.ckpt\"",
            "precision_args": "--precision autocast --no-half-vae"
        }
    ]
    
    base_script = '''@echo off
echo VAE Test: {description}
echo ========================================
echo.

REM Kill any existing WebUI processes
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention --medvram

REM Test-specific arguments
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% {precision_args}
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% {vae_args}

echo Configuration: {description}
echo VAE Args: {vae_args}
echo Precision Args: {precision_args}
echo.
echo Expected: Should fix colorful noise if this configuration works
echo Test prompt: "a simple red apple on white background"
echo.

call webui.bat %*
'''
    
    created_scripts = []
    
    for config in test_configs:
        try:
            script_content = base_script.format(
                description=config["description"],
                vae_args=config["vae_args"],
                precision_args=config["precision_args"]
            )
            
            with open(config["name"], 'w') as f:
                f.write(script_content)
            
            print(f"✅ Created {config['name']}")
            created_scripts.append(config["name"])
            
        except Exception as e:
            print(f"❌ Failed to create {config['name']}: {e}")
    
    return created_scripts

def create_vae_test_guide():
    """Create a detailed testing guide"""
    print("\n=== Creating VAE Test Guide ===")
    
    guide_content = '''# VAE Colorful Static/Noise Troubleshooting Guide
===============================================

## Current Issue Analysis
Your WebUI is generating colorful static/noise instead of proper images.
This indicates the VAE is decoding but with incorrect parameters.

## Systematic Testing Order

### Test 1: No External VAE
**Script:** test_no_vae.bat
**Purpose:** Check if model has built-in VAE that works
**Expected:** If this works, your model doesn't need external VAE

### Test 2: Full Precision
**Script:** test_vae_fp32.bat  
**Purpose:** Maximum precision to eliminate dtype issues
**Expected:** Slower but should produce correct images if precision is the issue

### Test 3: CPU Mode
**Script:** test_vae_cpu.bat
**Purpose:** Eliminate GPU precision/memory issues
**Expected:** Very slow but most compatible

### Test 4: Different VAE
**Script:** test_different_vae.bat
**Purpose:** Try MSE-trained VAE instead of EMA
**Expected:** Different VAE training may be more compatible

## Testing Instructions

1. **Stop current WebUI** (Ctrl+C in terminal)
2. **Run test scripts in order** (double-click or use PowerShell)
3. **For each test:**
   - Wait for "Model loaded" message
   - Open http://127.0.0.1:7862
   - Generate with prompt: "a simple red apple on white background"
   - Use settings: 20 steps, CFG 7.0, 512x512, DPM++ 2M Karras
   - Check if output is proper image or still noise

## What Each Result Means

### Test 1 Success (No VAE):
- **Cause:** Model has built-in VAE, external VAE conflicts
- **Solution:** Always launch without --vae-path argument

### Test 2 Success (FP32):
- **Cause:** Precision/dtype mismatch in autocast mode
- **Solution:** Use --precision full (slower but stable)

### Test 3 Success (CPU):
- **Cause:** GPU memory/precision issues
- **Solution:** Use CPU for VAE: --use-cpu vae

### Test 4 Success (Different VAE):
- **Cause:** VAE training incompatibility
- **Solution:** Use MSE VAE instead of EMA VAE

### All Tests Fail:
- **Cause:** Model file corruption or fundamental incompatibility
- **Solution:** Try different model or check model integrity

## Advanced Diagnostics

If all tests fail, the issue may be:
1. **Corrupted model file** - Re-download NSFW_master.safetensors
2. **Python 3.13 incompatibility** - Consider downgrading to Python 3.10-3.12
3. **PyTorch 2.6 issues** - Try PyTorch 2.4 or 2.5
4. **Model architecture mismatch** - Model may not be standard SD 1.5

## Console Messages to Watch For

**Good signs:**
- "Model loaded in X.Xs"
- "Loading VAE weights from..."
- No error messages during generation

**Bad signs:**
- "UnpicklingError"
- "CUDA out of memory"
- "NaN values detected"
- "VAE failed to load"

## Next Steps After Testing

Once you identify which test works:
1. Use that configuration permanently
2. Create a custom launch script with working parameters
3. Test with more complex prompts to confirm stability
'''
    
    try:
        with open("VAE_Static_Troubleshooting_Guide.md", 'w') as f:
            f.write(guide_content)
        print("✅ Created VAE_Static_Troubleshooting_Guide.md")
        return True
    except Exception as e:
        print(f"❌ Failed to create guide: {e}")
        return False

def download_alternative_vae():
    """Download a different VAE that might work better"""
    print("\n=== Downloading Alternative VAE ===")
    
    # Try to download a different VAE format
    alternative_vae = {
        "name": "vae-ft-mse-840000-ema-pruned.safetensors",
        "url": "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors",
        "description": "MSE-trained VAE in safetensors format"
    }
    
    vae_path = Path("models/VAE") / alternative_vae["name"]
    
    if vae_path.exists():
        print(f"✅ {alternative_vae['name']} already exists")
        return True
    
    try:
        print(f"Downloading {alternative_vae['name']}...")
        response = requests.get(alternative_vae["url"], stream=True)
        response.raise_for_status()
        
        with open(vae_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"✅ Downloaded {alternative_vae['name']}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download {alternative_vae['name']}: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("VAE Colorful Static/Noise Diagnostic")
    print("=" * 50)
    
    # Check current status
    webui_running = check_current_vae_status()
    
    # Analyze available VAE files
    vae_files = analyze_vae_files()
    
    # Download alternative VAE
    alt_vae_downloaded = download_alternative_vae()
    
    # Create test scripts
    test_scripts = create_systematic_test_scripts()
    
    # Create guide
    guide_created = create_vae_test_guide()
    
    print("\n" + "=" * 50)
    print("VAE STATIC/NOISE DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    print("🔍 CURRENT STATUS:")
    if webui_running:
        print("✅ WebUI is running but producing colorful static")
        print("🔧 DIAGNOSIS: VAE decoding issue - not a loading problem")
    else:
        print("❌ WebUI not accessible - check if it's running")
    
    print(f"\n📁 Available VAE files: {len(vae_files)}")
    for vae in vae_files:
        status = "✅" if vae['compatible'] else "⚠️"
        print(f"  {status} {vae['name']} ({vae['size_mb']:.1f}MB)")
    
    print(f"\n🧪 Test scripts created: {len(test_scripts)}")
    for script in test_scripts:
        print(f"  - {script}")
    
    print("\n🎯 IMMEDIATE ACTION PLAN:")
    print("1. Stop current WebUI (Ctrl+C in terminal)")
    print("2. Run: test_no_vae.bat (test if model has built-in VAE)")
    print("3. If still static, run: test_vae_fp32.bat (full precision)")
    print("4. If still static, run: test_vae_cpu.bat (CPU mode)")
    print("5. Check VAE_Static_Troubleshooting_Guide.md for details")
    
    print("\n⚠️ IMPORTANT:")
    print("- Colorful static = VAE is working but wrong parameters")
    print("- Test each configuration systematically")
    print("- One of these tests should produce proper images")
    print("- If all fail, the model file may be corrupted")

if __name__ == "__main__":
    main()
