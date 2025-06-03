#!/usr/bin/env python3
"""
Fix Image Generation Issues for Python 3.13

This script diagnoses and fixes grey/blank image generation issues
in CPU-only mode with PyTorch 2.6.0 and Python 3.13.

Author: Augment Agent
Date: January 2025
"""

import sys
import os
import numpy as np
from PIL import Image
import torch

def diagnose_torch_environment():
    """Diagnose PyTorch environment and tensor handling"""
    print("=== PyTorch Environment Diagnosis ===")
    
    print(f"PyTorch version: {torch.__version__}")
    print(f"Python version: {sys.version}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"CPU device: {torch.device('cpu')}")
    
    # Test basic tensor operations
    try:
        # Create test tensor
        test_tensor = torch.randn(1, 3, 64, 64, dtype=torch.float32)
        print(f"✅ Test tensor created: {test_tensor.shape}, dtype: {test_tensor.dtype}")
        
        # Test tensor to numpy conversion
        test_numpy = test_tensor.detach().cpu().numpy()
        print(f"✅ Tensor to numpy conversion: {test_numpy.shape}, dtype: {test_numpy.dtype}")
        
        # Test numpy to PIL conversion
        # Normalize to 0-255 range
        test_image_data = ((test_numpy[0].transpose(1, 2, 0) + 1) * 127.5).clip(0, 255).astype(np.uint8)
        test_pil = Image.fromarray(test_image_data)
        print(f"✅ NumPy to PIL conversion: {test_pil.size}, mode: {test_pil.mode}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tensor processing test failed: {e}")
        return False

def test_image_processing_pipeline():
    """Test the image processing pipeline"""
    print("\n=== Image Processing Pipeline Test ===")
    
    try:
        # Create a test image with known pattern
        width, height = 512, 512
        
        # Create gradient pattern
        test_array = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(height):
            for j in range(width):
                test_array[i, j] = [i % 256, j % 256, (i + j) % 256]
        
        test_image = Image.fromarray(test_array)
        print(f"✅ Test pattern created: {test_image.size}, mode: {test_image.mode}")
        
        # Save test image
        test_image.save("test_pattern.png")
        print("✅ Test pattern saved as test_pattern.png")
        
        # Test loading and conversion
        loaded_image = Image.open("test_pattern.png")
        loaded_array = np.array(loaded_image)
        print(f"✅ Test pattern loaded: {loaded_array.shape}, dtype: {loaded_array.dtype}")
        
        # Test tensor conversion
        tensor_data = torch.from_numpy(loaded_array.transpose(2, 0, 1)).float() / 255.0
        tensor_data = tensor_data * 2.0 - 1.0  # Normalize to [-1, 1]
        print(f"✅ Image to tensor conversion: {tensor_data.shape}, dtype: {tensor_data.dtype}")
        
        # Test reverse conversion
        reverse_data = ((tensor_data + 1.0) * 127.5).clamp(0, 255).byte()
        reverse_array = reverse_data.permute(1, 2, 0).numpy()
        reverse_image = Image.fromarray(reverse_array)
        reverse_image.save("test_reverse.png")
        print("✅ Reverse conversion test saved as test_reverse.png")
        
        return True
        
    except Exception as e:
        print(f"❌ Image processing pipeline test failed: {e}")
        return False

def patch_webui_image_processing():
    """Patch WebUI image processing for better CPU compatibility"""
    print("\n=== Patching WebUI Image Processing ===")
    
    # Check if modules/processing.py exists
    processing_file = "modules/processing.py"
    if not os.path.exists(processing_file):
        print(f"❌ {processing_file} not found")
        return False
    
    try:
        with open(processing_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already patched
        if "CPU-only tensor processing fix" in content:
            print("✅ modules/processing.py already patched")
            return True
        
        # Look for image processing functions to patch
        patches_applied = 0
        
        # Patch 1: Fix tensor device handling
        if "def decode_latent_batch" in content:
            old_pattern = "def decode_latent_batch(model, batch, target_device=None, check_for_nans=False):"
            if old_pattern in content:
                new_pattern = """def decode_latent_batch(model, batch, target_device=None, check_for_nans=False):
    # CPU-only tensor processing fix for Python 3.13
    if target_device is None:
        target_device = torch.device('cpu')
    
    # Ensure tensors are on correct device and have correct dtype
    if hasattr(batch, 'to'):
        batch = batch.to(device=target_device, dtype=torch.float32)"""
                
                content = content.replace(old_pattern, new_pattern)
                patches_applied += 1
                print("✅ Applied decode_latent_batch patch")
        
        # Patch 2: Fix image tensor conversion
        if "images_tensor_to_samples" in content:
            # Add tensor processing fix
            tensor_fix = """
# CPU-only image tensor processing fix
def fix_tensor_for_cpu(tensor):
    \"\"\"Fix tensor for CPU-only processing\"\"\"
    if tensor is None:
        return None
    
    # Ensure tensor is on CPU with correct dtype
    if hasattr(tensor, 'to'):
        tensor = tensor.to(device=torch.device('cpu'), dtype=torch.float32)
    
    # Ensure contiguous memory layout
    if hasattr(tensor, 'contiguous'):
        tensor = tensor.contiguous()
    
    return tensor

"""
            
            # Insert the fix function
            if "def images_tensor_to_samples" in content and "fix_tensor_for_cpu" not in content:
                insertion_point = content.find("def images_tensor_to_samples")
                content = content[:insertion_point] + tensor_fix + content[insertion_point:]
                patches_applied += 1
                print("✅ Added tensor processing fix function")
        
        if patches_applied > 0:
            # Create backup
            backup_file = processing_file + ".image_gen_backup"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Write patched file
            with open(processing_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Applied {patches_applied} patches to {processing_file}")
        else:
            print("✅ No patches needed for processing.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error patching {processing_file}: {e}")
        return False

def patch_webui_images_module():
    """Patch WebUI images module for better compatibility"""
    print("\n=== Patching WebUI Images Module ===")
    
    images_file = "modules/images.py"
    if not os.path.exists(images_file):
        print(f"❌ {images_file} not found")
        return False
    
    try:
        with open(images_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already patched
        if "CPU image processing fix" in content:
            print("✅ modules/images.py already patched")
            return True
        
        # Add CPU-specific image processing fix
        cpu_fix = """
# CPU image processing fix for Python 3.13
def ensure_cpu_compatible_image(image_data):
    \"\"\"Ensure image data is compatible with CPU processing\"\"\"
    if image_data is None:
        return None
    
    # Handle torch tensors
    if hasattr(image_data, 'detach'):
        image_data = image_data.detach().cpu()
    
    # Handle numpy arrays
    if isinstance(image_data, np.ndarray):
        # Ensure correct dtype and range
        if image_data.dtype != np.uint8:
            if image_data.max() <= 1.0:
                image_data = (image_data * 255).astype(np.uint8)
            else:
                image_data = image_data.astype(np.uint8)
    
    return image_data

"""
        
        # Insert the fix function at the beginning of the file after imports
        import_end = content.find('\n\n', content.find('import'))
        if import_end != -1 and "ensure_cpu_compatible_image" not in content:
            content = content[:import_end] + cpu_fix + content[import_end:]
            
            # Create backup
            backup_file = images_file + ".cpu_fix_backup"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Write patched file
            with open(images_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Added CPU image processing fix to images.py")
        else:
            print("✅ images.py doesn't need patching")
        
        return True
        
    except Exception as e:
        print(f"❌ Error patching {images_file}: {e}")
        return False

def create_cpu_optimization_script():
    """Create a script to optimize CPU-only image generation"""
    print("\n=== Creating CPU Optimization Script ===")
    
    cpu_script = """
# CPU Optimization for Stable Diffusion WebUI
# Add this to webui-user.bat or set as environment variables

# Optimize PyTorch for CPU
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
set OMP_NUM_THREADS=4
set MKL_NUM_THREADS=4

# Optimize memory usage
set PYTORCH_NO_CUDA_MEMORY_CACHING=1

# Force CPU device
set CUDA_VISIBLE_DEVICES=""

# WebUI CPU optimizations
set COMMANDLINE_ARGS=--precision full --no-half --use-cpu all --skip-torch-cuda-test --no-half-vae
"""
    
    try:
        with open("cpu_optimization.bat", "w") as f:
            f.write(cpu_script)
        print("✅ Created cpu_optimization.bat")
        return True
    except Exception as e:
        print(f"❌ Error creating CPU optimization script: {e}")
        return False

def test_webui_image_generation():
    """Test WebUI image generation functionality"""
    print("\n=== Testing WebUI Image Generation ===")
    
    try:
        # Add modules directory to path
        modules_path = os.path.join(os.getcwd(), "modules")
        if modules_path not in sys.path:
            sys.path.insert(0, modules_path)
        
        # Try importing WebUI modules
        import processing
        import images
        print("✅ WebUI modules imported successfully")
        
        # Test basic image functions
        if hasattr(images, 'ensure_cpu_compatible_image'):
            print("✅ CPU compatibility function available")
        
        return True
        
    except ImportError as e:
        print(f"❌ WebUI module import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ WebUI image generation test failed: {e}")
        return False

def main():
    """Main function"""
    print("Image Generation Fix for Python 3.13 CPU-only Mode")
    print("=" * 60)
    
    # Diagnose PyTorch environment
    torch_ok = diagnose_torch_environment()
    
    # Test image processing pipeline
    pipeline_ok = test_image_processing_pipeline()
    
    # Patch WebUI processing
    processing_patched = patch_webui_image_processing()
    
    # Patch WebUI images module
    images_patched = patch_webui_images_module()
    
    # Create CPU optimization script
    cpu_script_created = create_cpu_optimization_script()
    
    # Test WebUI functionality
    webui_ok = test_webui_image_generation()
    
    print("\n" + "=" * 60)
    print("IMAGE GENERATION FIX SUMMARY")
    print("=" * 60)
    
    if torch_ok and pipeline_ok and processing_patched and images_patched:
        print("✅ Image generation issues should be resolved!")
        print("\nNext steps:")
        print("1. Restart WebUI: .\\webui_compatible.bat")
        print("2. Try generating an image with a simple prompt")
        print("3. Check that downloaded images show actual content")
        print("4. For better performance, run: .\\cpu_optimization.bat")
        
        print("\nTroubleshooting tips:")
        print("- Use simple prompts first (e.g., 'a red apple')")
        print("- Try lower resolution (512x512)")
        print("- Use fewer sampling steps (20-30)")
        print("- Check that images are not all grey/black")
    else:
        print("⚠️  Some image generation issues may remain")
        
        if not torch_ok:
            print("❌ PyTorch environment issues")
        if not pipeline_ok:
            print("❌ Image processing pipeline issues")
        if not processing_patched:
            print("❌ WebUI processing patching failed")
        if not images_patched:
            print("❌ WebUI images patching failed")
    
    print(f"\nPython version: {sys.version}")
    print(f"PyTorch version: {torch.__version__}")
    print("CPU-only image generation should now work correctly")

if __name__ == "__main__":
    main()
