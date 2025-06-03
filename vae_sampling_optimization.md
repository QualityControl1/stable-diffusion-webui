# VAE and Sampling Optimization Guide
====================================

## 1. VAE SELECTION AND OPTIMIZATION

### Current Working VAE:
```
✅ vae-ft-ema-560000-ema-pruned.safetensors
- Type: EMA (Exponential Moving Average) trained
- Compatibility: Excellent with SD 1.5
- Quality: High detail preservation
- VRAM: ~800MB additional
```

### Alternative High-Quality VAEs:

#### For SD 1.5 Models:
```
1. vae-ft-mse-840000-ema-pruned.safetensors
   - Type: MSE (Mean Squared Error) trained
   - Best for: Sharp details, high contrast
   - Use case: Photography, realistic images
   - Download: HuggingFace stabilityai/sd-vae-ft-mse-original

2. kl-f8-anime2.ckpt
   - Type: Anime-optimized VAE
   - Best for: Anime/manga style images
   - Use case: Artistic, stylized content
   - Note: Use with anime-focused models

3. vae-ft-ema-560000-ema-pruned.ckpt
   - Type: Same as safetensors but .ckpt format
   - Use only if safetensors version unavailable
```

#### For SDXL Models:
```
1. sdxl_vae.safetensors
   - Type: Official SDXL VAE
   - Best for: SDXL models exclusively
   - VRAM: ~1.2GB additional
   - Required for proper SDXL operation
```

### VAE Quality Comparison Test:
```python
# Test prompt for VAE comparison
test_prompt = "close-up portrait of a woman, highly detailed skin texture, professional photography"

# Settings for comparison
steps = 25
cfg_scale = 7.5
sampler = "DPM++ 2M Karras"
resolution = "768x768"

# Compare:
1. No VAE (model default)
2. EMA VAE (current)
3. MSE VAE (alternative)
```

## 2. OPTIMAL SAMPLING METHODS

### Tier 1: Best Quality (Recommended)
```
1. DPM++ 2M Karras
   - Quality: Excellent
   - Speed: Good
   - Steps: 20-30
   - Best for: General use, high quality

2. DPM++ SDE Karras
   - Quality: Excellent
   - Speed: Slower
   - Steps: 20-25
   - Best for: Maximum quality, final renders

3. UniPC
   - Quality: Very Good
   - Speed: Fast
   - Steps: 15-25
   - Best for: Balanced quality/speed
```

### Tier 2: Good Quality/Speed Balance
```
1. Euler a
   - Quality: Good
   - Speed: Very Fast
   - Steps: 15-20
   - Best for: Quick previews, testing

2. DPM++ 2M
   - Quality: Very Good
   - Speed: Good
   - Steps: 20-25
   - Best for: General use without Karras noise

3. DDIM
   - Quality: Good
   - Speed: Fast
   - Steps: 20-30
   - Best for: Reproducible results
```

### Tier 3: Specialized Use Cases
```
1. LMS Karras
   - Quality: Good
   - Speed: Fast
   - Steps: 15-25
   - Best for: Artistic styles

2. Heun
   - Quality: Very Good
   - Speed: Slow
   - Steps: 15-20
   - Best for: High precision needs

3. DPM2 a Karras
   - Quality: Good
   - Speed: Medium
   - Steps: 20-30
   - Best for: Specific artistic effects
```

## 3. SAMPLING PARAMETER OPTIMIZATION

### CFG Scale (Classifier-Free Guidance):
```
Range: 1.0 - 20.0
Recommended ranges by use case:

1.0 - 3.0: Minimal guidance (very creative, unpredictable)
4.0 - 6.0: Low guidance (creative, loose interpretation)
7.0 - 9.0: Standard guidance (balanced, recommended)
10.0 - 12.0: High guidance (strict prompt following)
13.0+: Very high guidance (may cause artifacts)

Optimal for most cases: 7.0 - 8.0
```

### Steps Optimization:
```
Sampler-specific recommendations:

DPM++ 2M Karras:
- Minimum: 15 steps
- Optimal: 20-25 steps
- Maximum benefit: 30 steps

Euler a:
- Minimum: 10 steps
- Optimal: 15-20 steps
- Maximum benefit: 25 steps

UniPC:
- Minimum: 12 steps
- Optimal: 15-20 steps
- Maximum benefit: 25 steps
```

### Advanced Sampling Parameters:
```
Eta (η) - Noise scheduling:
- DDIM: 0.0 (deterministic) to 1.0 (stochastic)
- Ancestral samplers: Controls randomness
- Recommended: 0.0 for reproducibility, 0.67 for creativity

Sigma parameters:
- s_churn: 0.0-1.0 (adds noise, increases creativity)
- s_tmin: 0.0-1.0 (minimum sigma threshold)
- s_tmax: 0.0-1.0 (maximum sigma threshold)
- s_noise: 0.0-1.0 (noise multiplier)

Recommended for quality:
s_churn = 0.0, s_tmin = 0.0, s_tmax = 0.0, s_noise = 1.0
```

## 4. RESOLUTION AND ASPECT RATIO OPTIMIZATION

### SD 1.5 Optimal Resolutions:
```
Standard resolutions (trained on):
- 512x512 (1:1) - Best quality, fastest
- 512x768 (2:3) - Portrait orientation
- 768x512 (3:2) - Landscape orientation
- 640x640 (1:1) - Slightly higher detail

High-resolution (with highres fix):
- 768x768 (1:1) - Good balance
- 1024x1024 (1:1) - High detail
- 1024x768 (4:3) - Landscape
- 768x1024 (3:4) - Portrait
```

### Highres Fix Optimization:
```
Optimal settings for RTX 3080:
- Upscaler: R-ESRGAN 4x+ or R-ESRGAN 4x+ Anime6B
- Upscale by: 1.5x to 2.0x
- Hires steps: 15-20 (50-75% of main steps)
- Denoising strength: 0.4-0.6

Example configuration:
Base: 512x512, 25 steps
Hires: 1.5x scale (768x768), 15 steps, 0.5 denoising
```

## 5. BATCH OPTIMIZATION STRATEGIES

### Batch Size vs Quality:
```
RTX 3080 (16GB VRAM) recommendations:

512x512 resolution:
- Batch size: 4-6 images
- VRAM usage: ~12-14GB
- Generation time: ~15-20 seconds

768x768 resolution:
- Batch size: 2-3 images
- VRAM usage: ~14-15GB
- Generation time: ~25-35 seconds

1024x1024 resolution:
- Batch size: 1-2 images
- VRAM usage: ~15-16GB
- Generation time: ~45-60 seconds
```

### Batch Count Strategy:
```
For exploration (testing prompts):
- Batch size: 4
- Batch count: 2-3
- Total: 8-12 images

For final generation:
- Batch size: 1-2
- Batch count: 1
- Focus on quality over quantity
```

## 6. MEMORY OPTIMIZATION TECHNIQUES

### VRAM Management:
```
Current optimal flags for RTX 3080:
--xformers                    # Efficient attention mechanism
--opt-split-attention-v1      # Memory-efficient attention
--opt-channelslast           # Memory layout optimization
--no-half-vae                # Prevent VAE precision issues
--upcast-sampling            # Quality improvement
```

### Dynamic VRAM Allocation:
```python
# Environment variables for optimal memory usage
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512,expandable_segments:True
SAFETENSORS_FAST_GPU=1
CUDA_MODULE_LOADING=LAZY
```

## 7. QUALITY ENHANCEMENT WORKFLOWS

### Two-Pass Generation:
```
Pass 1: Base generation
- Resolution: 512x512
- Steps: 20
- CFG: 7.0
- Sampler: DPM++ 2M Karras

Pass 2: Upscaling/refinement
- Highres fix: 1.5x
- Hires steps: 15
- Denoising: 0.5
- Final resolution: 768x768
```

### Multi-Sampler Comparison:
```python
# Automated sampler comparison script
samplers = ["DPM++ 2M Karras", "DPM++ SDE Karras", "UniPC", "Euler a"]
prompt = "your test prompt here"

for sampler in samplers:
    generate_image(prompt, sampler, steps=20, cfg=7.5)
    # Compare results and select best
```

## 8. ADVANCED VAE TECHNIQUES

### VAE Tiling (for high resolution):
```
Enable for resolutions > 1024x1024:
--vae-tiling

Benefits:
- Reduces VRAM usage
- Enables higher resolution generation
- Maintains quality consistency
```

### VAE Precision Control:
```
Current optimal settings:
--no-half-vae        # Prevents precision issues
--upcast-sampling    # Improves quality

Alternative for extreme VRAM constraints:
--half-vae          # Reduces VRAM but may affect quality
```

## 9. PERFORMANCE MONITORING

### Key Metrics to Track:
```
1. Generation time per image
2. VRAM usage peak
3. Quality consistency score
4. Artifact frequency
5. Color accuracy

Tools:
- nvidia-smi (VRAM monitoring)
- WebUI built-in timing
- Custom benchmarking scripts
```

### Optimization Validation:
```python
# Performance test template
def test_configuration(sampler, steps, cfg, resolution):
    start_time = time.time()
    result = generate_image(
        prompt="test prompt",
        sampler=sampler,
        steps=steps,
        cfg_scale=cfg,
        width=resolution[0],
        height=resolution[1]
    )
    end_time = time.time()
    
    return {
        "time": end_time - start_time,
        "quality_score": evaluate_quality(result),
        "vram_peak": get_vram_usage()
    }
```

## 10. RECOMMENDED OPTIMIZATION PRESETS

### Ultra Quality Preset:
```
Sampler: DPM++ SDE Karras
Steps: 30
CFG Scale: 7.5
Resolution: 768x768
VAE: vae-ft-ema-560000-ema-pruned.safetensors
Highres fix: 1.5x, 20 steps, 0.5 denoising
```

### Balanced Preset:
```
Sampler: DPM++ 2M Karras
Steps: 20
CFG Scale: 7.0
Resolution: 512x512
VAE: vae-ft-ema-560000-ema-pruned.safetensors
Batch size: 4
```

### Speed Preset:
```
Sampler: Euler a
Steps: 15
CFG Scale: 6.5
Resolution: 512x512
VAE: vae-ft-ema-560000-ema-pruned.safetensors
Batch size: 6
```

These optimizations will significantly improve your image generation quality and workflow efficiency while maintaining stability with your Python 3.13/PyTorch 2.6 setup.
