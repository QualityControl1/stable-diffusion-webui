# PyTorch Python 3.13 Compatibility Fix

## Problem Description

You're encountering a `RuntimeError: "Couldn't install torch"` when trying to run stable-diffusion-webui with Python 3.13. This happens because:

1. **PyTorch 2.1.2 doesn't support Python 3.13** - The webui is hardcoded to install PyTorch 2.1.2, which was released before Python 3.13 support was added
2. **Limited wheel availability** - PyTorch wheels for Python 3.13 are only available for PyTorch 2.5.0+ and newer versions
3. **Version compatibility matrix** - The stable-diffusion-webui expects specific PyTorch versions that aren't compatible with Python 3.13

## Solutions (In Order of Recommendation)

### Solution 1: Use the Automated Fix Script ⭐ **RECOMMENDED**

I've created an automated fix script that handles all the compatibility issues:

```bash
# Run the automated fix
python fix_pytorch_python313.py

# Or on Windows, double-click:
fix_pytorch.bat
```

This script will:
- Detect your Python version
- Install the appropriate PyTorch version for Python 3.13 (2.5.1+)
- Create environment override files
- Test the installation

### Solution 2: Manual PyTorch Installation

Install a compatible PyTorch version manually:

```bash
# For Python 3.13 with CUDA 12.1
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --extra-index-url https://download.pytorch.org/whl/cu121

# For CPU-only (fallback)
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --extra-index-url https://download.pytorch.org/whl/cpu
```

### Solution 3: Use Environment Variables

Set environment variables to override the default PyTorch versions:

**Windows (Command Prompt):**
```cmd
set TORCH_COMMAND=pip install torch==2.5.1 torchvision==0.20.1 --extra-index-url https://download.pytorch.org/whl/cu121
set COMMANDLINE_ARGS=--skip-python-version-check
webui.bat
```

**Windows (PowerShell):**
```powershell
$env:TORCH_COMMAND="pip install torch==2.5.1 torchvision==0.20.1 --extra-index-url https://download.pytorch.org/whl/cu121"
$env:COMMANDLINE_ARGS="--skip-python-version-check"
.\webui.bat
```

### Solution 4: Downgrade to Python 3.10-3.12 ⭐ **MOST STABLE**

For the most stable experience, use Python 3.10-3.12:

1. Download Python 3.10.11 from: https://www.python.org/downloads/release/python-31011/
2. Install it in a separate directory
3. Create a virtual environment:
   ```bash
   C:\Python310\python.exe -m venv venv
   venv\Scripts\activate
   ```
4. Run the webui normally

## Files Modified

The automated fix has updated your `modules/launch_utils.py` to:
- Support Python 3.13 in the version check
- Automatically select compatible PyTorch versions based on Python version
- Provide better error messages and warnings

## Verification

After applying any solution, verify the installation:

```python
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"Python version: {sys.version}")
print(f"CUDA available: {torch.cuda.is_available()}")
```

## Troubleshooting

### If PyTorch installation still fails:

1. **Clear pip cache:**
   ```bash
   pip cache purge
   ```

2. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Try nightly build:**
   ```bash
   pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cu121
   ```

4. **Use CPU-only version:**
   ```bash
   pip install torch==2.5.1 torchvision==0.20.1 --extra-index-url https://download.pytorch.org/whl/cpu
   ```

### If webui still has issues:

1. **Delete venv folder** and let webui recreate it
2. **Use the skip flag:**
   ```bash
   webui.bat --skip-python-version-check --skip-torch-cuda-test
   ```

## PyTorch Python 3.13 Support Status

| PyTorch Version | Python 3.13 Support | Status |
|----------------|---------------------|---------|
| 2.1.2          | ❌ No              | Used by webui (incompatible) |
| 2.5.0          | ✅ Yes (Linux only) | Limited platform support |
| 2.5.1          | ✅ Yes (Linux only) | Better support |
| 2.6.0          | ✅ Yes (Multi-platform) | Recommended |
| Nightly        | ✅ Yes              | Latest features |

## Alternative: Use Docker

If all else fails, consider using Docker with a Python 3.10 environment:

```dockerfile
FROM python:3.10-slim
# ... rest of your setup
```

## Support

If you continue to have issues:
1. Check the [PyTorch installation guide](https://pytorch.org/get-started/locally/)
2. Visit the [stable-diffusion-webui GitHub issues](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues)
3. Consider using Python 3.10-3.12 for the most stable experience
