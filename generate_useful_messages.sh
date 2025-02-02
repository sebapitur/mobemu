#!/bin/bash

# Define datasets
datasets=("UPB2011" "UPB2012" "UPB2015")
# "Haggle-Intel" "Haggle-Cambridge" "Haggle-Content" "Haggle-Infocom2006" "NCCU" "Sigcomm" "SocialBlueConn" "StAndrews")

# Loop through datasets
for dataset in "${datasets[@]}"; do
    # Run the command in a new terminal window
    # gnome-terminal --tab -- bash -c "export DATASET=$dataset; .venv/bin/python filter_useful_messages.py; exec bash"
    bash -c "export DATASET=$dataset; .venv/bin/python filter_useful_messages.py &"
done
