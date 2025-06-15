chcp 936

@echo off&color 1f&mode con cols=52 lines=26
pushd %~dp0 & cd /d "%~dp0"
:menu
cls
echo.
echo.====================================================
echo.   　Windows Server 2025 26100 24H2 版本互換
echo.====================================================
echo.
echo.           [1]   轉為Win11專业版 [可數字激活]
echo.
echo.           [2]   轉為Win11企业版 [可數字激活]
echo.
echo.           [3]   轉為Win11專业工作站版 [可數字激活]
echo.
echo.           [4]   轉Win Server2025版 [請KMS38激活]
echo.
echo.           [5]   重启電腦
echo.
echo.----------------------------------------------------
echo.轉WIN11後可解除部分軟件和驱動限制Server不能安裝問題
echo.----------------------------------------------------
echo.如需更新系統打補丁請轉回Win2025 Server,系統會更稳定
echo.----------------------------------------------------
echo.
choice /C:12345 /N /M "**請輸入1-5: [如退出請直接關閉本窗口]"
if errorlevel 1 (set "os=11" & set "key=W269N-WFGWX-YVC9B-4J6C9-T83GX"&set "EditionID=Professional"&set "winos=Win11專业版")
if errorlevel 2 (set "os=11" & set "key=NPPR9-FWDCX-D2C8J-H872K-2YT43"&set "EditionID=Enterprise"&set "winos=Win11企业版")
if errorlevel 3 (set "os=11" & set "key=NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J"&set "EditionID=ProfessionalWorkstation"&set "winos=Win11專业工作站版")
if errorlevel 4 (set "os=Win2025Datacenter" & set "key=D764K-2NDRG-47T6Q-P8T8W-YP6DF"&set "EditionID=ServerDatacenter"&set "winos=Win2025數據中心版")
if errorlevel 5  cls & echo 按任意键將重启電腦[如不想重启請直接關閉本窗口]… & pause> nul&shutdown /r /f /t 1 & exit
cls
echo.
rem 判斷系統是否存在轉換文件,存在就跳轉到ChangeAuthority
if exist "%windir%\BrandingWin11.24H2.26100" (
goto ChangeAuthority
)
echo 首次轉換,備份原系統skus和Branding…
takeown /f "%windir%\System32\spp\tokens\skus" /r /d y  > nul
icacls "%windir%\System32\spp\tokens\skus" /grant:r administrators:F /T > nul
takeown /f "%windir%\Branding" /r /d y > nul
icacls "%windir%\Branding" /grant:r administrators:F /T > nul
xcopy "%windir%\System32\spp\tokens\skus" "%windir%\System32\spp\tokens\skusB" /q /s /e /c /i /y > nul
ren "%windir%\Branding" "BrandingB"  > nul
echo 首次轉換,拷贝轉換版本所需的文件到系統…
xcopy "%~dp0skus-24H2.26100" "%windir%\System32\spp\tokens\skus" /q /s /e /c /i /y > nul
xcopy "%~dp0BrandingWin11.24H2.26100" "%windir%\BrandingWin11.24H2.26100" /q /s /e /c /i /y > nul
xcopy "%~dp0BrandingWin2025.24H2.26100" "%windir%\BrandingWin2025.24H2.26100" /q /s /e /c /i /y > nul
:ChangeAuthority
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v "CompositionEditionID" /t REG_SZ /d "%EditionID%" /f > nul
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v "EditionID" /t REG_SZ /d "%EditionID%" /f > nul
echo 請耐心等待安裝許可證,需2-5分钟…
cscript /nologo %SystemRoot%\System32\slmgr.vbs /rilc  > nul
if "%os%"=="Win2025Datacenter" goto Win2025Datacenter
echo 正在將系統轉換為%winos%,請等待…
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v "InstallationType" /t REG_SZ /d "Client" /f > nul
xcopy "%windir%\BrandingWin11.24H2.26100\*" "%windir%\Branding" /q /s /e /c /i /y > nul
cscript /nologo %SystemRoot%\System32\slmgr.vbs /ipk %key% |find "錯誤"&&(pause&exit)
echo 已將系統轉換為%winos%
echo 請重启電腦,完成%winos%的轉換
echo 按任意键返回主菜單…
start slmgr.vbs /xpr&winver
start mshta vbscript:msgbox("請重启電腦後,使系統完整的運行於轉換後的%winos%!!",64,"請重启電腦")(window.close)
pause> nul&goto :menu
:Win2025Datacenter
echo 正在將系統轉換為%winos%,請等待…
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v "InstallationType" /t REG_SZ /d "Server" /f > nul
xcopy "%windir%\BrandingWin2025.24H2.26100\*" "%windir%\Branding" /q /s /e /c /i /y > nul
cscript /nologo %SystemRoot%\System32\slmgr.vbs /ipk %key% |find "錯誤"&&(pause&exit)
echo 已將系統轉換為%winos%
echo 請重启電腦,完成%winos%的轉換
echo 按任意键返回主菜單…
start slmgr.vbs /xpr&winver
start mshta vbscript:msgbox("請重启電腦,使系統完整的運行於轉換後的%winos%!!",64,"請重启電腦")(window.close)
pause> nul&goto :menu
