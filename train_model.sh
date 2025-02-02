#!/bin/bash

# models=("neural" "rf" "svm")
models=("neural" "svm")
# datasets=("UPB2011" "UPB2012" "UPB2015" 
#           "Haggle-Cambridge" "Haggle-Content" "Haggle-Infocom2006" "Haggle-Intel"
#           "NCCU" "Sigcomm" "SocialBlueConn" "StAndrews")
datasets=("UPB2012")

for dataset in "${datasets[@]}"; do
    for model in "${models[@]}"; do
        (
            cd ~/mobemu/ || exit
            source .venv/bin/activate
            export MODEL="$model"
            export DATASET="$dataset"
            python train_model.py
        ) &
    done
done

wait
