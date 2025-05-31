#!/bin/bash

# models=("neural" "rf" "svm")
models=("neural" "svm", "rf")

datasets=("UPB2011" "UPB2012" "UPB2015" "Haggle-Content" "Haggle-Infocom2006" "Haggle-Intel"
           "NCCU" "Sigcomm" "SocialBlueConn")

if [ -n "$DISSEMINATION" ]; then
    echo "DISSEMINATION is $DISSEMINATION"
else
    echo "Variable DISSEMINATION is unset and by default, False"
    DISSEMINATION="false"
fi



if [[ "$DISSEMINATION" == "true" ]]; then
    datasets=("UPB2012" "Haggle-Infocom2006" "SocialBlueConn" "Sigcomm")
fi

# Maximum number of parallel processes
MAX_PROCS=4

# Function to wait for background jobs if limit is reached
function wait_for_jobs() {
    while [ "$(jobs -rp | wc -l)" -ge "$MAX_PROCS" ]; do
        sleep 1
    done
}




for dataset in "${datasets[@]}"; do
    for model in "${models[@]}"; do
        wait_for_jobs  # Ensure we don't exceed MAX_PROCS
        (
            source .venv/Scripts/activate
            export MODEL="$model"
            export DATASET="$dataset"
            export DISSEMINATION="$DISSEMINATION"
            python train_model.py
        ) &
    done
done

wait
