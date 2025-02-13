import pandas as pd
from textblob import TextBlob
import logging

# Setting up logging
logging.basicConfig(filename='county_corruption_narrative.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def load_analysis_results():
    """
    Load the results from the previous analysis.
    
    :return: Dictionary with analysis results
    """
    results = {}
    for file in ['salary_stats.csv', 'total_worth_stats.csv', 'fees_fines.csv', 'commissions.csv']:
        try:
            results[file.replace('.csv', '')] = pd.read_csv(file)
        except FileNotFoundError:
            logging.error(f"File not found: {file}")
    
    return results

def generate_narrative(results):
    """
    Generate a narrative report based on the analysis results.
    
    :param results: Dictionary with analysis results
    :return: String containing the narrative report
    """
    narrative = []
    
    # Salaries and Total Worth
    max_salary_county = results['salary_stats'].loc[results['salary_stats']['max'].idxmax(), 'county']
    max_worth_county = results['total_worth_stats'].loc[results['total_worth_stats']['max'].idxmax(), 'county']
    narrative.append(f"In our analysis, {max_salary_county} county shows the highest maximum salary at ${results['salary_stats']['max'].max():.2f}, suggesting potential overcompensation or misuse of public funds. Meanwhile, {max_worth_county} county leads with the highest reported total worth at ${results['total_worth_stats']['max'].max():.2f}, raising questions about the accumulation of wealth among local officials.")
    
    # Fees and Fines
    max_fees_county = results['fees_fines'].loc[results['fees_fines']['fees'].idxmax(), 'county']
    max_fines_county = results['fees_fines'].loc[results['fees_fines']['fines'].idxmax(), 'county']
    narrative.append(f"Looking at fees and fines, {max_fees_county} county has collected an exorbitant amount in fees, totaling ${results['fees_fines']['fees'].max():.2f}, which might indicate overcharging or unnecessary financial burdens on its residents. Similarly, {max_fines_county} county's fines total ${results['fees_fines']['fines'].max():.2f}, possibly reflecting aggressive enforcement practices or revenue generation through punitive measures.")
    
    # Commissions
    for commission_type in ['Liquor', 'Cannabis']:
        if commission_type in results['commissions'].columns:
            max_commission_county = results['commissions'][results['commissions'][commission_type] == results['commissions'][commission_type].max()].index[0]
            narrative.append(f"The {commission_type.lower()} commission in {max_commission_county} county has amassed ${results['commissions'][commission_type].max():.2f}, yet there is little to show for this income in terms of public benefit or transparency, suggesting potential misallocation or corruption.")
    
    # Enforcement and Court Correlation
    if 'enforcement_court_correlation' in results:
        corr_value = results['enforcement_court_correlation']
        narrative.append(f"An interesting correlation of {corr_value:.2f} was found between enforcement actions and court outcomes, indicating a possible symbiotic relationship where enforcement might be used to generate court business, or vice versa, which could be indicative of systemic corruption.")
    
    # Combine narratives
    full_narrative = "\n\n".join(narrative)
    
    # Basic sentiment analysis
    blob = TextBlob(full_narrative)
    sentiment = blob.sentiment.polarity
    sentiment_text = "concerned" if sentiment < 0 else "neutral" if sentiment == 0 else "optimistic"
    
    full_narrative += f"\n\nSentiment of this report: {sentiment_text}"
    
    logging.info("Narrative report generated")
    return full_narrative

def main():
    results = load_analysis_results()
    narrative = generate_narrative(results)
    
    # Save the narrative to a text file
    with open('county_corruption_narrative.txt', 'w') as file:
        file.write(narrative)
    
    logging.info("Narrative saved to county_corruption_narrative.txt")

if __name__ == "__main__":
    main()
