@echo off
set TORCH_COMMAND=pip install torch==2.6.0 torchvision==0.21.0 --extra-index-url https://download.pytorch.org/whl/cu121
set COMMANDLINE_ARGS=--skip-python-version-check
call webui.bat %*
