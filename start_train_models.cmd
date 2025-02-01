@echo off
setlocal

rem Define arrays for models and datasets
set models=neural rf svm
set datasets=UPB2011 UPB2012 UPB2015 Haggle-Cambridge Haggle-Content Haggle-Infocom2006 Haggle-Intel NCCU Sigcomm SocialBlueConn StAndrews

rem Loop over datasets
for %%d in (%datasets%) do (
    rem Loop over models
    for %%m in (%models%) do (
        rem Open a new cmd window and run the script
        start cmd.exe /K "cd ~\Documents\facultate\mobemu && .venv\Scripts\Activate.ps1 && set MODEL=%%m&& set DATASET=%%d&& python train_model.py"
    )
)

endlocal
