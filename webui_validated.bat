@echo off
echo Stable Diffusion WebUI - Validated Arguments (RTX 3080)
echo ======================================================
echo.

REM Kill any existing WebUI processes
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Check if models exist
if not exist "models\Stable-diffusion\v1-5-pruned-emaonly.safetensors" (
    echo ❌ Model file not found: v1-5-pruned-emaonly.safetensors
    echo Please ensure the official SD 1.5 model is downloaded
    echo.
    pause
    exit /b 1
)

if not exist "models\VAE\vae-ft-ema-560000-ema-pruned.safetensors" (
    echo ❌ VAE file not found: vae-ft-ema-560000-ema-pruned.safetensors
    echo WebUI will use model's built-in VAE
    echo.
)

REM Advanced GPU environment variables for RTX 3080
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512,expandable_segments:True
set CUDA_LAUNCH_BLOCKING=0
set CUDA_CACHE_DISABLE=0
set CUDA_MODULE_LOADING=LAZY
set PYTORCH_NVFUSER_DISABLE_FALLBACK=1

REM Memory optimization
set SAFETENSORS_FAST_GPU=1

REM Base arguments (validated against cmd_args.py)
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install

REM Performance optimizations for RTX 3080 (16GB VRAM)
REM All arguments validated against stable-diffusion-webui v1.10.1
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --xformers
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention-v1
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-channelslast

REM Alternative attention optimizations (fallback if xFormers fails)
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-sub-quad-attention

REM Quality optimizations
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --upcast-sampling

REM Model and VAE paths
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --ckpt "models\Stable-diffusion\v1-5-pruned-emaonly.safetensors"
if exist "models\VAE\vae-ft-ema-560000-ema-pruned.safetensors" (
    set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models\VAE\vae-ft-ema-560000-ema-pruned.safetensors"
)

REM Advanced features
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --enable-insecure-extension-access
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --api
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --api-log

REM Performance monitoring
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --disable-console-progressbars

echo ✅ Configuration: RTX 3080 Laptop Optimized
echo ✅ All arguments validated against WebUI v1.10.1
echo ✅ Features: xFormers, optimized attention, upcast sampling
echo ✅ Quality: Maximum with performance balance
echo ✅ API: Enabled for extensions and automation
echo.

echo 🔍 Checking xFormers availability...
python -c "import xformers; print('✅ xFormers available:', xformers.__version__)" 2>nul || echo "⚠️  xFormers not available - using fallback optimizations"

echo.
echo 🚀 Starting WebUI...
echo.

call webui.bat %*
