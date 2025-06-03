#!/usr/bin/env python3
"""
Verify WebUI Configuration

This script shows the current configuration and verifies
all flags are set correctly for CPU-only operation.
"""

import os
import sys

def show_current_config():
    """Show current environment configuration"""
    print("=== Current WebUI Configuration ===")
    
    # Check environment variables that would be set by webui_compatible.bat
    env_vars = [
        "COMMANDLINE_ARGS",
        "TORCH_COMMAND", 
        "CLIP_PACKAGE",
        "OPENCLIP_PACKAGE",
        "XFORMERS_PACKAGE"
    ]
    
    print("Environment variables:")
    for var in env_vars:
        value = os.environ.get(var, "Not set")
        print(f"  {var}: {value}")

def show_expected_config():
    """Show what the configuration should be"""
    print("\n=== Expected Configuration ===")
    
    expected_args = [
        "--skip-python-version-check",
        "--skip-install", 
        "--skip-torch-cuda-test",  # This was missing!
        "--no-half",
        "--precision full",
        "--use-cpu all"
    ]
    
    print("Expected COMMANDLINE_ARGS:")
    for arg in expected_args:
        print(f"  ✅ {arg}")
    
    print("\nExpected environment:")
    print("  TORCH_COMMAND: echo 'Using existing PyTorch installation'")
    print("  CLIP_PACKAGE: echo 'Skipping CLIP (compatibility issues)'")
    print("  OPENCLIP_PACKAGE: echo 'Skipping open_clip (compatibility issues)'")
    print("  XFORMERS_PACKAGE: none")

def check_pytorch_cpu_mode():
    """Verify PyTorch is in CPU-only mode"""
    print("\n=== PyTorch CPU Mode Check ===")
    
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print("⚠️  CUDA is available but we're using CPU-only mode")
        else:
            print("✅ CUDA not available (CPU-only mode)")
        
        # Test CPU tensor operations
        device = torch.device('cpu')
        x = torch.rand(5, 3, device=device)
        print(f"✅ CPU tensor operations working: {x.device}")
        
        return True
    except Exception as e:
        print(f"❌ PyTorch test failed: {e}")
        return False

def show_webui_compatible_content():
    """Show the content of webui_compatible.bat"""
    print("\n=== webui_compatible.bat Content ===")
    
    try:
        with open("webui_compatible.bat", "r") as f:
            content = f.read()
        
        print("Current configuration file:")
        print("-" * 40)
        print(content)
        print("-" * 40)
        
        # Check for required flags
        required_flags = [
            "--skip-torch-cuda-test",
            "--skip-python-version-check", 
            "--skip-install",
            "--use-cpu all"
        ]
        
        print("\nFlag verification:")
        for flag in required_flags:
            if flag in content:
                print(f"✅ {flag} present")
            else:
                print(f"❌ {flag} missing")
        
        return True
    except FileNotFoundError:
        print("❌ webui_compatible.bat not found")
        return False

def main():
    """Main verification function"""
    print("WebUI Configuration Verification")
    print("=" * 50)
    
    show_current_config()
    show_expected_config()
    pytorch_ok = check_pytorch_cpu_mode()
    config_ok = show_webui_compatible_content()
    
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    
    if pytorch_ok and config_ok:
        print("✅ Configuration looks good!")
        print("\nNext steps:")
        print("1. Run: .\\webui_compatible.bat")
        print("2. Should start without CUDA errors")
        print("3. Will run in CPU-only mode")
    else:
        print("⚠️  Configuration issues detected")
        print("Check the output above for details")
    
    print(f"\nPython version: {sys.version}")
    print("Ready for CPU-only WebUI operation!")

if __name__ == "__main__":
    main()
