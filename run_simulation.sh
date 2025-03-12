#!/bin/bash

DISSEMINATION="true"

AVAILABLE_MODELS=(
    "neural-UPB2012" "rf-Haggle-Content" "rf-Haggle-Infocom2006"
    "rf-NCCU" "rf-Sigcomm" "rf-UPB2011" "rf-UPB2015"
    "svm-NCCU" "svm-UPB2011" "svm-UPB2015"
)

ALGOS=("EPIDEMIC" "SPRAY_FOCUS")

TRACE=(
    "Haggle-Intel" "Haggle-Cambridge" "Haggle-Content" "Haggle-Infocom2006"
    "NCCU" "Sigcomm" "SocialBlueConn" "StAndrews" "UPB2011" "UPB2012" "UPB2015"
)

MAX_PROCS=4  # Set the maximum number of concurrent processes
proc_count=0  # Counter to keep track of running processes

for algo in "${ALGOS[@]}"; do
    for trace in "${TRACE[@]}"; do
        ALGO=$algo
        TRACE=$trace
        OUTPUT_WRITE=false

        echo "Starting simulation with ALGO=$ALGO, TRACE=$TRACE"
        env ALGO=$ALGO TRACE=$TRACE OUTPUT_WRITE=$OUTPUT_WRITE DISSEMINATION=$DISSEMINATION \
            java -jar target/mobemu-1.0-SNAPSHOT-jar-with-dependencies.jar &

        ((proc_count++))

        # If we've reached MAX_PROCS, wait for some to finish
        if (( proc_count >= MAX_PROCS )); then
            wait -n  # Wait for at least one background job to finish
            ((proc_count--))  # Decrease the count
        fi
    done
done



ALGO="ML_FOCUS"

for model in "${AVAILABLE_MODELS[@]}"; do
    for trace in "${TRACE[@]}"; do
        TRACE=$trace
        OUTPUT_WRITE=false

        echo "Starting simulation with MODEL=$MODEL, ALGO=$ALGO, TRACE=$TRACE"
        env MODEL=$MODEL ALGO=$ALGO TRACE=$TRACE OUTPUT_WRITE=$OUTPUT_WRITE DISSEMINATION=$DISSEMINATION \
        java -jar target/mobemu-1.0-SNAPSHOT-jar-with-dependencies.jar &

        ((proc_count++))

        # If we've reached MAX_PROCS, wait for some to finish
        if (( proc_count >= MAX_PROCS )); then
            wait -n  # Wait for at least one background job to finish
            ((proc_count--))  # Decrease the count
        fi
    done
done


echo "All simulations completed."