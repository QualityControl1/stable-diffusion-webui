@echo off
REM PyTorch Recovery Script for Python 3.13 + CUDA
echo PyTorch Recovery for Python 3.13 + RTX 3080
echo =============================================
echo.

echo Cleaning previous installations...
pip uninstall torch torchvision torchaudio xformers -y

echo Installing PyTorch with CUDA 11.8 (Python 3.13 compatible)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo Testing installation...
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"}')"

echo Installing xFormers...
pip install xformers

echo Recovery completed!
pause
