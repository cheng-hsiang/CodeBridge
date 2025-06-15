@echo off
REM CodeBridge GUI 構建腳本 (Windows)
echo 🌉 CodeBridge GUI 構建腳本
echo ==============================

REM 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: 找不到 Python，請先安裝 Python 3.6+
    pause
    exit /b 1
)

echo ✅ Python 環境檢查通過

REM 安裝構建依賴
echo.
echo 📦 安裝構建依賴...
python -m pip install -r build_requirements.txt
if errorlevel 1 (
    echo ❌ 依賴安裝失敗
    pause
    exit /b 1
)

REM 執行構建
echo.
echo 🔨 開始構建...
python build.py
if errorlevel 1 (
    echo ❌ 構建失敗
    pause
    exit /b 1
)

echo.
echo 🎉 構建完成！
echo.
echo 📁 構建產物位置:
echo   • dist\CodeBridge-GUI.exe
echo   • CodeBridge-GUI-*-windows.zip
echo.
echo 💡 提示: 請測試 exe 檔案功能是否正常
echo.
pause 