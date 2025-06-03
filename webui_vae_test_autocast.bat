@echo off
echo Autocast precision test
echo ========================
echo.

REM GPU environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Base arguments
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --opt-split-attention --medvram

REM Precision-specific arguments
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast --no-half-vae --disable-nan-check

echo Configuration: Autocast precision test
echo Arguments: --precision autocast --no-half-vae --disable-nan-check
echo.
echo Expected: Should fix noise/static issues
echo.

call webui.bat %*
