set WATCH_DOG_APP_NAME=Diablo III
set WATCH_DOG_SCRENSHOTS_DIR=%temp%
set WATCH_DOG_LOG_FILE=z:\_DRIVE_Z\Documents\RoS-BoT\Logs\logs.txt


rem set WATCH_DOG_APP_NAME=Hearthstone
rem set WATCH_DOG_SCRENSHOTS_DIR=%temp%
rem set HEARTHRANGER_LOG_DIR=C:\GAMEBOTS\HearthRangerBot\log\
rem FOR /F "delims=|" %%I IN ('DIR "%HEARTHRANGER_LOG_DIR%*" /B /O:D') DO SET NEWEST_LOG=%%I
rem set WATCH_DOG_LOG_FILE=%HEARTHRANGER_LOG_DIR%%NEWEST_LOG%



set WATCH_DOG_HOME=%~dp0
set SIKULIX_HOME=%WATCH_DOG_HOME%\_portable\Sikuli\
set PARMS=-Xms64M -Xmx512M -Dfile.encoding=UTF-8 -Dsikuli.FromCommandLine -Djava.library.path="%SIKULIX_HOME%libs" 
set JAVA_HOME=%WATCH_DOG_HOME%\_portable\Java
set SIKULI_COMMAND=-r BotWatchDog.sikuli 
PATH=%PATH%;%SIKULIX_HOME%libs;%JAVA_HOME%\bin

"%JAVA_HOME%\bin\java.exe" %PARMS% -jar "%SIKULIX_HOME%sikulix.jar" %SIKULI_COMMAND%
