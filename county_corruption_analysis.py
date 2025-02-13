import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from datetime import datetime

# Setting up logging
logging.basicConfig(filename='county_corruption_analysis.log', level=logging.INFO,
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

def analyze_county_corruption(df):
    """
    Analyze county-level corruption indicators including salaries, total worth, fees, fines, and commissions.
    
    :param df: DataFrame with county financial data
    :return: Dictionary with analysis results
    """
    results = {}
    
    # Salaries and Total Worth Analysis
    results['salary_stats'] = df.groupby('county')['salary'].agg(['mean', 'median', 'max']).reset_index()
    results['total_worth_stats'] = df.groupby('county')['total_worth'].agg(['mean', 'median', 'max']).reset_index()
    
    # Fees and Fines Analysis
    fees_fines = df.groupby('county')[['fees', 'fines']].sum().reset_index()
    results['fees_fines'] = fees_fines
    
    # Commission Analysis
    commissions = df[df['commission_type'].isin(['Liquor', 'Cannabis'])].groupby(['county', 'commission_type'])['commission_income'].sum().unstack().fillna(0)
    results['commissions'] = commissions
    
    # Correlation between enforcement actions and court outcomes
    enforcement_court_corr = df[['enforcement_actions', 'court_outcomes']].corr().iloc[0, 1]
    results['enforcement_court_correlation'] = enforcement_court_corr
    
    # Visualization
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='salary', y='total_worth', hue='county', size='fees', sizes=(20, 200))
    plt.title('Salary vs Total Worth by County with Fee Size')
    plt.savefig('salary_vs_worth.png')
    plt.close()
    
    plt.figure(figsize=(12, 6))
    fees_fines.plot(kind='bar', x='county', y=['fees', 'fines'], figsize=(12, 6))
    plt.title('Fees and Fines by County')
    plt.ylabel('Amount ($)')
    plt.savefig('fees_fines_by_county.png')
    plt.close()
    
    logging.info("County-level corruption analysis completed")
    return results

def main():
    data_path = 'county_financial_data.csv'
    df = load_data(data_path)
    analysis_results = analyze_county_corruption(df)
    
    # Save results to CSV for further analysis or reporting
    for key, value in analysis_results.items():
        if isinstance(value, pd.DataFrame):
            value.to_csv(f'{key}.csv', index=False)
    
    logging.info("Analysis results saved to CSV files")

if __name__ == "__main__":
    main()
