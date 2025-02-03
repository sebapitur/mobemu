#!/bin/bash

# Define datasets
datasets=("UPB2011" "UPB2012" "UPB2015" "Haggle-Intel" "Haggle-Cambridge" "Haggle-Content" "Haggle-Infocom2006" "NCCU" "Sigcomm" "SocialBlueConn" "StAndrews")

# Initialize process counter
counter=0

# Loop through datasets
for dataset in "${datasets[@]}"; do
    # Start the process in the background
    bash -c "export DATASET=$dataset; .venv/bin/python filter_useful_messages.py &"
    
    # Increment counter
    ((counter++))
    
    # Wait after every three processes
    if ((counter % 3 == 0)); then
        wait
        echo "Waiting for batch of 3 processes to finish..."
    fi
done

# Final wait to ensure any remaining processes finish
wait
echo "All processes completed."
