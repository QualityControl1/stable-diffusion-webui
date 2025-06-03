#!/usr/bin/env python3
"""
RTX 3080 Performance Test (No xFormers)

Quick test to verify GPU acceleration performance.
"""

import time
import torch

def test_rtx3080_performance():
    print("RTX 3080 Performance Test (Standard Attention)")
    print("=" * 50)
    
    if not torch.cuda.is_available():
        print("ERROR: CUDA not available")
        return
    
    device = torch.device('cuda')
    gpu_name = torch.cuda.get_device_name(0)
    vram_total = torch.cuda.get_device_properties(0).total_memory // 1024**3
    
    print(f"GPU: {gpu_name}")
    print(f"VRAM: {vram_total}GB")
    print(f"PyTorch: {torch.__version__}")
    print()
    
    # Test matrix operations (attention-like)
    print("Testing matrix operations...")
    start_time = time.time()
    for _ in range(50):
        a = torch.randn(512, 512, device=device)
        b = torch.randn(512, 512, device=device)
        c = torch.mm(a, b)
        torch.cuda.synchronize()
    matrix_time = time.time() - start_time
    
    # Test convolution operations (diffusion-like)
    print("Testing convolution operations...")
    conv = torch.nn.Conv2d(32, 64, 3, padding=1).to(device)
    start_time = time.time()
    for _ in range(25):
        x = torch.randn(2, 32, 64, 64, device=device)
        y = conv(x)
        torch.cuda.synchronize()
    conv_time = time.time() - start_time
    
    print(f"\nResults:")
    print(f"Matrix operations: {matrix_time:.2f}s")
    print(f"Convolution operations: {conv_time:.2f}s")
    
    # Memory usage
    allocated = torch.cuda.memory_allocated(0) // 1024**2
    cached = torch.cuda.memory_reserved(0) // 1024**2
    
    print(f"\nMemory usage:")
    print(f"Allocated: {allocated}MB")
    print(f"Cached: {cached}MB")
    
    # Performance prediction
    print(f"\nPredicted WebUI performance:")
    if matrix_time < 3.0 and conv_time < 4.0:
        print("EXCELLENT: 25-35 seconds per 512x512 image")
    elif matrix_time < 5.0 and conv_time < 7.0:
        print("GOOD: 35-45 seconds per 512x512 image")
    else:
        print("MODERATE: 45-60 seconds per 512x512 image")
    
    print("\nNote: Without xFormers, expect standard attention performance")
    print("This is still 15-25x faster than CPU-only mode!")

if __name__ == "__main__":
    test_rtx3080_performance()
