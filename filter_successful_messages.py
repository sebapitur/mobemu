import os
import pandas as pd
import numpy as np

os.environ["DATASET"] = "UPB2011"

sent_messages = pd.read_csv(f"dataset/{os.environ.get('DATASET')}/sent_messages.csv")
print(f"sent_messages columns: {sent_messages.columns}")


successful_messages = pd.read_csv(f"dataset/{os.environ.get('DATASET')}/successful.csv")
print(f"successful messages columns: {successful_messages.columns}")


sent_messages = sent_messages[
    sent_messages["messageId"].isin(successful_messages["messageId"])
]

if sent_messages.shape[0] > 350000:
    sent_messages = sent_messages.sample(350000)

successful_messages = successful_messages[
    successful_messages["messageId"].isin(sent_messages["messageId"])
]

print("read the dataframes")

successful_messages = successful_messages.reset_index(drop=True)

# make sure column is integer not float
sent_messages["usefulTransfer"] = pd.Series(dtype=np.int64)

print("initialized the dataframe")

sent_messages = sent_messages.reset_index(drop=True)
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


sent_messages.loc[(sent_messages["usefulTransfer"] != 1), "usefulTransfer"] = 0
sent_messages = sent_messages.drop(
    columns=["messageId", "oldRelayId", "newRelayId", "messageSource"]
)
print(
    f"Number of useful transfers: {sent_messages['usefulTransfer'].value_counts()[1]}"
)

print(f"useful messages columns: {sent_messages.columns}")


sent_messages.to_csv(
    f"dataset/{os.environ.get('DATASET')}/useful_messages.csv", index=False
)
