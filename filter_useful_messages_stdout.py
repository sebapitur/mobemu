import os
import pandas as pd
import numpy as np

sent_messages_file = f"dataset/{os.environ.get('DATASET')}/sent_messages.csv"
file_size = os.path.getsize(sent_messages_file)

# if sent file is larger than 3GB
if file_size >  3 * 1024 * 1024 * 1024:
    sent_messages = pd.read_csv(
        sent_messages_file, nrows=10000000
    )
else:
    sent_messages = pd.read_csv(
        sent_messages_file
    )



successful_messages_file =  f"dataset/{os.environ.get('DATASET')}/successful.csv"

# if successful file is larger than 8Mb
if file_size > 8 * 1024 * 1024:
    successful_messages = pd.read_csv(
        f"dataset/{os.environ.get('DATASET')}/successful.csv", nrows=200000
    )
else:
    successful_messages = pd.read_csv(
        f"dataset/{os.environ.get('DATASET')}/successful.csv"
    )




sent_messages = sent_messages[
    sent_messages["messageId"].isin(successful_messages["messageId"])
]

if sent_messages.shape[0] > 350000:
    sent_messages = sent_messages.sample(350000)

successful_messages = successful_messages[
    successful_messages["messageId"].isin(sent_messages["messageId"])
]


successful_messages = successful_messages.reset_index(drop=True)

# make sure column is integer not float
sent_messages["usefulTransfer"] = pd.Series(dtype=np.int64)


sent_messages = sent_messages.reset_index(drop=True)



done_messages = 0

for index, row in successful_messages.iterrows():
    message_id = row.iloc[0]
    last_relay = row.iloc[1]
    destination = row.iloc[2]

    reached_source = False
    queue = sent_messages[
        (sent_messages["messageId"] == message_id)
        & (sent_messages["newRelayId"] == last_relay)
    ].index.tolist()

    visited = []
    while True:
        if len(queue) == 0:
            break

        curr_idx = queue.pop()
        visited.append(curr_idx)

        sent_messages_row = sent_messages.iloc[curr_idx]
        message_source = sent_messages_row.iloc[1]
        old_relay_id = sent_messages_row.iloc[3]

        sent_messages.loc[curr_idx, "usefulTransfer"] = 1

        if old_relay_id == message_source:
            break

        last_relay = old_relay_id

        for idx in sent_messages[
            (sent_messages["messageId"] == message_id)
            & (sent_messages["newRelayId"] == last_relay)
        ].index.tolist():
            if idx not in visited:
                queue.insert(0, idx)

    done_messages += 1



sent_messages.loc[(sent_messages["usefulTransfer"] != 1), "usefulTransfer"] = 0
sent_messages = sent_messages.drop(
    columns=["messageId", "oldRelayId", "newRelayId", "messageSource"]
)

csv_file_location = f"dataset/{os.environ.get('DATASET')}/useful_messages.csv"


sent_messages.to_csv(
    csv_file_location, index=False
)

import csv
import sys

with open(csv_file_location, 'r') as file:
    reader = csv.reader(file)
    writer = csv.writer(sys.stdout)
    for row in reader:
        writer.writerow(row)