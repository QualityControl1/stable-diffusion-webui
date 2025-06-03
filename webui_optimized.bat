@echo off
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
set SAFETENSORS_FAST_GPU=1

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install

REM Performance optimizations for RTX 3080 (16GB VRAM)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --xformers --opt-split-attention-v1
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-channelslast

REM Memory optimization (only use medvram-sdxl for SDXL models)
REM set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram-sdxl

REM Quality optimizations
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --upcast-sampling

REM Model and VAE
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --ckpt "models\Stable-diffusion\v1-5-pruned-emaonly.safetensors"
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models\VAE\vae-ft-ema-560000-ema-pruned.safetensors"

REM Advanced features
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --enable-insecure-extension-access
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --api --api-log

REM UI optimizations (gradio-queue is enabled by default, --multiple is not a valid argument)
REM set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --gradio-queue

echo Configuration: Optimized for RTX 3080 Laptop (16GB VRAM)
echo Features: xFormers, optimized attention, upcast sampling
echo Quality: Maximum with performance balance
echo API: Enabled for extensions and automation
echo.

call webui.bat %*
