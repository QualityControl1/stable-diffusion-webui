# VAE Noise/Static Troubleshooting Guide
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
