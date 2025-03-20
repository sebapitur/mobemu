import os
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def process_message(index, row):
    print(f"Processing index: {index}")
    message_id, last_relay, destination = row.iloc[:3]
    queue = sent_messages[(sent_messages["messageId"] == message_id) & (sent_messages["newRelayId"] == last_relay)].index.tolist()
    visited = []

    while queue:
        curr_idx = queue.pop()
        visited.append(curr_idx)
        sent_messages_row = sent_messages.iloc[curr_idx]
        message_source, old_relay_id = sent_messages_row.iloc[1], sent_messages_row.iloc[3]
        sent_messages.loc[curr_idx, "usefulTransfer"] = 1

        if old_relay_id == message_source:
            break

        last_relay = old_relay_id
        for idx in sent_messages[(sent_messages["messageId"] == message_id) & (sent_messages["newRelayId"] == last_relay)].index.tolist():
            if idx not in visited:
                queue.insert(0, idx)
    return message_id


# Multithreading to process messages
with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    count = 0
    futures = {executor.submit(process_message, i, row): i for i, row in successful_messages.iterrows()}
    for future in as_completed(futures):
        count += 1
        print(f"Done with message {future.result()}, percentage: {count / successful_messages.shape[0] * 100}%")

# Finalize data
sent_messages.loc[(sent_messages["usefulTransfer"] != 1), "usefulTransfer"] = 0
sent_messages.drop(columns=["messageId", "oldRelayId", "newRelayId", "messageSource"], inplace=True)
print(f"Number of useful transfers: {sent_messages['usefulTransfer'].sum()}")

csv_file_location = f"dataset/{os.environ.get('DATASET')}/useful_messages"
if os.environ.get('DISSEMINATION') == 'true':
    csv_file_location += "_dissemination"
csv_file_location += ".csv"

print(f"useful messages columns: {sent_messages.columns}")
print(f"Current working dir: {os.getcwd()}")
print(f"Saving to {csv_file_location}")

if os.environ.get('DISSEMINATION') == 'true':
    sent_messages.drop(columns=["messageHopCount"], inplace=True)

sent_messages.to_csv(csv_file_location, index=False)
