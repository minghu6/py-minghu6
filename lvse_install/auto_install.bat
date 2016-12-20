@echo off
  
  :: TODO:Install minghu6 Pacage, and minghu6_shell
 

  color 03
  set input=
  set /p "input=Please input minghu6 Pacage target directory(or press return for default current directorey):"
  if defined input (xcopy /E /I ..\minghu6 %input%\minghu6) else (set input="." )
  xcopy /E /I ..\minghu6_shell %input%\minghu6_shell
  xcopy /E /I ..\minghu6_shell %input%\resources

 python auto_install.py %input%

 ::check up python version ,0 -successful 1-failed
 if %ERRORLEVEL% == 1 (pause && echo Now try to run python3) else (echo minghu6 Pacage Installed Path %input% && echo Install successful! && exit)

 python3 auto_install.py %input%
 if %ERRORLEVEL% == 0 (echo minghu6 PacageInstalled Path%input% && echo Install successful!) else (echo install Failed)
 

pause