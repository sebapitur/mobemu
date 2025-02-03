#!/bin/bash

AVAILABLE_MODELS=(
    "neural-UPB2012" "rf-Haggle-Content" "rf-Haggle-Infocom2006"
    "rf-NCCU" "rf-Sigcomm" "rf-UPB2011" "rf-UPB2015"
    "svm-NCCU" "svm-UPB2011" "svm-UPB2015"
)

ALGOS=("ML_FOCUS" "EPIDEMIC" "SPRAY_FOCUS")

TRACE=(
    "Haggle-Intel" "Haggle-Cambridge" "Haggle-Content" "Haggle-Infocom2006"
    "NCCU" "Sigcomm" "SocialBlueConn" "StAndrews" "UPB2011" "UPB2012" "UPB2015"
)

for model in "${AVAILABLE_MODELS[@]}"; do
    for algo in "${ALGOS[@]}"; do
        for trace in "${TRACE[@]}"; do
            MODEL=$model
            ALGO=$algo
            TRACE=$trace
            OUTPUT_WRITE=false

            echo "Starting simulation with MODEL=$MODEL, ALGO=$ALGO, TRACE=$TRACE"
            env MODEL=$MODEL ALGO=$ALGO TRACE=$TRACE OUTPUT_WRITE=$OUTPUT_WRITE \
                java -jar target/mobemu-1.0-SNAPSHOT-jar-with-dependencies.jar &
        done

        # Wait for all background processes in the inner loop to finish before starting the next set
        wait
        echo "Batch for ALGO=$algo completed."
    done
done

echo "All simulations completed."
