@ECHO OFF
echo 正在停止Nginx进程......
plugin\Process -k nginx.exe
plugin\Process -k nginx.exe
del /Q /F nginx\logs\nginx.pid
echo 正在停止PHP(FastCGI)进程......
plugin\Process -k php-cgi.exe
plugin\Process -k mysqld.exe
del /Q /F mariadb\data\%COMPUTERNAME%.pid