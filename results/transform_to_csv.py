import os
import re
import pandas as pd
import sys

def extract_metrics(file_path):
    """Extract metrics from a single trace file."""
    metrics = {
        'trace_duration': None,
        'contacts': None,
        'contacts_per_hour': None,
        'nodes': None,
        'messages': None,
        'hit_rate': None,
        'delivery_cost': None,
        'delivery_latency': None,
        'hop_count': None
    }

    try:
        with open(file_path, 'r') as f:
            content = f.read()

            # Extract metrics using regex
            duration_match = re.search(r'Trace duration in hours: ([\d.]+)', content)
            if duration_match:
                metrics['trace_duration'] = float(duration_match.group(1))

            contacts_match = re.search(r'Trace contacts: (\d+)', content)
            if contacts_match:
                metrics['contacts'] = int(contacts_match.group(1))

            contacts_hour_match = re.search(r'Trace contacts per hour: ([\d.]+)', content)
            if contacts_hour_match:
                metrics['contacts_per_hour'] = float(contacts_hour_match.group(1))

            nodes_match = re.search(r'Nodes: (\d+)', content)
            if nodes_match:
                metrics['nodes'] = int(nodes_match.group(1))

            messages_match = re.search(r'Messages: (\d+)', content)
            if messages_match:
                metrics['messages'] = int(messages_match.group(1))

            hit_rate_match = re.search(r'HitRate ([\d.]+)', content)
            if hit_rate_match:
                metrics['hit_rate'] = float(hit_rate_match.group(1))

            delivery_cost_match = re.search(r'DeliveryCost ([\d.]+)', content)
            if delivery_cost_match:
                metrics['delivery_cost'] = float(delivery_cost_match.group(1))

            delivery_latency_match = re.search(r'DeliveryLatency ([\d.]+)', content)
            if delivery_latency_match:
                metrics['delivery_latency'] = float(delivery_latency_match.group(1))

            hop_count_match = re.search(r'HopCount ([\d.]+)', content)
            if hop_count_match:
                metrics['hop_count'] = float(hop_count_match.group(1))

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

    return metrics
def parse_filename(filename):
    """Extract dataset and model information from filename."""
    # Extract algo part (between ALGO_ and _TRACE)
    algo = re.search(r'ALGO_(.*)_TRACE', filename).group(1) if re.search(r'ALGO_(.*)_TRACE', filename) else None

    # Extract dataset part (between TRACE_ and _MODEL or .txt)
    dataset = re.search(r'TRACE_(.*?)(?:_MODEL|\.txt|_DATASET)', filename).group(1) if re.search(r'TRACE_(.*)(?:_MODEL|\.txt)', filename) else None

    # Extract model info (between MODEL_ and .txt) if it exists
    model_info = re.search(r'MODEL_(.*)[._]txt', filename).group(1) if re.search(r'MODEL_(.*?)\.txt', filename) else None

    dissemination = False

    if "DISSEMINATION" in filename:
        dissemination = True

    return dataset, algo, model_info, dissemination


def main():
    # List all text files in the current directory
    files = [f for f in os.listdir(sys.argv[1]) if f.startswith('ALGO_') and f.endswith('.txt')]

    # Create a list to store all data
    data = []

    # Process each file
    for file in files:
        dataset, algo, model_info, dissemination = parse_filename(file)
        if dataset and algo:
            metrics = extract_metrics(os.path.join(sys.argv[1], file))
            row_data = {
                'dataset': dataset,
                'algo': algo,
                'model_info': model_info if model_info else "not_relevant",
                'filename': file,
                'dissemination': dissemination,
                **metrics
            }
            data.append(row_data)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data)

    # Reorder columns for better readability
    columns_order = ['dataset', 'model_info', 'algo', 'dissemination', 'trace_duration',    'contacts','contacts_per_hour', 'nodes', 'messages',
                      'hit_rate', 'delivery_cost', 'delivery_latency', 'hop_count']
    df = df[columns_order]

    # Save to CSV
    output_file = 'trace_metrics.csv'
    df.to_csv(output_file, index=False)
    print(f"Data has been saved to {output_file}")
    print(f"Processed {len(files)} files")

if __name__ == "__main__":
    main()