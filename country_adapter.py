import json
import os
import logging
from datetime import datetime

# Setting up logging
logging.basicConfig(filename='international_adaptation.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def load_country_config(country_code):
    """
    Load configuration for a specific country.
    
    :param country_code: ISO 3166-1 alpha-2 country code
    :return: Dictionary with country-specific configurations
    """
    config_path = os.path.join(os.path.dirname(__file__), 'country_config.json')
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config.get(country_code, {})
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from {config_path}")
        return {}

def adapt_for_country(country_code):
    """
    Adapt the project setup for the specified country.
    
    :param country_code: ISO 3166-1 alpha-2 country code
    """
    country_config = load_country_config(country_code)
    
    if not country_config:
        logging.error(f"No configuration found for country code: {country_code}")
        return
    
    # Update data paths
    data_path = country_config.get('data_path', 'government_spending_data.csv')
    logging.info(f"Adapting for {country_code} with data path: {data_path}")
    
    # Update SQL scripts
    sql_path = os.path.join(os.path.dirname(__file__), '..', 'sql_queries')
    for script in ['data_retrieval.sql', 'data_analysis.sql', 'data_insertion.sql']:
        with open(os.path.join(sql_path, script), 'r') as file:
            content = file.read()
        
        # Replace placeholders with country-specific details
        for key, value in country_config.get('sql_placeholders', {}).items():
            content = content.replace(f'${key}', value)
        
        with open(os.path.join(sql_path, f'{country_code}_{script}'), 'w') as file:
            file.write(content)
        logging.info(f"SQL script {script} adapted for {country_code}")
    
    # Update Python scripts if necessary
    python_path = os.path.join(os.path.dirname(__file__), '..', 'python_scripts')
    for script in ['main.py', 'validate_data.py', 'generate_reports.py', 'admin_tools.py', 'time_series_analysis.py', 'network_analysis.py', 'security_audit.py', 'ai_assistant.py']:
        with open(os.path.join(python_path, script), 'r') as file:
            content = file.read()
        
        # Replace placeholders with country-specific details
        for key, value in country_config.get('python_placeholders', {}).items():
            content = content.replace(f'${key}', value)
        
        with open(os.path.join(python_path, f'{country_code}_{script}'), 'w') as file:
            file.write(content)
        logging.info(f"Python script {script} adapted for {country_code}")
    
    # Update HTML template if necessary
    template_path = os.path.join(os.path.dirname(__file__), '..', 'ai_assistant', 'templates')
    with open(os.path.join(template_path, 'chat_interface.html'), 'r') as file:
        content = file.read()
    
    # Replace placeholders in HTML
    for key, value in country_config.get('html_placeholders', {}).items():
        content = content.replace(f'${key}', value)
    
    with open(os.path.join(template_path, f'{country_code}_chat_interface.html'), 'w') as file:
        file.write(content)
    logging.info(f"HTML template adapted for {country_code}")
    
    logging.info(f"Adaptation for {country_code} completed")

def main():
    country_code = input("Enter the country code (ISO 3166-1 alpha-2) to adapt the project for: ")
    adapt_for_country(country_code)

if __name__ == "__main__":
    main()
