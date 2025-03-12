#!/bin/bash

# Define datasets
datasets=("UPB2011" "UPB2012" "UPB2015" "Haggle-Intel" "Haggle-Cambridge" "Haggle-Content" "Haggle-Infocom2006" "NCCU" "Sigcomm" "SocialBlueConn" "StAndrews")

# Get the number of available CPU cores
MAX_PROCS=4
echo "Using up to $MAX_PROCS parallel processes..."

# Initialize process counter
proc_count=0

# Loop through datasets and run each command in the background
for dataset in "${datasets[@]}"; do
    (
        export TRACE="$dataset"
        export ALGO=EPIDEMIC
        export OUTPUT_WRITE=true
        java -jar ./target/mobemu-1.0-SNAPSHOT-jar-with-dependencies.jar
    ) &

    ((proc_count++))

    # Ensure we never exceed MAX_PROCS running in parallel
    if (( proc_count >= MAX_PROCS )); then
        wait -n  # Wait for at least one process to finish before starting a new one
        ((proc_count--))  # Decrease the counter
    fi
done

# Final wait to ensure all processes complete before exiting
wait
echo "All processes completed."
