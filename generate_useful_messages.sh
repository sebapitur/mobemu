#!/bin/bash

# Define datasets

datasets=("UPB2011" "UPB2012" "UPB2015"
           "Haggle-Cambridge" "Haggle-Content" "Haggle-Infocom2006" "Haggle-Intel"
           "NCCU" "Sigcomm" "SocialBlueConn" "StAndrews")

if [[ "$DISSEMINATION" == "true" ]]; then
    datasets=("UPB2012" "Haggle-Infocom2006" "SocialBlueConn" "Sigcomm")
fi

# Get the number of available CPU cores
MAX_PROCS=1
echo "Using up to $MAX_PROCS parallel processes..."

# Initialize process counter
proc_count=0

# Loop through datasets
for dataset in "${datasets[@]}"; do
    (
        export DATASET="$dataset"
        python filter_useful_messages.py
    ) &  # Run in the background

    ((proc_count++))

    # Ensure we never exceed MAX_PROCS running in parallel
    if (( proc_count >= MAX_PROCS )); then
        wait -n  # Wait for at least one process to finish before starting a new one
        ((proc_count--))  # Decrease the counter
    fi
done

# Final wait to ensure all remaining processes complete before exiting
wait
echo "All processes completed."
