import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import logging
from sklearn.preprocessing import StandardScaler

# Setting up logging
logging.basicConfig(filename='anomaly_detection.log', level=logging.INFO,
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

def detect_anomalies(df, features):
    """
    Detect anomalies in the data using Isolation Forest.
    
    :param df: Input DataFrame
    :param features: List of features to consider for anomaly detection
    :return: DataFrame with anomaly scores and predictions
    """
    # Preprocess data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[features])
    
    # Train Isolation Forest
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    anomalies = iso_forest.fit_predict(scaled_data)
    
    # Add anomaly scores and predictions to DataFrame
    df['anomaly_score'] = iso_forest.decision_function(scaled_data)
    df['anomaly'] = [1 if x == -1 else 0 for x in anomalies]
    
    logging.info("Anomaly detection completed")
    return df

def visualize_anomalies(df, feature):
    """
    Visualize anomalies in a scatter plot.
    
    :param df: DataFrame with anomaly detection results
    :param feature: Feature to plot against anomaly score
    """
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df[feature], df['anomaly_score'], c=df['anomaly'], cmap='viridis')
    plt.colorbar(scatter)
    plt.xlabel(feature)
    plt.ylabel('Anomaly Score')
    plt.title(f'Anomaly Detection: {feature} vs Anomaly Score')
    plt.savefig('anomaly_detection.png')
    plt.close()

def main():
    data_path = 'government_spending_data.csv'
    df = load_data(data_path)
    
    features = ['amount', 'transaction_count']  # Example features
    df_with_anomalies = detect_anomalies(df, features)
    
    # Visualize anomalies
    for feature in features:
        visualize_anomalies(df_with_anomalies, feature)
    
    # Save results
    df_with_anomalies.to_csv('anomaly_detection_results.csv', index=False)

if __name__ == "__main__":
    main()
