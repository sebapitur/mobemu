#!/bin/bash

# Define datasets
datasets=("UPB2011" "UPB2012" "UPB2015" "Haggle-Intel" "Haggle-Cambridge" "Haggle-Content" "Haggle-Infocom2006" "NCCU" "Sigcomm" "SocialBlueConn" "StAndrews")

# Set working directory
cd "$HOME/mobemu" || exit

# Loop through datasets and run each command in the background
for dataset in "${datasets[@]}"; do
    (
        export TRACE="$dataset"
        export ALGO="EPIDEMIC"
        export OUTPUT_WRITE="true"
        java -jar ./target/mobemu-1.0-SNAPSHOT-jar-with-dependencies.jar
    ) &
done

# Wait for all background jobs to finish
wait
