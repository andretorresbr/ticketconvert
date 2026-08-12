@echo off
setlocal enabledelayedexpansion

echo.
echo  ticket_convert builder
echo  =============================================
echo.

:: ── Check Python ──────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [-] Python not found in PATH.
    echo     Install Python 3.8+ and make sure it is added to PATH.
    pause & exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo [*] Found: %%v

echo.

:: ── Install dependencies ──────────────────────────────────────────────────
echo [*] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [-] pip install failed. Check your internet connection.
    pause & exit /b 1
)
echo [+] Dependencies OK
echo.

:: ── Build ─────────────────────────────────────────────────────────────────
echo [*] Running PyInstaller...
echo.

pyinstaller ^
    --onefile ^
    --console ^
    --name ticket_convert ^
    --hidden-import impacket.krb5.ccache ^
    --hidden-import impacket.krb5.asn1 ^
    --hidden-import impacket.krb5.types ^
    --hidden-import impacket.krb5.constants ^
    --hidden-import impacket.krb5.crypto ^
    --hidden-import impacket.structure ^
    --hidden-import pyasn1 ^
    --hidden-import pyasn1.type ^
    --hidden-import pyasn1.codec.der ^
    --hidden-import pyasn1_modules ^
    --collect-submodules impacket ^
    ticket_convert.py

echo.
if exist dist\ticket_convert.exe (
    echo [+] ============================================
    echo [+]  Build successful!
    echo [+]  dist\ticket_convert.exe
    echo [+] ============================================
    echo.
    echo  Quick test:
    echo    dist\ticket_convert.exe --help
    echo    dist\ticket_convert.exe --version
) else (
    echo [-] Build failed. Review the PyInstaller output above.
    pause & exit /b 1
)

pause
endlocal
