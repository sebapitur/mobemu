import pandas as pd
from tabulate import tabulate


def display_by_metric(df: pd.DataFrame):
    for metric in df['metric'].unique():
        print(f"################# {metric} #####################")
        print(tabulate(df[df['metric']==metric], headers='keys', tablefmt='pretty'))


# Sample DataFrame
routing_df = pd.read_csv("comparison_routing.csv")
dissemination_df = pd.read_csv("comparison_dissemination.csv")

# Convert DataFrame to tabulated format
print()
print("#################ROUTING EPIDEMIC###################")
print()

epidemic_routing = routing_df[routing_df['comparison_algo']=='EPIDEMIC']
display_by_metric(epidemic_routing)

print()
print("#################ROUTING SPRAY FOCUS###################")
print()

spray_routing = routing_df[routing_df['comparison_algo']=='SPRAY_FOCUS']
display_by_metric(spray_routing)


print()
print("#################DISSEMINATION EPIDEMIC###################")
print()
epidemic_dissemination = dissemination_df[dissemination_df['comparison_algo']=='EPIDEMIC']
display_by_metric(epidemic_dissemination)


print()
print("#################DISSEMINATION SPRAY FOCUS###################")
print()
spray_dissemination = dissemination_df[dissemination_df['comparison_algo']=='SPRAY_FOCUS'] 
display_by_metric(spray_dissemination)
