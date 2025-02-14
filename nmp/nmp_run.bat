@ECHO OFF
plugin\Process -k nginx.exe
plugin\Process -k nginx.exe
del /Q /F nginx\logs\nginx.pid
plugin\Process -k php-cgi.exe
plugin\Process -k mysqld.exe
del /Q /F mariadb\data\%COMPUTERNAME%.pid

set "HKLMU=HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\"
reg query %HKLMU%{9A25302D-30C0-39D9-BD6F-21E6EC160475}>nul 2>nul&&set VC9=Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.17
set "HKLMU=HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\"
reg query %HKLMU%{9A25302D-30C0-39D9-BD6F-21E6EC160475}>nul 2>nul&&set VC9=Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.17

if defined VC9 (goto:startnginx) else (goto VC9Install)
:VC9Install
echo 正在安装 Microsoft Visual C++ 2008 Redistributable
vcredist_x86.exe /q

:startnginx
if exist nginx\logs\nginx.pid goto startmariadb
echo 正在启动Nginx进程......
cd ./nginx
"../plugin/RunHiddenConsole.exe" nginx.exe -c conf/nginx.conf
cd ..

:startmariadb
if exist mariadb\data\%COMPUTERNAME%.pid goto startphp
echo 正在启动MySQL进程......
plugin\RunHiddenConsole.exe  mariadb\bin\mysqld.exe

:startphp
echo 正在启动php(FastCGI)进程......
plugin\RunHiddenConsole.exe  php\php-cgi.exe -b 127.0.0.1:9000 -c php\php.ini
mariadb\bin\mysql.exe -uroot -proot -e "use cgmsv;delete from tbl_lock;delete from tbl_lock2;"