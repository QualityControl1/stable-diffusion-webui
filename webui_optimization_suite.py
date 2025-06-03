#!/usr/bin/env python3
"""
Stable Diffusion WebUI Optimization Suite
=========================================

Comprehensive optimization tools for image quality, speed, and workflow
improvements in stable-diffusion-webui with Python 3.13/PyTorch 2.6.

Author: Augment Agent
Date: January 2025
"""

import os
import json
from pathlib import Path

def create_optimized_config():
    """Create optimized config.json for WebUI"""
    print("=== Creating Optimized WebUI Configuration ===")
    
    # Optimized settings for RTX 3080 Laptop (16GB VRAM)
    optimized_config = {
        "samples_save": True,
        "samples_format": "png",
        "samples_filename_pattern": "[seed]-[model_name]-[prompt_spaces]",
        "save_images_add_number": True,
        "grid_save": True,
        "grid_format": "png",
        "grid_extended_filename": True,
        "grid_only_if_multiple": True,
        "grid_prevent_empty_spots": False,
        "n_rows": -1,
        "enable_pnginfo": True,
        "save_txt": False,
        "save_images_before_face_restoration": False,
        "save_images_before_highres_fix": False,
        "save_images_before_color_correction": False,
        "jpeg_quality": 80,
        "webp_lossless": False,
        "export_for_4chan": True,
        "img_downscale_threshold": 4.0,
        "target_side_length": 4000,
        "img_max_size_mp": 200,
        "use_original_name_batch": True,
        "use_upscaler_name_as_suffix": False,
        "save_selected_only": True,
        "do_not_add_watermark": False,
        "temp_dir": "",
        "clean_temp_dir_at_start": False,
        
        # Performance optimizations for RTX 3080
        "cross_attention_optimization": "Doggettx",
        "s_min_uncond": 0.0,
        "token_merging_ratio": 0.0,
        "token_merging_ratio_img2img": 0.0,
        "token_merging_ratio_hr": 0.0,
        "pad_cond_uncond": False,
        "experimental_persistent_cond_cache": True,
        
        # Quality settings
        "CLIP_stop_at_last_layers": 1,
        "upcast_attn": False,
        "randn_source": "GPU",
        "font": "",
        "js_modal_lightbox": True,
        "js_modal_lightbox_initially_zoomed": True,
        "show_progress_bar": True,
        "live_previews_enable": True,
        "show_progress_grid": True,
        "show_progress_every_n_steps": 10,
        "show_progress_type": "Approx NN",
        "live_preview_content": "Prompt",
        "live_preview_refresh_period": 1000,
        
        # Memory optimization
        "memmon_poll_rate": 8,
        "samples_log_stdout": False,
        "multiple_tqdm": True,
        "print_hypernet_extra": False,
        "unload_models_when_training": False,
        "pin_memory": False,
        "save_optimizer_state": False,
        "save_training_settings_to_txt": True,
        "dataset_filename_word_regex": "",
        "dataset_filename_join_string": " ",
        "training_image_repeats_per_epoch": 1,
        "training_write_csv_every": 500,
        "training_xattention_optimizations": False,
        "training_enable_tensorboard": False,
        "training_tensorboard_save_images": False,
        "training_tensorboard_flush_every": 120,
        
        # Advanced settings
        "sd_model_checkpoint": "v1-5-pruned-emaonly.safetensors",
        "sd_vae": "vae-ft-ema-560000-ema-pruned.safetensors",
        "sd_vae_as_default": True,
        "inpainting_mask_weight": 1.0,
        "initial_noise_multiplier": 1.0,
        "img2img_color_correction": False,
        "img2img_fix_steps": False,
        "img2img_background_color": "#ffffff",
        "enable_quantization": False,
        "enable_emphasis": True,
        "enable_batch_seeds": True,
        "comma_padding_backtrack": 20,
        "CLIP_stop_at_last_layers": 1,
        
        # Sampling defaults
        "eta_ddim": 0.0,
        "eta_ancestral": 1.0,
        "ddim_discretize": "uniform",
        "s_churn": 0.0,
        "s_tmin": 0.0,
        "s_noise": 1.0,
        "eta_noise_seed_delta": 0,
        "always_discard_next_to_last_sigma": False,
        "uni_pc_variant": "bh1",
        "uni_pc_skip_type": "time_uniform",
        "uni_pc_order": 3,
        "uni_pc_lower_order_final": True
    }
    
    config_path = Path("config.json")
    try:
        with open(config_path, 'w') as f:
            json.dump(optimized_config, f, indent=2)
        print(f"✅ Created optimized config.json")
        return True
    except Exception as e:
        print(f"❌ Failed to create config: {e}")
        return False

def create_quality_presets():
    """Create quality preset configurations"""
    print("\n=== Creating Quality Presets ===")
    
    presets = {
        "ultra_quality": {
            "name": "Ultra Quality",
            "description": "Maximum quality for final renders",
            "steps": 30,
            "cfg_scale": 7.5,
            "sampler": "DPM++ 2M Karras",
            "width": 768,
            "height": 768,
            "batch_size": 1,
            "batch_count": 1,
            "seed": -1,
            "restore_faces": False,
            "tiling": False,
            "enable_hr": True,
            "hr_scale": 1.5,
            "hr_upscaler": "R-ESRGAN 4x+",
            "hr_second_pass_steps": 15,
            "denoising_strength": 0.5
        },
        "balanced": {
            "name": "Balanced Quality/Speed",
            "description": "Good quality with reasonable speed",
            "steps": 20,
            "cfg_scale": 7.0,
            "sampler": "DPM++ 2M Karras",
            "width": 512,
            "height": 512,
            "batch_size": 1,
            "batch_count": 4,
            "seed": -1,
            "restore_faces": False,
            "tiling": False,
            "enable_hr": False
        },
        "fast_preview": {
            "name": "Fast Preview",
            "description": "Quick generation for testing prompts",
            "steps": 15,
            "cfg_scale": 6.0,
            "sampler": "Euler a",
            "width": 512,
            "height": 512,
            "batch_size": 1,
            "batch_count": 1,
            "seed": -1,
            "restore_faces": False,
            "tiling": False,
            "enable_hr": False
        },
        "batch_generation": {
            "name": "Batch Generation",
            "description": "Optimized for generating multiple variations",
            "steps": 25,
            "cfg_scale": 7.0,
            "sampler": "DPM++ 2M Karras",
            "width": 512,
            "height": 512,
            "batch_size": 4,
            "batch_count": 2,
            "seed": -1,
            "restore_faces": False,
            "tiling": False,
            "enable_hr": False
        }
    }
    
    presets_path = Path("quality_presets.json")
    try:
        with open(presets_path, 'w') as f:
            json.dump(presets, f, indent=2)
        print(f"✅ Created quality_presets.json")
        return True
    except Exception as e:
        print(f"❌ Failed to create presets: {e}")
        return False

def create_advanced_launcher():
    """Create advanced launcher with optimization flags"""
    print("\n=== Creating Advanced Launcher ===")
    
    launcher_script = '''@echo off
echo Stable Diffusion WebUI - Optimized for RTX 3080 Laptop
echo ======================================================
echo.

REM Kill any existing WebUI processes
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Advanced GPU environment variables for RTX 3080
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512,expandable_segments:True
set CUDA_LAUNCH_BLOCKING=0
set CUDA_CACHE_DISABLE=0
set CUDA_MODULE_LOADING=LAZY
set PYTORCH_NVFUSER_DISABLE_FALLBACK=1

REM Memory optimization
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set SAFETENSORS_FAST_GPU=1

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install

REM Performance optimizations for RTX 3080 (16GB VRAM)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --xformers --opt-split-attention-v1
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram-sdxl --opt-channelslast

REM Quality optimizations
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --upcast-sampling

REM Model and VAE
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --ckpt "models\\Stable-diffusion\\v1-5-pruned-emaonly.safetensors"
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models\\VAE\\vae-ft-ema-560000-ema-pruned.safetensors"

REM Advanced features
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --enable-insecure-extension-access
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --api --api-log

REM UI optimizations
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --gradio-queue --multiple

echo Configuration: Optimized for RTX 3080 Laptop (16GB VRAM)
echo Features: xFormers, optimized attention, upcast sampling
echo Quality: Maximum with performance balance
echo.

call webui.bat %*
'''
    
    try:
        with open("webui_optimized.bat", 'w') as f:
            f.write(launcher_script)
        print("✅ Created webui_optimized.bat")
        return True
    except Exception as e:
        print(f"❌ Failed to create launcher: {e}")
        return False

def create_prompt_engineering_guide():
    """Create comprehensive prompt engineering guide"""
    print("\n=== Creating Prompt Engineering Guide ===")
    
    guide_content = '''# Advanced Prompt Engineering Guide
=====================================

## 1. PROMPT STRUCTURE OPTIMIZATION

### Basic Structure:
```
[Subject] [Action/Pose] [Environment/Setting] [Style] [Quality Tags] [Technical Parameters]
```

### Example:
```
portrait of a beautiful woman, elegant pose, sitting in a garden, 
oil painting style, masterpiece, best quality, highly detailed, 
8k uhd, professional photography, soft lighting
```

## 2. QUALITY ENHANCEMENT TAGS

### Universal Quality Boosters:
- `masterpiece, best quality, highly detailed`
- `8k uhd, ultra high res, photorealistic`
- `professional photography, award winning`
- `sharp focus, perfect composition`
- `studio lighting, soft lighting, dramatic lighting`

### Art Style Specific:
- **Photography**: `dslr, bokeh, depth of field, professional lighting`
- **Digital Art**: `digital painting, concept art, trending on artstation`
- **Anime/Manga**: `anime style, manga style, cel shading`
- **Realistic**: `photorealistic, hyperrealistic, lifelike`

## 3. NEGATIVE PROMPT OPTIMIZATION

### Essential Negative Prompts:
```
lowres, bad anatomy, bad hands, text, error, missing fingers, 
extra digit, fewer digits, cropped, worst quality, low quality, 
normal quality, jpeg artifacts, signature, watermark, username, blurry
```

### Advanced Negative Prompts:
```
(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), 
text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, 
morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, 
deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, 
gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, 
too many fingers, long neck
```

## 4. WEIGHT AND EMPHASIS TECHNIQUES

### Emphasis Syntax:
- `(word)` - 1.1x emphasis
- `((word))` - 1.21x emphasis  
- `(word:1.3)` - 1.3x emphasis
- `[word]` - 0.9x de-emphasis
- `{word}` - Alternative emphasis (some UIs)

### Strategic Weighting:
```
(beautiful detailed eyes:1.2), (perfect face:1.1), [background:0.8], 
(masterpiece:1.3), (best quality:1.2)
```

## 5. COMPOSITION AND FRAMING

### Camera Angles:
- `close-up, medium shot, full body, wide shot`
- `low angle, high angle, bird's eye view, worm's eye view`
- `profile view, three-quarter view, front view, back view`

### Composition Rules:
- `rule of thirds, golden ratio, centered composition`
- `dynamic pose, static pose, action shot`
- `shallow depth of field, deep focus`

## 6. LIGHTING MASTERY

### Lighting Types:
- `soft lighting, hard lighting, dramatic lighting`
- `golden hour, blue hour, studio lighting`
- `rim lighting, backlighting, side lighting`
- `volumetric lighting, god rays, ambient lighting`

### Color Temperature:
- `warm lighting, cool lighting, neutral lighting`
- `cinematic lighting, moody lighting`

## 7. STYLE TRANSFER TECHNIQUES

### Artist References:
- `in the style of [artist name]`
- `[artist name] style painting`
- `inspired by [artist name]`

### Art Movement References:
- `impressionist style, baroque style, art nouveau`
- `cyberpunk style, steampunk aesthetic`
- `minimalist design, maximalist art`

## 8. TECHNICAL QUALITY PARAMETERS

### Resolution and Detail:
- `8k uhd, 4k, ultra high resolution`
- `highly detailed, intricate details, fine details`
- `sharp focus, crystal clear, pristine quality`

### Rendering Quality:
- `octane render, unreal engine, blender render`
- `ray tracing, global illumination`
- `subsurface scattering, ambient occlusion`

## 9. PROMPT OPTIMIZATION STRATEGIES

### A/B Testing Approach:
1. Start with basic prompt
2. Add quality tags systematically
3. Test different emphasis weights
4. Compare results and iterate

### Prompt Length Optimization:
- **Short prompts** (10-20 words): Better for simple concepts
- **Medium prompts** (20-50 words): Balanced detail and coherence
- **Long prompts** (50+ words): Maximum detail but may lose focus

### Keyword Density:
- Avoid repetition of similar concepts
- Use synonyms for variety
- Balance positive and negative prompts

## 10. ADVANCED TECHNIQUES

### Prompt Blending:
```
[landscape:portrait:0.3] - Blend landscape and portrait at 30% transition
```

### Attention Scheduling:
```
(detailed face:1.2) AND (beautiful eyes:1.3) - Multiple emphasis
```

### Conditional Prompting:
```
IF realistic THEN photorealistic ELSE artistic style
```

## 11. WORKFLOW OPTIMIZATION

### Iterative Refinement:
1. **Base prompt** - Core concept
2. **Quality pass** - Add quality tags
3. **Style pass** - Define artistic style
4. **Detail pass** - Add specific details
5. **Negative pass** - Refine negative prompts

### Seed Management:
- Use fixed seeds for consistent iterations
- Document successful seed/prompt combinations
- Create seed libraries for different styles

## 12. COMMON MISTAKES TO AVOID

### Over-prompting:
- Too many conflicting styles
- Excessive emphasis weights
- Redundant quality tags

### Under-specification:
- Vague subject descriptions
- Missing quality indicators
- Insufficient negative prompts

### Technical Issues:
- Conflicting art styles
- Impossible physical combinations
- Inconsistent lighting descriptions
'''
    
    try:
        with open("Advanced_Prompt_Engineering_Guide.md", 'w', encoding='utf-8') as f:
            f.write(guide_content)
        print("✅ Created Advanced_Prompt_Engineering_Guide.md")
        return True
    except Exception as e:
        print(f"❌ Failed to create guide: {e}")
        return False

def main():
    """Main optimization setup function"""
    print("Stable Diffusion WebUI Optimization Suite")
    print("=" * 50)
    
    # Create optimized configuration
    config_created = create_optimized_config()
    
    # Create quality presets
    presets_created = create_quality_presets()
    
    # Create advanced launcher
    launcher_created = create_advanced_launcher()
    
    # Create prompt engineering guide
    guide_created = create_prompt_engineering_guide()
    
    print("\n" + "=" * 50)
    print("OPTIMIZATION SUITE SUMMARY")
    print("=" * 50)
    
    print("📁 FILES CREATED:")
    if config_created:
        print("✅ config.json - Optimized WebUI settings")
    if presets_created:
        print("✅ quality_presets.json - Quality preset configurations")
    if launcher_created:
        print("✅ webui_optimized.bat - Advanced launcher with optimizations")
    if guide_created:
        print("✅ Advanced_Prompt_Engineering_Guide.md - Comprehensive prompting guide")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Launch with: .\\webui_optimized.bat")
    print("2. Load quality presets from quality_presets.json")
    print("3. Study Advanced_Prompt_Engineering_Guide.md")
    print("4. Test with optimized settings")
    
    print("\n💡 OPTIMIZATION FEATURES:")
    print("- RTX 3080 specific optimizations")
    print("- xFormers attention optimization")
    print("- Memory management improvements")
    print("- Quality preset configurations")
    print("- Advanced prompt engineering techniques")

if __name__ == "__main__":
    main()
