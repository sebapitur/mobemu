import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse

def plot_bar_chart_from_csv(csv_file, title=None):
    try:
        # Read the CSV file
        print(f"Reading data from {csv_file}...")
        df = pd.read_csv(csv_file)
        
        # Print basic information about the data
        print("\nData preview:")
        print(df.head())
        print("\nColumn names:", df.columns.tolist())
        
        # Check if the dataframe is empty
        if df.empty:
            print("Error: The CSV file is empty.")
            return False
            
        # Identify numeric columns for plotting
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_columns:
            print("Error: No numeric columns found for plotting.")
            return False
            
        print(f"\nNumeric columns available for plotting: {numeric_columns}")
        
        # Try to identify a suitable category column (first non-numeric column)
        non_numeric_cols = [col for col in df.columns if col not in numeric_columns]
        
        # Create a new figure
        plt.figure(figsize=(12, 7))
        
        # Different plotting strategies based on data structure
        if non_numeric_cols and len(numeric_columns) >= 1:
            # Use first non-numeric column as categories and first numeric column for values
            category_col = non_numeric_cols[0]
            value_col = numeric_columns[0]
            
            print(f"Creating bar chart with '{category_col}' as categories and '{value_col}' as values")
            
            # Sort by value in descending order for better visualization
            sorted_data = df.sort_values(by=value_col, ascending=False)
            plt.bar(sorted_data[category_col], sorted_data[value_col], color='skyblue')
            plt.xlabel(category_col)
            plt.ylabel(value_col)
            
            # If there are many categories, rotate the labels
            if len(df[category_col].unique()) > 7:
                plt.xticks(rotation=45, ha='right')
        
        elif len(numeric_columns) >= 2:
            # Use first numeric column as categories and second as values
            category_col = numeric_columns[0]
            value_col = numeric_columns[1]
            
            print(f"Creating bar chart with '{category_col}' as categories and '{value_col}' as values")
            
            plt.bar(df[category_col], df[value_col], color='skyblue')
            plt.xlabel(category_col)
            plt.ylabel(value_col)
        
        else:
            # Use index as categories and the numeric column as values
            value_col = numeric_columns[0]
            
            print(f"Creating bar chart with index as categories and '{value_col}' as values")
            
            plt.bar(df.index, df[value_col], color='skyblue')
            plt.xlabel('Index')
            plt.ylabel(value_col)
        
        # Add title
        if title:
            plt.title(title, fontsize=14, fontweight='bold')
        else:
            plt.title(f'Bar Chart from {csv_file}', fontsize=14)
        
        # Customize appearance
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the plot
        output_file = csv_file.replace('.csv', '_bar_chart.png')
        plt.savefig(output_file)
        print(f"\nBar chart saved as {output_file}")
        
        # Show the plot
        plt.show()
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return False
    except pd.errors.EmptyDataError:
        print(f"Error: File '{csv_file}' is empty.")
        return False
    except pd.errors.ParserError:
        print(f"Error: Unable to parse file '{csv_file}'. Make sure it's a valid CSV file.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def plot_multiple_bars_from_csv(csv_file, title=None):
    """Alternative function to plot multiple columns as grouped bar chart"""
    try:
        # Read the CSV file
        print(f"Reading data from {csv_file}...")
        df = pd.read_csv(csv_file)
        
        # Print basic information about the data
        print("\nData preview:")
        print(df.head())
        
        # Check if the dataframe is empty
        if df.empty:
            print("Error: The CSV file is empty.")
            return False
            
        # Identify numeric columns for plotting
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        if len(numeric_columns) < 2:
            print("Error: At least two numeric columns needed for grouped bar chart.")
            return False
        
        # Try to identify a suitable category column (first non-numeric column)
        non_numeric_cols = [col for col in df.columns if col not in numeric_columns]
        
        # Create a new figure
        plt.figure(figsize=(12, 7))
        
        if non_numeric_cols:
            # Use first non-numeric column as x-axis
            category_col = non_numeric_cols[0]
            categories = df[category_col]
            
            # Get position indices for bars
            x = range(len(categories))
            width = 0.8 / len(numeric_columns)
            
            # Plot each numeric column as a set of bars
            for i, col in enumerate(numeric_columns):
                offset = i * width - 0.4 + width / 2
                plt.bar([pos + offset for pos in x], df[col], width=width, label=col)
            
            plt.xlabel(category_col)
            plt.xticks(x, categories, rotation=45, ha='right')
        else:
            # Without a category column, use the first numeric column as x-axis
            categories = df[numeric_columns[0]]
            x = range(len(categories))
            width = 0.8 / (len(numeric_columns) - 1)
            
            # Plot each numeric column (except first) as a set of bars
            for i, col in enumerate(numeric_columns[1:]):
                offset = i * width - 0.4 + width / 2
                plt.bar([pos + offset for pos in x], df[col], width=width, label=col)
            
            plt.xlabel(numeric_columns[0])
            plt.xticks(x, categories, rotation=45, ha='right')
        
        # Add title
        if title:
            plt.title(title, fontsize=14, fontweight='bold')
        else:
            plt.title(f'Grouped Bar Chart from {csv_file}', fontsize=14)
        
        # Customize appearance
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend()
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the plot
        output_file = csv_file.replace('.csv', '_grouped_bar_chart.png')
        plt.savefig(output_file)
        print(f"\nGrouped bar chart saved as {output_file}")
        
        # Show the plot
        plt.show()
        return True
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Create bar charts from CSV data')
    parser.add_argument('csv_file', nargs='?', help='Path to the CSV file')
    parser.add_argument('--grouped', '-g', action='store_true', help='Create a grouped bar chart')
    parser.add_argument('--title', '-t', type=str, help='Custom title for the plot')
    
    args = parser.parse_args()
    
    # Get the CSV file path
    if args.csv_file:
        csv_file = args.csv_file
    else:
        csv_file = input("Enter the path to your CSV file: ")
    
    # Get chart type if not specified
    if not args.grouped and '--grouped' not in sys.argv and '-g' not in sys.argv:
        chart_type = input("Enter chart type (single/grouped): ").lower()
        grouped = chart_type in ['grouped', 'group', 'multiple']
    else:
        grouped = args.grouped
    
    # Get title if not specified
    if not args.title and '--title' not in sys.argv and '-t' not in sys.argv:
        title = input("Enter chart title (press Enter for default): ")
        if not title:
            title = None
    else:
        title = args.title
    
    # Create the chart
    if grouped:
        plot_multiple_bars_from_csv(csv_file, title)
    else:
        plot_bar_chart_from_csv(csv_file, title)