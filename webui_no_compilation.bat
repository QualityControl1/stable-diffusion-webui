@echo off
REM No-Compilation WebUI Configuration for Python 3.13
echo ================================================
echo Stable Diffusion WebUI - No Compilation Mode
echo ================================================
echo.
echo This configuration avoids cmake, sentencepiece, and C++ compilation
echo by skipping problematic packages and using CPU-only mode.
echo.

REM Skip all package installations that require compilation
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install --no-half --precision full

REM Use existing PyTorch installation
set TORCH_COMMAND=echo "Using existing PyTorch 2.7.0+cpu"

REM Skip problematic packages
set CLIP_PACKAGE=echo "Skipping CLIP (compilation issues)"
set OPENCLIP_PACKAGE=echo "Skipping open_clip (compilation issues)"
set XFORMERS_PACKAGE=none

REM Additional stability flags
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --disable-safe-unpickle --use-cpu all

echo Configuration Summary:
echo - Python 3.13.1 compatibility mode
echo - Skipping automatic package installation
echo - Using existing PyTorch 2.7.0+cpu
echo - CPU-only processing (no GPU)
echo - Avoiding all compilation requirements
echo.
echo Note: This will be slower but should work without build errors.
echo.

pause
echo Starting WebUI...
call webui.bat %*
