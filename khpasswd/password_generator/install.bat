@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Пожалуйста, запустите этот файл от имени Администратора!
    pause
    exit /b
)

copy kh_passwd C:\Windows\kh_passwd.py >nul

echo @python C:\Windows\kh_passwd.py %%* > C:\Windows\kh_passwd.bat

echo ----------------------------------------
echo Установка в Windows завершена успешно!
echo Теперь команда kh_passwd доступна в cmd/PowerShell.
echo ----------------------------------------
pause
