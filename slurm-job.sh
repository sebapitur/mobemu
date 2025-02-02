#!/bin/bash

#SBATCH --cpus-per-task=4  # Request 4 CPUs
#SBATCH --mem=4G  # Request 4GB of RAM

# Check if DATASET is provided
if [ -z "$DATASET" ]; then
    echo "Error: DATASET environment variable not set."
    exit 1
fi

# Define the Singularity image path
SINGULARITY_IMAGE="./filter_messages.sif"

singularity run --env DATASET="$DATASET" "$SINGULARITY_IMAGE" 
