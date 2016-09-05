@echo off
  
  :: TODO:安装minghu6 Pacage
 

  color 03
  set input=
  set /p "input=请输入minghu6 Pacage所在的目标位置（或回车默认路径为它所在的当前路径）:"
  if defined input (xcopy /E /I ..\minghu6 %input%\minghu6) else ( set input="." )

 python auto_install.py %input%

 ::判断python版本是否正确,0 -successful 1-failed
 if %ERRORLEVEL% == 1 (pause && echo Now try to run python3) else (echo minghu6 Pacage安装路径为%input% && echo Install successful! && exit)

 python3 auto_install.py %input%
 if %ERRORLEVEL% == 0 (echo minghu6 Pacage安装路径为%input% && echo Install successful!) else (echo install Failed)
 

pause