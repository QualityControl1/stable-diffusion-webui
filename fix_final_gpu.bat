@echo off
echo Final RTX 3080 GPU Optimization
echo ================================
echo.
echo This will resolve the remaining issues:
echo - xFormers installation for PyTorch 2.7.0+cu118
echo - Unicode encoding error in launch script creation
echo - Create working GPU launch configuration
echo.

echo Running final GPU optimization...
python fix_final_gpu_issues.py

echo.
echo Final optimization completed!
echo.
echo Launch WebUI with: .\webui_gpu_rtx3080_final.bat
echo Test performance with: python test_gpu_performance.py
echo.
pause
