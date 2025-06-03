# PyTorch CUDA Fix Commands for Python 3.13

## Quick Fix (Manual Commands)

### Step 1: Uninstall CPU-only PyTorch
```powershell
python -m pip uninstall torch torchvision torchaudio -y
```

### Step 2: Install CUDA-enabled PyTorch 2.6.0
```powershell
# For CUDA 12.1 (matches your system)
python -m pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --extra-index-url https://download.pytorch.org/whl/cu121
```

### Step 3: Verify Installation
```powershell
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

## Alternative CUDA Versions (if cu121 fails)

### CUDA 11.8 (fallback)
```powershell
python -m pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --extra-index-url https://download.pytorch.org/whl/cu118
```

### CUDA 12.4 (newer)
```powershell
python -m pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --extra-index-url https://download.pytorch.org/whl/cu124
```

## Automated Solutions

### Option 1: Use the CUDA Fix Script
```powershell
# In PowerShell, navigate to your webui directory
cd "C:\Users\TEila\source\repos\AUTOMATIC_UI\stable-diffusion-webui"

# Run the CUDA fix
.\fix_cuda.bat
# OR
python fix_pytorch_cuda.py
```

### Option 2: Use Updated Main Fix Script
```powershell
python fix_pytorch_python313.py
```

## Verification Commands

### Test CUDA Availability
```powershell
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

### Test GPU Operations
```powershell
python -c "import torch; device = torch.device('cuda' if torch.cuda.is_available() else 'cpu'); x = torch.rand(5, 3, device=device); print('GPU test successful:', x.device)"
```

### Check GPU Memory
```powershell
python -c "import torch; print('GPU memory:', torch.cuda.get_device_properties(0).total_memory / 1024**3, 'GB') if torch.cuda.is_available() else print('No GPU')"
```

## WebUI Launch Commands

### Using Environment Override
```powershell
# Use the created environment file
.\webui_env.bat
```

### Manual Environment Variables
```powershell
$env:TORCH_COMMAND="pip install torch==2.6.0 torchvision==0.21.0 --extra-index-url https://download.pytorch.org/whl/cu121"
$env:COMMANDLINE_ARGS="--skip-python-version-check"
.\webui.bat
```

## Troubleshooting

### If CUDA Installation Fails
1. **Check NVIDIA drivers:**
   ```powershell
   nvidia-smi
   ```

2. **Clear pip cache:**
   ```powershell
   python -m pip cache purge
   ```

3. **Upgrade pip:**
   ```powershell
   python -m pip install --upgrade pip
   ```

4. **Force reinstall:**
   ```powershell
   python -m pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --extra-index-url https://download.pytorch.org/whl/cu121 --force-reinstall --no-cache-dir
   ```

### If WebUI Still Has Issues
1. **Delete venv folder:**
   ```powershell
   Remove-Item -Recurse -Force venv
   ```

2. **Launch with skip flags:**
   ```powershell
   .\webui.bat --skip-python-version-check --skip-torch-cuda-test
   ```

## Expected Output After Fix

```
✅ PyTorch version: 2.6.0+cu121
✅ CUDA available: True
✅ GPU device: [Your GPU Name]
✅ GPU memory: [Your GPU Memory] GB
```

## PowerShell Notes

- Use `.\` prefix for batch files: `.\fix_cuda.bat`
- Use `python` command (not `py` or `python3`)
- Run PowerShell as Administrator if you get permission errors
