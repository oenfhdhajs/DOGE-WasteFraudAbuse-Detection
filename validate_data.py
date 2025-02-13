import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Setting up logging
logging.basicConfig(filename='data_validation.log', level=logging.INFO,
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

def validate_data(df):
    """
    Perform various validations on the data to ensure its integrity.
    
    :param df: Input DataFrame
    :return: Dictionary with validation results
    """
    validation_results = {}
    
    # Check for missing values
    missing_values = df.isnull().sum().sum()
    validation_results['missing_values'] = missing_values
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    validation_results['duplicates'] = duplicates
    
    # Check date format
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'])
            validation_results['date_format_valid'] = True
        except:
            validation_results['date_format_valid'] = False
    
    # Validate numerical columns for negative values where they shouldn't be
    numerical_columns = df.select_dtypes(include=[np.number]).columns
    for col in numerical_columns:
        if (df[col] < 0).any():
            validation_results[f'{col}_negative_values'] = (df[col] < 0).sum()
        else:
            validation_results[f'{col}_negative_values'] = 0
    
    # Check categorical data for unexpected values
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        unique_values = df[col].unique()
        validation_results[f'{col}_unexpected_values'] = len(unique_values)
    
    logging.info("Data validation completed")
    return validation_results

def generate_validation_report(validation_results, output_file='validation_report.csv'):
    """
    Generate a CSV report of the validation results.
    
    :param validation_results: Dictionary containing validation results
    :param output_file: Path to save the report
    """
    report_df = pd.DataFrame.from_dict(validation_results, orient='index', columns=['Count'])
    report_df.to_csv(output_file)
    logging.info(f"Validation report generated and saved to {output_file}")

def main():
    # Load the data
    data_path = 'government_spending_data.csv'
    df = load_data(data_path)
    
    # Validate the data
    results = validate_data(df)
    
    # Generate report
    generate_validation_report(results)

if __name__ == "__main__":
    main()
