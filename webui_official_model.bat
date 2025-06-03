@echo off
echo Stable Diffusion WebUI - Official SD 1.5 Model
echo ==============================================
echo.

REM Kill any existing WebUI processes
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

REM Check if official model exists
if not exist "models\Stable-diffusion\v1-5-pruned-emaonly.safetensors" (
    echo Official SD 1.5 model not found!
    echo Please wait for download to complete or run: download_official_sd15.bat
    echo.
    pause
    exit /b 1
)

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention --medvram

REM Optimal settings for official model
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --ckpt "models\Stable-diffusion\v1-5-pruned-emaonly.safetensors"
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --vae-path "models\VAE\vae-ft-ema-560000-ema-pruned.safetensors"

echo Configuration: Official SD 1.5 with optimal settings
echo Model: v1-5-pruned-emaonly.safetensors
echo VAE: vae-ft-ema-560000-ema-pruned.safetensors
echo Expected: Perfect image generation without issues
echo.
echo Test prompt: "a simple red apple on white background"
echo Settings: 20 steps, CFG 7.0, 512x512, DPM++ 2M Karras
echo.

call webui.bat %*