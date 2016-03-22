set WATCH_DOG_APP_NAME=Hearthstone
set WATCH_DOG_SCRENSHOTS_DIR=%temp%
set HEARTHRANGER_LOG_DIR=C:\GAMEBOTS\HearthRangerBot\log\
FOR /F "delims=|" %%I IN ('DIR "%HEARTHRANGER_LOG_DIR%*" /B /O:D') DO SET NEWEST_LOG=%%I
set WATCH_DOG_LOG_FILE=%HEARTHRANGER_LOG_DIR%%NEWEST_LOG%



set WATCH_DOG_HOME=%~dp0
set SIKULIX_HOME=%WATCH_DOG_HOME%\_portable\Sikuli\
set PARMS=-Xms64M -Xmx512M -Dfile.encoding=UTF-8 -Dsikuli.FromCommandLine -Djava.library.path="%SIKULIX_HOME%libs" -Dsikuli.Debug=3
set JAVA_HOME=%WATCH_DOG_HOME%\_portable\Java
set SIKULI_COMMAND=-r BotWatchDog.sikuli 
PATH=%PATH%;%SIKULIX_HOME%libs;%JAVA_HOME%\bin

"%JAVA_HOME%\bin\java.exe" %PARMS% -jar "%SIKULIX_HOME%sikulix.jar" %SIKULI_COMMAND%
