import pandas as pd
import os


ml_df = pd.read_csv("ml_trace_metrics.csv")
epidemic_df = pd.read_csv("epidemic_trace_metrics.csv")
spray_focus_df = pd.read_csv("spray_focus_trace_metrics.csv")

# Assuming df is your dataframe with all the data
# First, let's create separate dataframes for each algorithm type


filter = False
if 'DISSEMINATION' in os.environ:
    filter = os.environ['DISSEMINATION'] == 'true'


ml_focus_df = ml_df[ml_df["dissemination"]==filter]
epidemic_df = epidemic_df[epidemic_df["dissemination"]==filter]
spray_focus_df = spray_focus_df[spray_focus_df['dissemination'] == filter]

# Function to compare ML_FOCUS with other algorithms for each dataset
def compare_performance(dataset_name):
    # Filter data for the specific dataset
    ml_data = ml_focus_df[ml_focus_df['dataset'] == dataset_name]
    epidemic_data = epidemic_df[epidemic_df['dataset'].str.contains(dataset_name.split('_')[0])]
    spray_data = spray_focus_df[spray_focus_df['dataset'].str.contains(dataset_name.split('_')[0])]

    # If any algorithm doesn't have data for this dataset, return None
    if ml_data.empty or epidemic_data.empty or spray_data.empty:
        return None

    results = {
        'dataset': dataset_name,
        'metric': [],
        'ML_FOCUS_model': [],
        'ML_FOCUS_value': [],
        'comparison_algo': [],
        'comparison_value': [],
        'improvement_percentage': []
    }

    # Get epidemic and spray values for this dataset
    epidemic_values = epidemic_data.iloc[0]
    spray_values = spray_data.iloc[0]

    # Metrics to compare
    metrics = ['hit_rate', 'delivery_cost', 'delivery_latency', 'hop_count']

    # For each ML_FOCUS model in this dataset
    for _, ml_row in ml_data.iterrows():
        model_name = ml_row['model_info']

        for metric in metrics:
            ml_value = ml_row[metric]
            epidemic_value = epidemic_values[metric]
            spray_value = spray_values[metric]

            # For hit_rate, higher is better
            if metric == 'hit_rate':
                if ml_value > epidemic_value:
                    improvement = ((ml_value - epidemic_value) / epidemic_value) * 100
                    results['metric'].append(metric)
                    results['ML_FOCUS_model'].append(model_name)
                    results['ML_FOCUS_value'].append(ml_value)
                    results['comparison_algo'].append('EPIDEMIC')
                    results['comparison_value'].append(epidemic_value)
                    results['improvement_percentage'].append(improvement)

                if ml_value > spray_value:
                    improvement = ((ml_value - spray_value) / spray_value) * 100
                    results['metric'].append(metric)
                    results['ML_FOCUS_model'].append(model_name)
                    results['ML_FOCUS_value'].append(ml_value)
                    results['comparison_algo'].append('SPRAY_FOCUS')
                    results['comparison_value'].append(spray_value)
                    results['improvement_percentage'].append(improvement)

            # For other metrics, lower is better
            else:
                if ml_value < epidemic_value:
                    improvement = ((epidemic_value - ml_value) / epidemic_value) * 100
                    results['metric'].append(metric)
                    results['ML_FOCUS_model'].append(model_name)
                    results['ML_FOCUS_value'].append(ml_value)
                    results['comparison_algo'].append('EPIDEMIC')
                    results['comparison_value'].append(epidemic_value)
                    results['improvement_percentage'].append(improvement)

                if ml_value < spray_value:
                    improvement = ((spray_value - ml_value) / spray_value) * 100
                    results['metric'].append(metric)
                    results['ML_FOCUS_model'].append(model_name)
                    results['ML_FOCUS_value'].append(ml_value)
                    results['comparison_algo'].append('SPRAY_FOCUS')
                    results['comparison_value'].append(spray_value)
                    results['improvement_percentage'].append(improvement)

    # Return a dataframe with the results
    if results['metric']:
        return pd.DataFrame(results)
    else:
        return None

# Get unique datasets from ML_FOCUS
unique_datasets = ml_focus_df['dataset'].unique()

# Collect all comparisons
all_comparisons = []
for dataset in unique_datasets:
    comparison = compare_performance(dataset)
    if comparison is not None:
        all_comparisons.append(comparison)

# Combine all comparisons if there are any
if all_comparisons:
    final_results = pd.concat(all_comparisons)

    # Sort by improvement percentage (descending)
    final_results = final_results.sort_values('improvement_percentage', ascending=False)

    # Round numeric columns for better readability
    numeric_cols = ['ML_FOCUS_value', 'comparison_value', 'improvement_percentage']
    final_results[numeric_cols] = final_results[numeric_cols].round(2)

    print("Instances where ML_FOCUS performs better:")
    print(final_results)
    filename = "comparison_dissemination.csv" if filter else "comparison_routing.csv"
    final_results.to_csv(filename)
else:
    print("No instances found where ML_FOCUS performs better")
