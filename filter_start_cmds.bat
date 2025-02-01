@echo off
setlocal enabledelayedexpansion

rem Define datasets
set datasets=UPB2011 UPB2012 UPB2015 Haggle-Intel Haggle-Cambridge Haggle-Content Haggle-Infocom2006 NCCU Sigcomm SocialBlueConn StAndrews

rem Loop through datasets
for %%d in (%datasets%) do (
    start cmd /k "cd %USERPROFILE%\Documents\facultate\mobemu && set DATASET=%%d&& .venv\Scripts\python.exe filter_useful_messages.py"
)

endlocal