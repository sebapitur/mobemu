@echo off
setlocal enabledelayedexpansion

set models=neural rf svm
set datasets=UPB2011 UPB2015 Haggle-Content Haggle-Infocom2006 NCCU Sigcomm

for %%d in (%datasets%) do (
    for %%m in (%models%) do (
        start cmd /k "cd %USERPROFILE%\Documents\facultate\mobemu && call .venv\Scripts\activate && set MODEL=%%m&& set DATASET=%%d&& python train_model.py"
    )
)

endlocal
