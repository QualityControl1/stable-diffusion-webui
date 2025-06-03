# WebUI Launch Guide for Python 3.13

## ✅ Your Current Status
- Python 3.13.1 with PyTorch 2.7.0+cpu ✅
- All problematic packages avoided ✅
- Alternative packages installed ✅
- webui_compatible.bat created ✅

## 🚀 How to Launch WebUI

### Step 1: Use Correct PowerShell Syntax
```powershell
# Navigate to your WebUI directory (if not already there)
cd "C:\Users\TEila\source\repos\AUTOMATIC_UI\stable-diffusion-webui"

# Launch with dot-slash prefix (required in PowerShell)
.\webui_compatible.bat
```

### Step 2: What to Expect
The WebUI will start with these messages:
```
Starting WebUI with Python 3.13 compatibility...

Configuration:
- Python 3.13 compatibility mode
- Skipping CLIP installation (compatibility issues)
- Using existing PyTorch installation
- Stability flags enabled

Installing torch and torchvision
Skipping CLIP/open_clip installation on Python 3.13 (compatibility issues)
CLIP functionality will be limited but WebUI should still work
```

### Step 3: Expected Startup Sequence
1. **Environment preparation** - Should skip CLIP packages
2. **Repository cloning** - Downloads required models/assets
3. **Requirements installation** - Installs remaining packages
4. **WebUI startup** - Launches Gradio interface
5. **Browser opens** - Usually at http://127.0.0.1:7860

## 🛠️ Troubleshooting

### If "CommandNotFoundException" persists:
```powershell
# Check if file exists
ls webui_compatible.bat

# Check current directory
pwd

# Try full path
.\webui_compatible.bat

# Alternative: Use cmd instead of PowerShell
cmd /c webui_compatible.bat
```

### If WebUI fails to start:
```powershell
# Try with more verbose output
set WEBUI_LAUNCH_LIVE_OUTPUT=1
.\webui_compatible.bat

# Or try the original webui.bat with skip flags
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install --no-half --precision full
.\webui.bat
```

### If package installation errors occur:
```powershell
# The config should skip problematic packages, but if issues persist:
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install --skip-torch-cuda-test
.\webui.bat
```

## 📋 Expected Limitations

With Python 3.13 and skipped CLIP packages:
- ✅ **Basic image generation** - Should work
- ✅ **Text-to-image** - Core functionality works
- ✅ **Image-to-image** - Should work
- ⚠️ **CLIP interrogator** - May be limited
- ⚠️ **Some extensions** - May have compatibility issues
- ✅ **Web interface** - Should work normally

## 🎯 Success Indicators

You'll know it's working when you see:
```
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://[random].gradio.live

To create a public link, set `share=True` in `launch()`.
```

## 🔧 Alternative Launch Methods

### Method 1: Direct webui.bat with environment variables
```powershell
$env:COMMANDLINE_ARGS="--skip-python-version-check --skip-install --no-half --precision full"
$env:TORCH_COMMAND="echo 'Using existing PyTorch'"
$env:CLIP_PACKAGE="echo 'Skipping CLIP'"
$env:OPENCLIP_PACKAGE="echo 'Skipping open_clip'"
.\webui.bat
```

### Method 2: Command Prompt (if PowerShell issues persist)
```cmd
webui_compatible.bat
```

### Method 3: Manual Python execution
```powershell
# If batch files don't work, try direct Python
python launch.py --skip-python-version-check --skip-install --no-half --precision full
```

## 📊 Performance Expectations

With CPU-only PyTorch 2.7.0:
- **Image generation time**: 30-120 seconds per image (depending on settings)
- **Memory usage**: 4-8GB RAM typical
- **CPU usage**: High during generation
- **Quality**: Same as GPU (just slower)

## 🎨 Recommended Settings for CPU Mode

Once WebUI starts, use these settings for better performance:
- **Sampling steps**: 20-30 (lower = faster)
- **Image size**: 512x512 or 768x768 (smaller = faster)
- **Batch size**: 1 (CPU can't handle multiple images well)
- **CFG Scale**: 7-12 (standard range)

## 🚨 If All Else Fails

Last resort options:
1. **Use Python 3.10**: Most stable for AI workloads
2. **Try Docker**: Isolated environment
3. **Use online services**: If local setup too problematic

## 📞 Next Steps After Launch

1. **Test basic generation** - Try generating a simple image
2. **Check console output** - Look for any error messages
3. **Monitor performance** - Note generation times
4. **Explore features** - See what works with your setup
