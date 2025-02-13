import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import logging

# Setting up logging
logging.basicConfig(filename='reports.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    
    :param file_path: Path to the CSV file
    :return: pandas DataFrame
    """
    try:
        data = pd.read_csv(file_path)
        logging.info(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Failed to load data: {str(e)}")
        raise

def generate_fraud_report(df, output_dir):
    """
    Generate a detailed report on fraud detection.
    
    :param df: DataFrame with fraud detection results
    :param output_dir: Directory to save the reports
    """
    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Fraud summary
    fraud_summary = df[df['fraud_flag'] == 1].groupby('department').size().reset_index(name='fraud_count')
    fraud_summary.to_csv(os.path.join(output_dir, 'fraud_summary.csv'), index=False)
    
    # Visual fraud report
    plt.figure(figsize=(12, 6))
    plt.bar(fraud_summary['department'], fraud_summary['fraud_count'])
    plt.title('Fraudulent Cases by Department')
    plt.xlabel('Department')
    plt.ylabel('Number of Fraudulent Cases')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fraud_distribution.png'))
    plt.close()
    
    logging.info(f"Fraud report generated and saved to {output_dir}")

def generate_waste_report(df, output_dir):
    """
    Generate a report on identified waste.
    
    :param df: DataFrame with waste analysis results
    :param output_dir: Directory to save the reports
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Waste by category
    waste_by_category = df.groupby('category')['amount'].sum().reset_index()
    waste_by_category.to_csv(os.path.join(output_dir, 'waste_by_category.csv'), index=False)
    
    # Visual waste report
    plt.figure(figsize=(12, 6))
    plt.pie(waste_by_category['amount'], labels=waste_by_category['category'], autopct='%1.1f%%')
    plt.title('Distribution of Waste by Category')
    plt.savefig(os.path.join(output_dir, 'waste_pie_chart.png'))
    plt.close()
    
    logging.info(f"Waste report generated and saved to {output_dir}")

def main():
    data_path = 'government_spending_data.csv'
    df = load_data(data_path)
    report_dir = 'reports_' + datetime.now().strftime("%Y%m%d_%H%M%S")
    
    generate_fraud_report(df, report_dir)
    generate_waste_report(df, report_dir)

if __name__ == "__main__":
    main()
