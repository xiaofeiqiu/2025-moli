@ECHO OFF
chcp 936 >nul
@cls
Color 0A
>"%tmp%\t.t" echo;WSH.Echo(/[\u4E00-\u9FFF]/.test(WSH.Arguments(0)))
for /f %%a in ('cscript -nologo -e:jscript "%tmp%\t.t" "%~dp0"') do if %%a neq 0 (goto ansierr) else goto startserver

:startserver
echo.
echo.
echo.
echo.
@echo  ****************************************************************************
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                            魔力宝贝cgmsv引擎                             *
@echo  *                              www.cgmsv.com                               *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *        切记使用 Ctrl + C 方式关闭服务端后填写 N 来关闭网站数据库!        *
@echo  *                                                                          *
@echo  *                  否则会导致游戏登录卡号或数据库异常!!!                   *
@echo  *                                                                          *
@echo  *                            5秒后开始启动引擎                             *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  ****************************************************************************
echo.
echo.
echo.
echo.
echo.
@ECHO OFF
cscript /nologo %~dp0nmp\plugin\sleep.vbs 5000
@cls
Color 07
%~d0
cd %~dp0
del /q gmsv\gmsvlog*
del /q gmsv\log\*.log
del /q gmsv\log\*20*
del /q gmsv\Dengon\*
del /q gmsv\store\dungeon\*
del /q gmsv\store\house\*
del /q gmsv\store\itemcount\*
::del /q gmsv\store\*.txt
del /q gmsv\store\dungeonnpc.txt
del /q gmsv\store\dungeonencount.txt
del /q gmsv\store\dungeontech_area.txt
del /q gmsv\store\mapjob.txt
del /q gmsv\store\activedungeon.txt
del /q gmsv\store\makeseq.txt
del /q gmsv\store\itembox.txt
del /q gmsv\store\petmail.txt
del /q gmsv\store\*itemgold*
del /q gmsv\dump\*
::del /q nmp\mariadb\data\*logfile*
::del /q nmp\mariadb\data\ibdata*
::del /q nmp\mariadb\data\*.err
cd %~dp0nmp
for /f "tokens=3 delims=: " %%a in ('netstat -an') do (
if "%%a"=="3306" goto mysqlcheck
)
:check80port
for /f "tokens=3 delims=: " %%a in ('netstat -an') do (
if "%%a"=="80" goto nginxcheck
)

:runnmp
@cls
Color 07
call %~dp0nmp\nmp_run.bat
@cls
Color 07
cd %~dp0gmsv
for /f "tokens=1* delims=[" %%a in ('ver') do set b=%%b
set b=%b:* =%
if "%b:~0,3%"=="5.1" goto winxp
start /b /WAIT /AFFINITY 0x3 %~dp0gmsv\cgmsv.exe
cd %~dp0nmp
call %~dp0nmp\nmp_stop.bat
@ECHO OFF
Color 0A
echo.
echo.
echo.
echo.
@echo  ****************************************************************************
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                      (服务端已经关闭,按任意键退出)                       *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  ****************************************************************************
echo.
echo.
echo.
echo.
@ECHO OFF
pause
exit

:winxp
start /b /WAIT %~dp0gmsv\cgmsv.exe
cd %~dp0nmp
call %~dp0nmp\nmp_stop.bat
@ECHO OFF
Color 0A
echo.
echo.
echo.
echo.
@echo  ****************************************************************************
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                      (服务端已经关闭,按任意键退出)                       *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  ****************************************************************************
echo.
echo.
echo.
echo.
@ECHO OFF
pause
exit

:mysqlcheck
tasklist | find /i "mysqld.exe"
if "%errorlevel%"=="1" (goto portused3306) else (goto check80port)

:nginxcheck
tasklist | find /i "nginx.exe"
if "%errorlevel%"=="1" (goto portused80) else (goto runnmp)

:portused3306
@ECHO OFF
Color 0A
@cls
echo.
echo.
echo.
echo.
@echo  ****************************************************************************
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                   检测到数据库所需的 3306 端口已被占用                   *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                 引擎将无法正常启动,请先处理端口占用问题                  *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                            (按任意键退出)                                *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  ****************************************************************************
echo.
echo.
echo.
echo.
echo.
@ECHO OFF
pause
exit

:portused80
@ECHO OFF
Color 0A
@cls
echo.
echo.
echo.
echo.
@echo  ****************************************************************************
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                      检测到网站所需的 80 端口已被占用                    *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                   引擎将继续启动,但注册网页可能无法使用!                 *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                         (请按任意键继续启动引擎)                         *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  ****************************************************************************
echo.
echo.
echo.
echo.
echo.
@ECHO OFF
pause
@cls
goto runnmp

:ansierr
@ECHO OFF
Color 0A
@cls
echo.
echo.
echo.
echo.
@echo  ****************************************************************************
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *           检测到服务端存放路径中含有中文,服务端将无法正常启动            *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *             请将服务端文件夹移动到不含中文的路径后中再启动               *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  *                                                                          *
@echo  ****************************************************************************
echo.
echo.
echo.
echo.
@ECHO OFF
pause
exit