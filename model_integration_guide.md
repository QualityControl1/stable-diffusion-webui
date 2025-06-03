# Safe Model Integration Guide for Python 3.13/PyTorch 2.6
===========================================================

## 1. MODEL COMPATIBILITY CHECKLIST

### ✅ Safe Model Formats:
- **Safetensors (.safetensors)** - Preferred format, maximum security
- **Checkpoint (.ckpt)** - Use with caution, scan for malicious code
- **Diffusers format** - HuggingFace native format, very safe

### ❌ Avoid These:
- **Pickle files from unknown sources** - Security risk
- **Models without proper metadata** - May have compatibility issues
- **Very old models (pre-2023)** - Likely incompatible with modern PyTorch

## 2. RECOMMENDED HIGH-QUALITY MODELS

### SD 1.5 Variants (Guaranteed Compatible):
```
1. Realistic Vision V5.1 (safetensors)
   - URL: https://civitai.com/models/4201/realistic-vision-v51
   - Best for: Photorealistic portraits and scenes
   - VRAM: 4-6GB

2. DreamShaper 8 (safetensors)
   - URL: https://civitai.com/models/4384/dreamshaper
   - Best for: Artistic and fantasy content
   - VRAM: 4-6GB

3. Deliberate V2 (safetensors)
   - URL: https://civitai.com/models/4823/deliberate
   - Best for: Balanced realism and artistic style
   - VRAM: 4-6GB

4. ChilloutMix (safetensors)
   - URL: https://civitai.com/models/6424/chilloutmix
   - Best for: Asian-style portraits
   - VRAM: 4-6GB
```

### SDXL Models (For Future Use):
```
1. SDXL Base 1.0 (safetensors)
   - Official Stability AI release
   - VRAM: 8-12GB
   - Higher resolution (1024x1024 native)

2. SDXL Turbo (safetensors)
   - Fast generation variant
   - VRAM: 6-8GB
   - 1-4 steps generation
```

## 3. SAFE DOWNLOAD PROCEDURES

### Step 1: Verify Source
```bash
# Trusted sources:
- HuggingFace (huggingface.co)
- Civitai (civitai.com)
- Official model repositories
- Stability AI releases
```

### Step 2: Check File Integrity
```bash
# Verify file size matches expected
# Check SHA256 hash if provided
# Scan with antivirus before use
```

### Step 3: Test Installation
```bash
# Place in models/Stable-diffusion/
# Launch with webui_optimized.bat
# Test with simple prompt first
# Monitor VRAM usage and stability
```

## 4. MODEL TESTING PROTOCOL

### Phase 1: Basic Compatibility Test
```
Prompt: "a simple red apple on white background"
Settings: 20 steps, CFG 7.0, 512x512, DPM++ 2M Karras
Expected: Clean, artifact-free image
```

### Phase 2: Quality Assessment
```
Prompt: "portrait of a woman, professional photography, highly detailed"
Settings: 25 steps, CFG 7.5, 768x768, DPM++ 2M Karras
Expected: High-quality, detailed portrait
```

### Phase 3: Performance Test
```
Batch generation: 4 images
Monitor: VRAM usage, generation time, stability
Expected: Consistent performance without crashes
```

### Phase 4: Advanced Features
```
Test: Highres fix, face restoration, inpainting
Expected: All features work without errors
```

## 5. VRAM OPTIMIZATION BY MODEL TYPE

### SD 1.5 Models (4GB base):
```
--medvram          # 8GB+ VRAM
--lowvram          # 4-6GB VRAM  
--lowram           # <4GB VRAM (very slow)
```

### SDXL Models (8GB base):
```
--medvram-sdxl     # 12GB+ VRAM
--lowvram          # 8-10GB VRAM
--lowram           # <8GB VRAM (not recommended)
```

### Your RTX 3080 (16GB) Optimal Settings:
```
# For SD 1.5: No VRAM flags needed
--xformers --opt-split-attention-v1

# For SDXL: Use medvram-sdxl for safety
--medvram-sdxl --xformers --opt-split-attention-v1
```

## 6. MODEL SWITCHING WORKFLOW

### Method 1: WebUI Interface
```
1. Settings > Stable Diffusion > SD Checkpoint
2. Select new model from dropdown
3. Click "Apply settings"
4. Wait for model loading (30-60 seconds)
5. Test with simple prompt
```

### Method 2: Command Line
```
--ckpt "models/Stable-diffusion/model_name.safetensors"
```

### Method 3: API (Advanced)
```python
import requests
response = requests.post("http://127.0.0.1:7860/sdapi/v1/options", 
                        json={"sd_model_checkpoint": "model_name.safetensors"})
```

## 7. TROUBLESHOOTING COMMON ISSUES

### Issue: Model Won't Load
```
Solutions:
1. Check file integrity (re-download if corrupted)
2. Verify safetensors format
3. Check available VRAM
4. Try with --lowvram flag
```

### Issue: Poor Quality Output
```
Solutions:
1. Adjust CFG scale (6.0-8.0 range)
2. Increase steps (20-30)
3. Try different sampler
4. Check VAE compatibility
```

### Issue: CUDA Out of Memory
```
Solutions:
1. Add --medvram flag
2. Reduce batch size
3. Lower resolution
4. Close other GPU applications
```

### Issue: Slow Generation
```
Solutions:
1. Enable xFormers (--xformers)
2. Use optimized attention (--opt-split-attention-v1)
3. Check for background processes
4. Verify GPU utilization
```

## 8. ADVANCED MODEL MANAGEMENT

### Model Organization:
```
models/
├── Stable-diffusion/
│   ├── realistic/
│   │   ├── realistic-vision-v51.safetensors
│   │   └── chilloutmix.safetensors
│   ├── artistic/
│   │   ├── dreamshaper-8.safetensors
│   │   └── deliberate-v2.safetensors
│   └── sdxl/
│       └── sdxl-base-1.0.safetensors
```

### Model Metadata Tracking:
```json
{
  "model_name": "Realistic Vision V5.1",
  "file_size": "3.97GB",
  "hash": "sha256:...",
  "source": "civitai.com",
  "tested_date": "2025-01-XX",
  "compatibility": "excellent",
  "recommended_settings": {
    "steps": 25,
    "cfg": 7.5,
    "sampler": "DPM++ 2M Karras"
  }
}
```

## 9. PERFORMANCE BENCHMARKING

### Benchmark Script Template:
```python
import time
import requests

def benchmark_model(model_name, prompt, steps=20):
    # Switch model
    requests.post("http://127.0.0.1:7860/sdapi/v1/options", 
                 json={"sd_model_checkpoint": model_name})
    
    # Generate image
    start_time = time.time()
    response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", 
                           json={"prompt": prompt, "steps": steps})
    end_time = time.time()
    
    return end_time - start_time
```

### Key Metrics to Track:
- Generation time per image
- VRAM usage peak
- Quality consistency
- Feature compatibility
- Stability (crashes/errors)

## 10. FUTURE-PROOFING STRATEGIES

### Stay Updated:
- Monitor PyTorch compatibility
- Follow model format evolution
- Test new releases carefully
- Maintain backup configurations

### Version Control:
- Document working configurations
- Keep model version history
- Track performance changes
- Maintain rollback capability

This guide ensures safe, high-quality model integration while maintaining the stability we've achieved with your Python 3.13/PyTorch 2.6 setup.
