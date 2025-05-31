import pandas as pd
import os


ml_df = pd.read_csv("ml_trace_metrics.csv")
# epidemic_df = pd.read_csv("epidemic_trace_metrics.csv")
# spray_focus_df = pd.read_csv("spray_focus_trace_metrics.csv")


algos = ["epidemic", "spray_focus", "ironman", "moghadamschulzrinne", "onside", "saros", "sense", "socialtrust"]


datasets = {algo: pd.read_csv(f"{algo}_trace_metrics.csv") for algo in algos}

# Assuming df is your dataframe with all the data
# First, let's create separate dataframes for each algorithm type


filter = False
if 'DISSEMINATION' in os.environ:
    filter = os.environ['DISSEMINATION'] == 'true'


ml_focus_df = ml_df[ml_df["dissemination"]==filter]

algos_df = {algo: datasets[algo][datasets[algo]["dissemination"] == filter] for algo in algos}

# Function to compare ML_FOCUS with other algorithms for each dataset
def compare_performance(dataset_name):
    # Filter data for the specific dataset
    ml_data = ml_focus_df[ml_focus_df['dataset'] == dataset_name]
    compared_datas = {algo: algos_df[algo][algos_df[algo]['dataset'].str.contains(dataset_name.split('_')[0])] for algo in algos}

    for algo in algos:
        if compared_datas[algo].empty:
            del compared_datas[algo]

    results = {
        'dataset': dataset_name,
        'metric': [],
        'ML_FOCUS_model': [],
        'ML_FOCUS_value': [],
        'comparison_algo': [],
        'comparison_value': [],
        'improvement_percentage': []
    }

    algo_values = {algo: compared_datas[algo].iloc[0] for algo in compared_datas.keys()}

    # Metrics to compare
    metrics = ['hit_rate', 'delivery_cost', 'delivery_latency', 'hop_count']

    # For each ML_FOCUS model in this dataset
    for _, ml_row in ml_data.iterrows():
        model_name = ml_row['model_info']

        for metric in metrics:
            ml_value = ml_row[metric]
            algo_value_row = {algo: algo_values[algo][metric] for algo in algo_values.keys()}

            for algo in algo_value_row.keys():
                print(algo)
                compared_value = algo_value_row[algo]
                # For hit_rate, higher is better
                if metric == 'hit_rate':
                    print(f"hit rate {ml_value} compared to {compared_value}")
                    if ml_value > compared_value:
                        improvement = ((ml_value - compared_value) / compared_value) * 100
                        results['metric'].append(metric)
                        results['ML_FOCUS_model'].append(model_name)
                        results['ML_FOCUS_value'].append(ml_value)
                        results['comparison_algo'].append(str(algo).upper())
                        results['comparison_value'].append(compared_value)
                        results['improvement_percentage'].append(improvement)
                # For other metrics, lower is better
                else:
                    print(f"other metrics {ml_value} compared to {compared_value}")
                    if ml_value < compared_value:
                        improvement = ((compared_value - ml_value) / compared_value) * 100
                        results['metric'].append(metric)
                        results['ML_FOCUS_model'].append(model_name)
                        results['ML_FOCUS_value'].append(ml_value)
                        results['comparison_algo'].append(str(algo).upper())
                        results['comparison_value'].append(compared_value)
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

    print(f"Saving results to filename {filename}")
    final_results.to_csv(filename)
else:
    print("No instances found where ML_FOCUS performs better")
