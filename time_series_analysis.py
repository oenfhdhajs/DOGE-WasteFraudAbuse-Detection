import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import logging

# Setting up logging
logging.basicConfig(filename='time_series_analysis.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    
    :param file_path: Path to the CSV file
    :return: pandas DataFrame
    """
    try:
        data = pd.read_csv(file_path, parse_dates=['date'])
        logging.info(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Failed to load data: {str(e)}")
        raise

def perform_time_series_analysis(df, target_column='amount'):
    """
    Perform time series analysis on the specified column.
    
    :param df: DataFrame with time series data
    :param target_column: Column to analyze over time
    """
    # Ensure the data is sorted by date
    df = df.sort_values('date')
    
    # Set date as index
    df.set_index('date', inplace=True)
    
    # Resample data to monthly frequency
    monthly_data = df[target_column].resample('M').sum()
    
    # Perform seasonal decomposition
    decomposition = seasonal_decompose(monthly_data, model='additive', period=12)
    
    # Plot decomposition
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 16))
    decomposition.observed.plot(ax=ax1)
    ax1.set_title('Observed')
    decomposition.trend.plot(ax=ax2)
    ax2.set_title('Trend')
    decomposition.seasonal.plot(ax=ax3)
    ax3.set_title('Seasonal')
    decomposition.resid.plot(ax=ax4)
    ax4.set_title('Residual')
    plt.tight_layout()
    plt.savefig('time_series_decomposition.png')
    plt.close()
    
    # Test for stationarity
    result = adfuller(monthly_data)
    logging.info(f'ADF Statistic: {result[0]}')
    logging.info(f'p-value: {result[1]}')
    
    # If p-value is less than 0.05, we reject the null hypothesis and the series is stationary
    if result[1] < 0.05:
        logging.info("The time series is stationary")
    else:
        logging.info("The time series is non-stationary")

def main():
    data_path = 'government_spending_data.csv'
    df = load_data(data_path)
    perform_time_series_analysis(df)

if __name__ == "__main__":
    main()
