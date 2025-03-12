#!/bin/bash

# Define the target directory
TARGET_DIR="all_metrics_files"
mkdir -p "$TARGET_DIR"

# Find and process each file
find . -name 'metr*.txt' | while read filepath; do
    # Extract the base directory name
    base_dir=$(basename $(dirname "$filepath"))
    
    # Extract the filename
    filename=$(basename "$filepath")

    # Create new filename with directory prefix
    new_filename="${base_dir}-${filename}"

    # Copy the file to the new directory with the new name
    cp "$filepath" "$TARGET_DIR/$new_filename"
done

echo "All files have been copied and renamed in $TARGET_DIR/"
