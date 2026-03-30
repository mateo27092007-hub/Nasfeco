@echo off
echo ========================================
echo   NASFECO - Subiendo cambios a GitHub
echo ========================================
echo.
git add .
git commit -m "update: cambios automaticos %date% %time%"
git push origin main
echo.
echo ========================================
echo   Listo! Cambios subidos correctamente
echo ========================================
pause
