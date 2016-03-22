

#Usage

## Enviroment Variables
### RosBot
```
set WATCH_DOG_APP_NAME=Diablo III
set WATCH_DOG_SCRENSHOTS_DIR=%temp%
set WATCH_DOG_LOG_FILE="%userprofile%\my documents\ros-bot\rosbot.log" 
```

### HearthRanger

```
set WATCH_DOG_APP_NAME=Hearthstone
set WATCH_DOG_SCRENSHOTS_DIR=%temp%
set HEARTHRANGER_LOG_DIR=C:\GAMEBOTS\HearthRangerBot\log\
FOR /F "delims=|" %%I IN ('DIR "%HEARTHRANGER_LOG_DIR%*" /B /O:D') DO SET NEWEST_LOG=%%I
set WATCH_DOG_LOG_FILE=%HEARTHRANGER_LOG_DIR%%NEWEST_LOG%

```