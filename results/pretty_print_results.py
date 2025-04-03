import pandas as pd
from tabulate import tabulate

# Sample DataFrame
routing_df = pd.read_csv("comparison_routing.csv")
dissemination_df = pd.read_csv("comparison_dissemination.csv")

# Convert DataFrame to tabulated format
print()
print("#################ROUTING EPIDEMIC###################")
print()
print(tabulate(routing_df[routing_df['comparison_algo']=='EPIDEMIC'], headers='keys', tablefmt='pretty'))

print()
print("#################ROUTING SPRAY FOCUS###################")
print()
print(tabulate(routing_df[routing_df['comparison_algo']=='SPRAY_FOCUS'], headers='keys', tablefmt='pretty'))



print()
print("#################DISSEMINATION EPIDEMIC###################")
print()
print(tabulate(dissemination_df[dissemination_df['comparison_algo']=='EPIDEMIC'], headers='keys', tablefmt='pretty'))
print()
print("#################DISSEMINATION SPRAY FOCUS###################")
print()
print(tabulate(dissemination_df[dissemination_df['comparison_algo']=='SPRAY_FOCUS'], headers='keys', tablefmt='pretty'))
