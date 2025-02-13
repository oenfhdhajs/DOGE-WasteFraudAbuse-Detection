import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
import logging
from datetime import datetime

# Setting up logging
logging.basicConfig(filename='hidden_corruption_analysis.log', level=logging.INFO,
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

def detect_anomalies(df, column, threshold=3):
    """
    Detect anomalies in a given column using z-score method.
    
    :param df: DataFrame with the data
    :param column: Column to analyze for anomalies
    :param threshold: Z-score threshold for anomaly detection
    :return: DataFrame with an additional column indicating anomalies
    """
    df['z_score'] = zscore(df[column])
    df['is_anomaly'] = (df['z_score'] > threshold) | (df['z_score'] < -threshold)
    return df

def analyze_hidden_corruption(df):
    """
    Perform detailed analysis to uncover hidden corruption at the local level.
    
    :param df: DataFrame with local financial data
    :return: Dictionary with detailed analysis results
    """
    results = {}
    
    # Anomaly Detection in Salaries
    df = detect_anomalies(df, 'salary')
    results['salary_anomalies'] = df[df['is_anomaly']][['county', 'salary', 'z_score']]
    
    # Anomaly Detection in Total Worth
    df = detect_anomalies(df, 'total_worth')
    results['worth_anomalies'] = df[df['is_anomaly']][['county', 'total_worth', 'z_score']]
    
    # Analyze Discrepancy in Fee/Fine Collection vs Public Services
    df['fee_fine_ratio'] = df['fees'] + df['fines']
    df['service_spending'] = df['public_service_spending']  # Assuming this column exists
    results['fee_fine_vs_service'] = df.groupby('county').agg({
        'fee_fine_ratio': 'sum',
        'service_spending': 'sum'
    }).reset_index()
    results['fee_fine_vs_service']['discrepancy'] = results['fee_fine_vs_service']['fee_fine_ratio'] - results['fee_fine_vs_service']['service_spending']
    
    # Analyze Commission Income vs Local Business Support
    df['business_support'] = df['business_grants'] + df['business_loans']  # Assuming these columns exist
    commission_types = ['Liquor', 'Cannabis']
    for commission_type in commission_types:
        subset = df[df['commission_type'] == commission_type]
        results[f'{commission_type.lower()}_commission_analysis'] = subset.groupby('county').agg({
            'commission_income': 'sum',
            'business_support': 'sum'
        }).reset_index()
        results[f'{commission_type.lower()}_commission_analysis']['support_ratio'] = results[f'{commission_type.lower()}_commission_analysis']['business_support'] / results[f'{commission_type.lower()}_commission_analysis']['commission_income']
    
    # Visualizations
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='county', y='salary', data=df)
    plt.title('Salary Distribution by County')
    plt.xticks(rotation=45)
    plt.savefig('salary_distribution.png')
    plt.close()
    
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=results['fee_fine_vs_service'], x='fee_fine_ratio', y='service_spending', hue='county')
    plt.title('Fee/Fine Collection vs Public Service Spending')
    plt.savefig('fee_fine_vs_service.png')
    plt.close()
    
    logging.info("Hidden corruption analysis completed")
    return results

def main():
    data_path = 'local_financial_data.csv'
    df = load_data(data_path)
    analysis_results = analyze_hidden_corruption(df)
    
    # Save results to CSV for further analysis or reporting
    for key, value in analysis_results.items():
        if isinstance(value, pd.DataFrame):
            value.to_csv(f'{key}.csv', index=False)
    
    logging.info("Analysis results saved to CSV files")

if __name__ == "__main__":
    main()
