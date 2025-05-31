#!/bin/bash

if [ -n "$DISSEMINATION" ]; then
    echo "DISSEMINATION is $DISSEMINATION"
else
    echo "Variable DISSEMINATION is unset and by default, False"
    DISSEMINATION="false"
fi

AVAILABLE_MODELS=(
    neural-Haggle-Content neural-Haggle-Infocom2006 neural-NCCU neural-Sigcomm neural-UPB2011 neural-UPB2012 neural-UPB2015 rf-Haggle-Content rf-Haggle-Infocom2006 rf-NCCU rf-Sigcomm rf-UPB2011 rf-UPB2012 rf-UPB2015 svm-UPB2015
)

TRACE=(
    "Haggle-Intel" "Haggle-Cambridge" "Haggle-Content" "Haggle-Infocom2006"
    "NCCU" "Sigcomm" "SocialBlueConn" "StAndrews" "UPB2011" "UPB2012" "UPB2015"
)

# Check if DISSEMINATION has the expected value
if [[ "$DISSEMINATION" == "true" ]]; then
    # Assign only UPB2012 and UPB2015 to TRACE
    TRACE=("Haggle-Infocom2006" "UPB2012" "SocialBlueConn", "Sigcomm")

    AVAILABLE_MODELS=(
        decision-UPB2012 neural-Haggle-Infocom2006 neural-Sigcomm neural-SocialBlueConn neural-UPB2012 rf-Haggle-Infocom2006 rf-Sigcomm rf-SocialBlueConn rf-UPB2012 svm-Haggle-Infocom2006 svm-Sigcomm svm-SocialBlueConn svm-UPB2012
    )

    ALGOS=(
        "EPIDEMIC" "SPRAY_FOCUS" "SENSE" "IRONMAN" "SPRINT"
    )
else
    ALGOS=(
        "EPIDEMIC" "SPRAY_FOCUS" "MOGHADAMSCHULZRINNE" "ONSIDE" "SAROS" "SOCIALTRUST"
    )
fi


MAX_PROCS=2  # Set the maximum number of concurrent processes
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
       MODEL=$model

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
