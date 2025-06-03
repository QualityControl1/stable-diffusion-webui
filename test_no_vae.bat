@echo off
echo VAE Test: No external VAE (use model's built-in)
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
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast --no-half-vae
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% 

echo Configuration: No external VAE (use model's built-in)
echo VAE Args: 
echo Precision Args: --precision autocast --no-half-vae
echo.
echo Expected: Should fix colorful noise if this configuration works
echo Test prompt: "a simple red apple on white background"
echo.

call webui.bat %*
