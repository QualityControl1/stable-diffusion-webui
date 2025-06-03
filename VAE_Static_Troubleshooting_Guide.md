# VAE Colorful Static/Noise Troubleshooting Guide
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
