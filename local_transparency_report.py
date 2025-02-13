import pandas as pd
from textblob import TextBlob
import logging

# Setting up logging
logging.basicConfig(filename='local_transparency_report.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def load_analysis_results():
    """
    Load the results from the previous hidden corruption analysis.
    
    :return: Dictionary with analysis results
    """
    results = {}
    for file in ['salary_anomalies.csv', 'worth_anomalies.csv', 'fee_fine_vs_service.csv', 'liquor_commission_analysis.csv', 'cannabis_commission_analysis.csv']:
        try:
            results[file.replace('.csv', '')] = pd.read_csv(file)
        except FileNotFoundError:
            logging.error(f"File not found: {file}")
    
    return results

def generate_transparency_report(results):
    """
    Generate a report focusing on transparency issues based on the analysis results.
    
    :param results: Dictionary with analysis results
    :return: String containing the transparency report
    """
    report = []
    
    # Salary Anomalies
    if 'salary_anomalies' in results:
        anomalies = results['salary_anomalies']
        report.append(f"Anomalies in Salaries: Our analysis detected {len(anomalies)} salary outliers across various counties. For instance, in {anomalies['county'].iloc[0]}, an official's salary of ${anomalies['salary'].iloc[0]:.2f} stands out with a z-score of {anomalies['z_score'].iloc[0]:.2f}, which might indicate potential overcompensation or financial irregularities.")
    
    # Total Worth Anomalies
    if 'worth_anomalies' in results:
        anomalies = results['worth_anomalies']
        report.append(f"Anomalies in Total Worth: Similarly, we found {len(anomalies)} instances where the total worth of county officials was significantly higher than average. In {anomalies['county'].iloc[0]}, with a total worth of ${anomalies['total_worth'].iloc[0]:.2f} and a z-score of {anomalies['z_score'].iloc[0]:.2f}, there's a clear deviation from the norm, suggesting potential hidden wealth accumulation.")
    
    # Fee/Fine vs Public Service
    if 'fee_fine_vs_service' in results:
        discrepancies = results['fee_fine_vs_service']
        max_discrepancy_county = discrepancies.loc[discrepancies['discrepancy'].idxmax(), 'county']
        report.append(f"Discrepancy in Fee/Fine Collection: In {max_discrepancy_county}, the collection of fees and fines significantly outpaces the spending on public services. With a discrepancy of ${discrepancies['discrepancy'].max():.2f}, this raises concerns about where the collected funds are being allocated, pointing towards potential misuse or lack of transparency.")
    
    # Commission Analysis
    for commission_type in ['liquor', 'cannabis']:
        if f'{commission_type}_commission_analysis' in results:
            analysis = results[f'{commission_type}_commission_analysis']
            min_support_ratio_county = analysis.loc[analysis['support_ratio'].idxmin(), 'county']
            report.append(f"{commission_type.capitalize()} Commission Transparency: The {commission_type} commission in {min_support_ratio_county} shows a support ratio of only {analysis['support_ratio'].min():.2f}, indicating that for every dollar collected, only a fraction is returned to support local businesses. This low ratio suggests a lack of reinvestment into the community, highlighting a potential area of concern for transparency and local economic development.")
    
    # Combine report sections
    full_report = "\n\n".join(report)
    
    # Basic sentiment analysis
    blob = TextBlob(full_report)
    sentiment = blob.sentiment.polarity
    sentiment_text = "concerned" if sentiment < 0 else "neutral" if sentiment == 0 else "optimistic
