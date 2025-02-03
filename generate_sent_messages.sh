#!/bin/bash

# Define datasets
datasets=("UPB2011" "UPB2012" "UPB2015" "Haggle-Intel" "Haggle-Cambridge" "Haggle-Content" "Haggle-Infocom2006" "NCCU" "Sigcomm" "SocialBlueConn" "StAndrews")

# Set working directory
cd "$HOME/mobemu" || exit

# Initialize process counter
counter=0

# Loop through datasets and run each command in the background
for dataset in "${datasets[@]}"; do
    (
        export TRACE="$dataset"
        export ALGO="EPIDEMIC"
        export OUTPUT_WRITE="true"
        java -jar ./target/mobemu-1.0-SNAPSHOT-jar-with-dependencies.jar
    ) &

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
