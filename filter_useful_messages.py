import os
from threading import Thread
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time



def process_message(index, row, sent_messages):

    message_id, last_relay, destination = row.iloc[:3]

    indices_to_update = []
    visited = []
    queue = sent_messages[(sent_messages["messageId"] == message_id) & (sent_messages["newRelayId"] == last_relay)].index.tolist()
    max_len = 0

    while queue:
        curr_idx = queue.pop()
        visited.append(curr_idx)
        indices_to_update.append(curr_idx)

        sent_messages_row = sent_messages.iloc[curr_idx]
        message_source, old_relay_id = sent_messages_row.iloc[1], sent_messages_row.iloc[3]

        if old_relay_id == message_source:
            break

        last_relay = old_relay_id
        for idx in sent_messages[(sent_messages["messageId"] == message_id) & (sent_messages["newRelayId"] == last_relay)].index.tolist():
            if idx not in visited and len(queue) < 200:
                queue.insert(0, idx)
                if (len(queue) > max_len):
                    max_len = len(queue)


    return indices_to_update  # Return the indices to update

if __name__ == "__main__":
    sent_messages_file = f"dataset/{os.environ.get('DATASET')}/sent_messages"

    if os.environ.get('DISSEMINATION') == 'true':
        sent_messages_file += "_dissemination"
    sent_messages_file += ".csv"

    file_size = os.path.getsize(sent_messages_file)

    # Read sent messages with size consideration
    if file_size > 3 * 1024 * 1024 * 1024:
        sent_messages = pd.read_csv(sent_messages_file, nrows=10000000, engine="python")
    else:
        sent_messages = pd.read_csv(sent_messages_file)

    print(f"sent_messages columns: {sent_messages.columns}")

    successful_messages_file = f"dataset/{os.environ.get('DATASET')}/successful"
    if os.environ.get('DISSEMINATION') == 'true':
        successful_messages_file += "_dissemination"
    successful_messages_file += ".csv"

    # Read successful messages with size consideration
    if file_size > 8 * 1024 * 1024:
        successful_messages = pd.read_csv(successful_messages_file, nrows=200000, engine="python")
    else:
        successful_messages = pd.read_csv(successful_messages_file, engine="python")

    print(f"successful messages columns: {successful_messages.columns}")

    # Filter sent messages based on successful messages
    sent_messages = sent_messages[sent_messages["messageId"].isin(successful_messages["messageId"])]
    if sent_messages.shape[0] > 350000:
        sent_messages = sent_messages.sample(350000)

    successful_messages = successful_messages[successful_messages["messageId"].isin(sent_messages["messageId"])]
    print("read the dataframes")

    sent_messages = sent_messages.reset_index(drop=True)
    sent_messages["usefulTransfer"] = pd.Series(dtype=np.int64)
    print("initialized the dataframe")

    successful_messages = successful_messages.reset_index(drop=True)

    count = 0
    total = successful_messages.shape[0]


    # Process in smaller batches
    batch_size = 50  # Adjust as needed
    for start_idx in range(0, total, batch_size):
        start_time = time.time()
        end_idx = min(start_idx + batch_size, total)
        batch = successful_messages.iloc[start_idx:end_idx]

        with ProcessPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(process_message, i, row, sent_messages): i for i, row in batch.iterrows()}

            all_indices_to_update = []
            for future in as_completed(futures):
                indices = future.result()
                all_indices_to_update.extend(indices)
                count += 1
            print(f"ALL INDICES TO UPDATE {len(all_indices_to_update)}")

            # Update after each batch
            sent_messages.loc[all_indices_to_update, "usefulTransfer"] = 1

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time {elapsed_time}")
        print(f"Completed batch {start_idx//batch_size + 1} of {(total + batch_size - 1)//batch_size}")