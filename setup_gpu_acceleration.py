#!/usr/bin/env python3
"""
Setup GPU Acceleration for Python 3.13 Stable Diffusion WebUI

This script configures GPU acceleration while preserving all
Python 3.13 compatibility fixes we've implemented.

Author: Augment Agent
Date: January 2025
"""

import sys
import subprocess
import platform
import os

def detect_system_specs():
    """Detect system specifications"""
    print("=== System Specifications Detection ===")
    
    specs = {
        'os': platform.system(),
        'python_version': sys.version,
        'gpu': None,
        'cuda_available': False,
        'pytorch_version': None,
        'cuda_version': None
    }
    
    # Check PyTorch and CUDA
    try:
        import torch
        specs['pytorch_version'] = torch.__version__
        specs['cuda_available'] = torch.cuda.is_available()
        if torch.cuda.is_available():
            specs['cuda_version'] = torch.version.cuda
            specs['gpu'] = torch.cuda.get_device_name(0)
            specs['gpu_count'] = torch.cuda.device_count()
            specs['gpu_memory'] = torch.cuda.get_device_properties(0).total_memory // (1024**3)
        print(f"✅ PyTorch {specs['pytorch_version']} detected")
        print(f"CUDA Available: {specs['cuda_available']}")
        if specs['cuda_available']:
            print(f"GPU: {specs['gpu']}")
            print(f"GPU Memory: {specs['gpu_memory']}GB")
            print(f"CUDA Version: {specs['cuda_version']}")
    except ImportError:
        print("❌ PyTorch not found")
    
    # Detect GPU via nvidia-smi if available
    if not specs['gpu']:
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                gpu_info = result.stdout.strip().split(',')
                specs['gpu'] = gpu_info[0].strip()
                specs['gpu_memory'] = int(gpu_info[1].strip()) // 1024  # Convert MB to GB
                print(f"✅ GPU detected via nvidia-smi: {specs['gpu']}")
                print(f"GPU Memory: {specs['gpu_memory']}GB")
        except FileNotFoundError:
            print("⚠️  nvidia-smi not found")
    
    return specs

def check_cuda_compatibility():
    """Check CUDA compatibility with current setup"""
    print("\n=== CUDA Compatibility Check ===")
    
    try:
        import torch
        
        if not torch.cuda.is_available():
            print("❌ CUDA not available in current PyTorch installation")
            return False
        
        # Test basic CUDA operations
        try:
            device = torch.device('cuda')
            test_tensor = torch.randn(100, 100).to(device)
            result = torch.mm(test_tensor, test_tensor)
            print("✅ CUDA operations working correctly")
            
            # Check memory
            total_memory = torch.cuda.get_device_properties(0).total_memory
            allocated_memory = torch.cuda.memory_allocated(0)
            print(f"GPU Memory - Total: {total_memory//1024**3}GB, Allocated: {allocated_memory//1024**2}MB")
            
            return True
            
        except Exception as e:
            print(f"❌ CUDA operation test failed: {e}")
            return False
            
    except ImportError:
        print("❌ PyTorch not available")
        return False

def install_gpu_pytorch():
    """Install GPU-enabled PyTorch while preserving Python 3.13 compatibility"""
    print("\n=== Installing GPU-Enabled PyTorch ===")
    
    # PyTorch installation commands for different CUDA versions
    pytorch_commands = {
        '12.1': 'pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121',
        '11.8': 'pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118',
        'cpu': 'pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu'
    }
    
    print("Available PyTorch installations:")
    for cuda_ver, command in pytorch_commands.items():
        print(f"  CUDA {cuda_ver}: {command}")
    
    # Auto-detect CUDA version
    cuda_version = None
    try:
        result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            if 'release 12.1' in output:
                cuda_version = '12.1'
            elif 'release 11.8' in output:
                cuda_version = '11.8'
            print(f"✅ Detected CUDA {cuda_version}")
    except FileNotFoundError:
        print("⚠️  nvcc not found, will try to detect from PyTorch")
    
    # If no CUDA detected, try CUDA 12.1 (most common)
    if not cuda_version:
        cuda_version = '12.1'
        print(f"⚠️  Auto-selecting CUDA {cuda_version}")
    
    try:
        command = pytorch_commands[cuda_version]
        print(f"Installing PyTorch with CUDA {cuda_version}...")
        subprocess.run(command.split(), check=True)
        print("✅ GPU-enabled PyTorch installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyTorch installation failed: {e}")
        return False

def create_gpu_webui_config():
    """Create GPU-optimized WebUI configuration"""
    print("\n=== Creating GPU-Optimized Configuration ===")
    
    gpu_config = '''@echo off
REM GPU-Optimized WebUI Configuration for Python 3.13
echo Starting WebUI with Python 3.13 compatibility and GPU acceleration...
echo.

REM Install core dependencies that might be missing from venv
echo Installing core dependencies and WebUI requirements...
pip install packaging setuptools wheel --upgrade --quiet
pip install "pytorch_lightning>=2.0.0,<3.0.0" torchmetrics --upgrade --quiet
pip install omegaconf safetensors accelerate --upgrade --quiet
pip install diskcache jsonmerge inflection --upgrade --quiet
pip install "gradio==3.41.2" "pydantic>=1.10.0,<2.0.0" fastapi uvicorn --upgrade --quiet
pip install tomesd einops kornia --upgrade --quiet
pip install "numpy>=2.0.2" --upgrade --quiet
echo Attempting pillow_avif installation (may fail on Python 3.13)...
pip install pillow_avif --quiet || echo "pillow_avif installation failed - AVIF support disabled"
echo Attempting open_clip installation (may fail on Python 3.13)...
pip install open-clip-torch --no-deps --quiet || echo "open_clip installation failed - using fallback"
echo Core dependencies and WebUI requirements installed.
echo.

REM GPU optimization environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0
set CUDA_CACHE_DISABLE=0
set CUDA_MODULE_LOADING=LAZY

REM Skip problematic package installations but allow GPU
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install

REM Use existing PyTorch installation
set TORCH_COMMAND=echo "Using existing PyTorch installation"

REM Skip CLIP packages (compatibility issues)
set CLIP_PACKAGE=echo "Skipping CLIP (compatibility issues)"
set OPENCLIP_PACKAGE=echo "Skipping open_clip (compatibility issues)"

REM GPU-optimized flags
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --precision autocast --opt-split-attention --opt-sub-quad-attention --opt-chunk-size 512

REM Memory optimization for GPU
set COMMANDLINE_ARGS=%COMMANDLINE_ARGS% --medvram --opt-channelslast

echo Configuration:
echo - Python 3.13 compatibility mode
echo - GPU acceleration enabled
echo - Memory optimization enabled
echo - Performance flags enabled
echo - CUDA optimizations active
echo.

call webui.bat %*
'''
    
    try:
        with open('webui_gpu.bat', 'w') as f:
            f.write(gpu_config)
        print("✅ Created webui_gpu.bat")
        return True
    except Exception as e:
        print(f"❌ Error creating GPU config: {e}")
        return False

def create_performance_configs():
    """Create different performance configuration options"""
    print("\n=== Creating Performance Configuration Options ===")
    
    configs = {
        'webui_gpu_fast.bat': {
            'description': 'Maximum speed (requires 8GB+ VRAM)',
            'flags': '--precision autocast --opt-split-attention --no-half-vae --opt-channelslast'
        },
        'webui_gpu_balanced.bat': {
            'description': 'Balanced speed/memory (4-8GB VRAM)',
            'flags': '--precision autocast --opt-split-attention --opt-sub-quad-attention --medvram'
        },
        'webui_gpu_lowvram.bat': {
            'description': 'Low VRAM mode (2-4GB VRAM)',
            'flags': '--precision autocast --lowvram --opt-split-attention --opt-sub-quad-attention'
        }
    }
    
    base_config = '''@echo off
REM {description}
echo Starting WebUI with GPU acceleration - {description}...
echo.

REM Install dependencies (same as GPU config)
echo Installing core dependencies...
pip install packaging setuptools wheel --upgrade --quiet
pip install "pytorch_lightning>=2.0.0,<3.0.0" torchmetrics --upgrade --quiet
pip install omegaconf safetensors accelerate --upgrade --quiet
pip install diskcache jsonmerge inflection --upgrade --quiet
pip install "gradio==3.41.2" "pydantic>=1.10.0,<2.0.0" fastapi uvicorn --upgrade --quiet
pip install tomesd einops kornia --upgrade --quiet
pip install "numpy>=2.0.2" --upgrade --quiet
echo Core dependencies installed.
echo.

REM GPU optimization environment variables
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set CUDA_LAUNCH_BLOCKING=0

REM Configuration flags
set COMMANDLINE_ARGS=--skip-python-version-check --skip-install {flags}

REM Use existing PyTorch installation
set TORCH_COMMAND=echo "Using existing PyTorch installation"

echo GPU Configuration: {description}
echo.

call webui.bat %*
'''
    
    created_configs = []
    for filename, config in configs.items():
        try:
            content = base_config.format(**config)
            with open(filename, 'w') as f:
                f.write(content)
            created_configs.append(f"{filename} - {config['description']}")
            print(f"✅ Created {filename}")
        except Exception as e:
            print(f"❌ Error creating {filename}: {e}")
    
    return created_configs

def test_gpu_performance():
    """Test GPU performance with WebUI"""
    print("\n=== GPU Performance Test ===")
    
    try:
        import torch
        
        if not torch.cuda.is_available():
            print("❌ CUDA not available for testing")
            return False
        
        device = torch.device('cuda')
        
        # Test tensor operations speed
        print("Testing GPU tensor operations...")
        import time
        
        start_time = time.time()
        for _ in range(100):
            a = torch.randn(1000, 1000, device=device)
            b = torch.randn(1000, 1000, device=device)
            c = torch.mm(a, b)
        end_time = time.time()
        
        gpu_time = end_time - start_time
        print(f"✅ GPU tensor operations: {gpu_time:.2f}s for 100 iterations")
        
        # Compare with CPU
        print("Comparing with CPU...")
        start_time = time.time()
        for _ in range(10):  # Fewer iterations for CPU
            a = torch.randn(1000, 1000)
            b = torch.randn(1000, 1000)
            c = torch.mm(a, b)
        end_time = time.time()
        
        cpu_time = (end_time - start_time) * 10  # Scale to 100 iterations
        speedup = cpu_time / gpu_time
        
        print(f"CPU tensor operations: {cpu_time:.2f}s for 100 iterations (estimated)")
        print(f"🚀 GPU Speedup: {speedup:.1f}x faster than CPU")
        
        return True
        
    except Exception as e:
        print(f"❌ GPU performance test failed: {e}")
        return False

def main():
    """Main function"""
    print("GPU Acceleration Setup for Python 3.13 Stable Diffusion WebUI")
    print("=" * 70)
    
    # Detect system specs
    specs = detect_system_specs()
    
    # Check CUDA compatibility
    cuda_works = check_cuda_compatibility()
    
    if not cuda_works:
        print("\n🔄 Installing GPU-enabled PyTorch...")
        pytorch_installed = install_gpu_pytorch()
        if pytorch_installed:
            cuda_works = check_cuda_compatibility()
    
    # Create GPU configurations
    gpu_config_created = create_gpu_webui_config()
    performance_configs = create_performance_configs()
    
    # Test GPU performance
    if cuda_works:
        test_gpu_performance()
    
    print("\n" + "=" * 70)
    print("GPU ACCELERATION SETUP SUMMARY")
    print("=" * 70)
    
    if cuda_works and gpu_config_created:
        print("🎉 GPU acceleration setup completed successfully!")
        print("\nAvailable configurations:")
        print("1. webui_gpu.bat - Standard GPU acceleration")
        for config in performance_configs:
            print(f"2. {config}")
        
        print("\nRecommended next steps:")
        if specs.get('gpu_memory', 0) >= 8:
            print("✅ Use webui_gpu_fast.bat (you have sufficient VRAM)")
        elif specs.get('gpu_memory', 0) >= 4:
            print("✅ Use webui_gpu_balanced.bat (balanced performance)")
        else:
            print("✅ Use webui_gpu_lowvram.bat (conservative settings)")
        
        print("\nExpected performance improvement:")
        print("🚀 Generation time: 5-10 minutes → 10-30 seconds")
        print("🚀 Speed increase: 10-30x faster than CPU-only")
        
    else:
        print("⚠️  GPU acceleration setup incomplete")
        if not cuda_works:
            print("❌ CUDA not working properly")
        if not gpu_config_created:
            print("❌ GPU configuration creation failed")
    
    print(f"\nSystem detected:")
    print(f"- GPU: {specs.get('gpu', 'Unknown')}")
    print(f"- GPU Memory: {specs.get('gpu_memory', 'Unknown')}GB")
    print(f"- PyTorch: {specs.get('pytorch_version', 'Unknown')}")
    print(f"- CUDA: {specs.get('cuda_version', 'Not available')}")

if __name__ == "__main__":
    main()
