@echo off
REM RTX 3080 GPU Launch Script (Manual Creation - No Unicode)
echo Starting WebUI with RTX 3080 GPU acceleration...
echo.

REM Verify dependencies
python -c "import torch; import numpy; import gradio; print('Dependencies OK')" || (
    echo ERROR: Dependencies missing - run fix_package_conflicts.py
    pause
    exit /b 1
)

REM Check GPU
python -c "import torch; print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not available')"

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM WebUI configuration
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set TORCH_COMMAND=echo "Using existing PyTorch installation"
set CLIP_PACKAGE=echo "Skipping CLIP (compatibility issues)"
set OPENCLIP_PACKAGE=echo "Skipping open_clip (compatibility issues)"

REM RTX 3080 optimization flags
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --no-half-vae

REM Enable xFormers if available
python -c "import xformers" >nul 2>&1 && (
    set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --xformers
    echo xFormers enabled - Maximum performance
) || (
    echo xFormers not available - Standard performance
)

echo.
echo RTX 3080 Configuration:
echo - Target: 15-40 seconds per 512x512 image
echo - VRAM: 8-12GB usage
echo - Python 3.13 compatibility preserved
echo.

call webui.bat %*
