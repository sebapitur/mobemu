python transform_to_csv.py .
mv trace_metrics.csv ml_trace_metrics.csv

python transform_to_csv.py spray_focus/
mv trace_metrics.csv spray_focus_trace_metrics.csv

python transform_to_csv.py epidemic/
mv trace_metrics.csv epidemic_trace_metrics.csv