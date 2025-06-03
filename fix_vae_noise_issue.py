#!/usr/bin/env python3
"""
Fix VAE Noise/Static Issue
==========================

This script addresses the issue where VAE loads successfully but produces
colorful noise/static instead of proper images. This typically indicates:
1. VAE/Model compatibility issues
2. Precision/dtype mismatches
3. Incorrect VAE scaling factors
4. Model-specific VAE requirements

Author: Augment Agent
Date: January 2025
"""

import sys
import os
import json
import requests
from pathlib import Path

def analyze_model_vae_compatibility():
    """Analyze if the current model and VAE are compatible"""
    print("=== Analyzing Model-VAE Compatibility ===")
    
    model_path = "models/Stable-diffusion/NSFW_master.safetensors"
    current_vae = "models/VAE/vae-ft-ema-560000-ema-pruned.safetensors"
    
    print(f"Model: {model_path}")
    print(f"Current VAE: {current_vae}")
    
    # Check model file size to determine likely architecture
    if os.path.exists(model_path):
        model_size_gb = os.path.getsize(model_path) / (1024**3)
        print(f"Model size: {model_size_gb:.1f} GB")
        
        if model_size_gb < 3:
            print("✅ Likely SD 1.5 model - should work with standard VAE")
            return "sd15"
        elif model_size_gb < 8:
            print("⚠️  Likely SD 2.x model - may need specific VAE")
            return "sd2"
        else:
            print("⚠️  Likely SDXL model - needs SDXL VAE")
            return "sdxl"
    else:
        print("❌ Model file not found")
        return "unknown"

def download_model_specific_vaes():
    """Download VAEs that are more likely to work with various model types"""
    print("\n=== Downloading Model-Specific VAEs ===")
    
    vaes_to_download = [
        {
            "name": "vae-ft-mse-840000-ema-pruned.ckpt",
            "url": "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.ckpt",
            "description": "SD 1.5 VAE (ckpt format - sometimes more compatible)"
        },
        {
            "name": "kl-f8-anime2.ckpt", 
            "url": "https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/vae/kl-f8-anime2.ckpt",
            "description": "Anime/NSFW optimized VAE (often works better with custom models)"
        }
    ]
    
    downloaded_vaes = []
    
    for vae_info in vaes_to_download:
        vae_path = Path("models/VAE") / vae_info["name"]
        
        if vae_path.exists():
            print(f"✅ {vae_info['name']} already exists")
            downloaded_vaes.append(vae_info["name"])
            continue
        
        try:
            print(f"Downloading {vae_info['name']} - {vae_info['description']}")
            response = requests.get(vae_info["url"], stream=True)
            response.raise_for_status()
            
            with open(vae_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"✅ Downloaded {vae_info['name']}")
            downloaded_vaes.append(vae_info["name"])
            
        except Exception as e:
            print(f"❌ Failed to download {vae_info['name']}: {e}")
    
    return downloaded_vaes

def create_precision_test_scripts():
    """Create launch scripts with different precision settings"""
    print("\n=== Creating Precision Test Scripts ===")
    
    scripts = {
        "webui_vae_test_fp32.bat": {
            "description": "Full FP32 precision test",
            "args": "--precision full --no-half --no-half-vae --disable-nan-check"
        },
        "webui_vae_test_autocast.bat": {
            "description": "Autocast precision test", 
            "args": "--precision autocast --no-half-vae --disable-nan-check"
        },
        "webui_vae_test_anime.bat": {
            "description": "Anime VAE test",
            "args": "--precision autocast --no-half-vae --vae-path \"models/VAE/kl-f8-anime2.ckpt\""
        },
        "webui_vae_test_ckpt.bat": {
            "description": "CKPT VAE format test",
            "args": "--precision autocast --no-half-vae --vae-path \"models/VAE/vae-ft-mse-840000-ema-pruned.ckpt\""
        }
    }
    
    base_script = '''@echo off
echo {description}
echo ========================
echo.

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention --medvram

REM Precision-specific arguments
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% {args}

echo Configuration: {description}
echo Arguments: {args}
echo.
echo Expected: Should fix noise/static issues
echo.

call webui.bat %*
'''
    
    created_scripts = []
    
    for script_name, config in scripts.items():
        try:
            script_content = base_script.format(
                description=config["description"],
                args=config["args"]
            )
            
            with open(script_name, 'w') as f:
                f.write(script_content)
            
            print(f"✅ Created {script_name}")
            created_scripts.append(script_name)
            
        except Exception as e:
            print(f"❌ Failed to create {script_name}: {e}")
    
    return created_scripts

def create_generation_test_script():
    """Create a script to test different generation parameters"""
    print("\n=== Creating Generation Test Guide ===")
    
    test_guide = '''# VAE Noise/Static Troubleshooting Guide
==========================================

## Test Generation Parameters

### Test 1: Basic Settings
- Prompt: "a red apple"
- Steps: 20
- CFG Scale: 7.0
- Size: 512x512
- Sampler: DPM++ 2M Karras

### Test 2: Conservative Settings  
- Prompt: "a simple house"
- Steps: 15
- CFG Scale: 5.0
- Size: 256x256
- Sampler: Euler a

### Test 3: Different Samplers
Try these samplers in order:
1. Euler a
2. DPM++ 2M Karras  
3. DDIM
4. LMS

### Test 4: VAE Testing Order
1. Launch: webui_vae_test_anime.bat
2. Launch: webui_vae_test_ckpt.bat
3. Launch: webui_vae_test_fp32.bat
4. Launch: webui_vae_test_autocast.bat

## Expected Results
- Anime VAE: Often fixes NSFW/custom model issues
- CKPT format: Sometimes more compatible than safetensors
- FP32: Maximum precision, slower but most compatible
- Autocast: Good balance of speed and compatibility

## If Still Getting Noise:
1. Try different model (download a standard SD 1.5 model)
2. Check if model file is corrupted
3. Try CPU-only mode: --use-cpu all
4. Check WebUI console for error messages

## Model Compatibility Notes:
- NSFW models often need anime-optimized VAEs
- Custom merged models may have VAE baked in
- Some models are incompatible with standard VAEs
'''
    
    try:
        with open("VAE_Troubleshooting_Guide.md", 'w') as f:
            f.write(test_guide)
        print("✅ Created VAE_Troubleshooting_Guide.md")
        return True
    except Exception as e:
        print(f"❌ Failed to create guide: {e}")
        return False

def check_model_embedded_vae():
    """Check if the model has an embedded VAE that might be conflicting"""
    print("\n=== Checking for Model Embedded VAE ===")
    
    try:
        import safetensors.torch
        model_path = "models/Stable-diffusion/NSFW_master.safetensors"
        
        if not os.path.exists(model_path):
            print("❌ Model file not found")
            return False
        
        print("Loading model metadata...")
        # Load just the metadata without loading the full model
        with safetensors.torch.safe_open(model_path, framework="pt") as f:
            keys = list(f.keys())
        
        # Check for VAE keys in the model
        vae_keys = [k for k in keys if any(vae_term in k.lower() for vae_term in ['vae', 'first_stage', 'decoder', 'encoder'])]
        
        if vae_keys:
            print(f"⚠️  Model contains {len(vae_keys)} VAE-related parameters")
            print("This model likely has an embedded VAE that may conflict with external VAE")
            print("Recommendation: Try without specifying external VAE")
            return True
        else:
            print("✅ Model does not appear to have embedded VAE")
            print("External VAE should work fine")
            return False
            
    except Exception as e:
        print(f"❌ Error checking model: {e}")
        return False

def main():
    """Main diagnostic and fix function"""
    print("VAE Noise/Static Issue Fix")
    print("=" * 50)
    
    # Analyze model compatibility
    model_type = analyze_model_vae_compatibility()
    
    # Check for embedded VAE
    has_embedded_vae = check_model_embedded_vae()
    
    # Download alternative VAEs
    downloaded_vaes = download_model_specific_vaes()
    
    # Create test scripts
    test_scripts = create_precision_test_scripts()
    
    # Create troubleshooting guide
    guide_created = create_generation_test_script()
    
    print("\n" + "=" * 50)
    print("VAE NOISE/STATIC FIX SUMMARY")
    print("=" * 50)
    
    print("🔍 DIAGNOSIS:")
    if has_embedded_vae:
        print("⚠️  Model likely has embedded VAE - this may be causing conflicts")
        print("🔧 RECOMMENDED FIX: Try launching without --vae-path argument")
    else:
        print("✅ Model appears to need external VAE")
        print("🔧 RECOMMENDED FIX: Try anime-optimized VAE")
    
    print(f"\n📁 Downloaded VAEs: {len(downloaded_vaes)}")
    for vae in downloaded_vaes:
        print(f"  - {vae}")
    
    print(f"\n🧪 Test Scripts Created: {len(test_scripts)}")
    for script in test_scripts:
        print(f"  - {script}")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Stop current WebUI (Ctrl+C)")
    
    if has_embedded_vae:
        print("2. Try: webui_vae_test_autocast.bat (no external VAE)")
        print("3. If still noise, try: webui_vae_test_anime.bat")
    else:
        print("2. Try: webui_vae_test_anime.bat (anime VAE)")
        print("3. If still noise, try: webui_vae_test_ckpt.bat")
    
    print("4. Test with simple prompt: 'a red apple'")
    print("5. Check VAE_Troubleshooting_Guide.md for detailed steps")
    
    print("\n⚠️  IMPORTANT:")
    print("- Colorful noise = VAE loading but wrong format/precision")
    print("- Try different VAE files if noise persists")
    print("- Some NSFW models need specific VAEs")
    print("- Check console for VAE loading messages")

if __name__ == "__main__":
    main()
