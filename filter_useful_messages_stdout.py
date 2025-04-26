import os
from threading import Thread
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time

MAX_QUEUE_SIZE = 200
SENT_MAX_SIZE = 500000
MAX_FILE_SIZE = 3 * 1024 * 1024 * 1024
SUCCESSFUL_MAX_SIZE = 100000

def process_message(index, row, sent_messages):
    message_id, last_relay, destination = row.iloc[:3]

    indices_to_update = []
    visited = set()
    queue = sent_messages[(sent_messages["messageId"] == message_id) & (sent_messages["newRelayId"] == last_relay)].index.tolist()
    max_len = 0

    while queue:
        curr_idx = queue.pop()
        visited.add(curr_idx)
        indices_to_update.append(curr_idx)

        sent_messages_row = sent_messages.iloc[curr_idx]
        message_source, old_relay_id = sent_messages_row.iloc[1], sent_messages_row.iloc[3]

        if old_relay_id == message_source:
            break

        last_relay = old_relay_id

        for idx in sent_messages[(sent_messages["messageId"] == message_id) & (sent_messages["newRelayId"] == last_relay)].index.tolist():
            if idx not in visited and len(queue) < MAX_QUEUE_SIZE:
                queue.insert(0, idx)
                if (len(queue) > max_len):
                    max_len = len(queue)


    return indices_to_update  # Return the indices to update


def save_to_file(df, curr_idx=None):
    location = f"dataset/{os.environ.get('DATASET')}/useful_messages"
    if 'DISSEMINATION' in os.environ and os.environ['DISSEMINATION'] == 'true':
        location += '_dissemination'

    location += '.csv'

    df.to_csv(location)

    if curr_idx:
        with open(f"{os.environ.get('DATASET')}.tmp", "w") as f:
            f.write(str(curr_idx))

if __name__ == "__main__":
    sent_messages_file = f"dataset/{os.environ.get('DATASET')}/sent_messages"

    if os.environ.get('DISSEMINATION') == 'true':
        sent_messages_file += "_dissemination"
    sent_messages_file += ".csv"

    file_size = os.path.getsize(sent_messages_file)

    successful_messages_file = f"dataset/{os.environ.get('DATASET')}/successful"
    if os.environ.get('DISSEMINATION') == 'true':
        successful_messages_file += "_dissemination"
    successful_messages_file += ".csv"

    print(f"Sent messages file size {file_size}")

    # Read sent messages with size consideration
    if file_size > MAX_FILE_SIZE:
        print("reading just n rows")
        sent_messages = pd.read_csv(sent_messages_file, nrows=SENT_MAX_SIZE, engine="python")
    else:
        sent_messages = pd.read_csv(sent_messages_file)


    successful_messages = pd.read_csv(successful_messages_file, engine="python")

    # Filter sent messages based on successful messages
    sent_messages = sent_messages[sent_messages["messageId"].isin(successful_messages["messageId"])]


    if successful_messages.shape[0] > SUCCESSFUL_MAX_SIZE:
        successful_messages = successful_messages.sample(SUCCESSFUL_MAX_SIZE)


    if sent_messages.shape[0] > SENT_MAX_SIZE:
        sent_messages = sent_messages.sample(SENT_MAX_SIZE)
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

    print(f"Number of batches {total // batch_size}")

    start = 0
    tmp_file_name = f"{os.environ['DATASET']}.tmp"

    if os.path.exists(tmp_file_name):
        with open(tmp_file_name, "r") as f:
            start = int(f.read())
            location = f"dataset/{os.environ.get('DATASET')}/useful_messages"
            if 'DISSEMINATION' in os.environ and os.environ['DISSEMINATION'] == 'true':
                location += '_dissemination'

            location += '.csv'
            successful_messages = pd.read_csv(location)
            print(f"Continuing from {start} index")


    for start_idx in range(start, total, batch_size):
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


        if (start_idx//batch_size + 1) % 100 == 0:
            print("saving intermediary result")
            save_to_file(sent_messages, curr_idx=end_idx)


    save_to_file(sent_messages)
