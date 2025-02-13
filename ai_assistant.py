import pandas as pd
from flask import Flask, render_template, request, jsonify
import logging
from datetime import datetime
import subprocess
import os
from textblob import TextBlob

# Importing necessary functions from previous scripts
from validate_data import validate_data
from generate_reports import generate_fraud_report, generate_waste_report
from admin_tools import backup_database, manage_users
from time_series_analysis import perform_time_series_analysis
from network_analysis import build_network, analyze_network
from security_audit import run_security_scan, check_database_privileges

# Setting up logging
logging.basicConfig(filename='ai_assistant.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)

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

def analyze_and_report():
    """
    Perform all analyses and generate reports, then summarize them for the AI assistant.
    """
    df = load_data('government_spending_data.csv')
    
    # Data Validation
    validation_results = validate_data(df)
    validation_summary = f"Data validation found {validation_results.get('missing_values', 0)} missing values and {validation_results.get('duplicates', 0)} duplicates."
    
    # Generate Reports
    report_dir = 'reports_' + datetime.now().strftime("%Y%m%d_%H%M%S")
    generate_fraud_report(df, report_dir)
    generate_waste_report(df, report_dir)
    report_summary = f"Fraud report and waste report generated. Check {report_dir} for details."
    
    # Time Series Analysis
    perform_time_series_analysis(df)
    time_series_summary = "Time series analysis completed, showing trends in spending over time."
    
    # Network Analysis
    G = build_network(df)
    analyze_network(G)
    network_summary = "Network analysis performed, revealing potential collusion or unusual transaction patterns."
    
    # System Administration
    backup_database('government_spending_db', 'backups')
    manage_users('create', 'ai_user', 'read_only')
    admin_summary = "Database backed up and a new user 'ai_user' with read-only permissions created."
    
    # Security and Compliance
    run_security_scan()
    check_database_privileges()
    security_summary = "Security scan and database privilege check completed."
    
    # Combine all summaries
    full_summary = f"{validation_summary}\n{report_summary}\n{time_series_summary}\n{network_summary}\n{admin_summary}\n{security_summary}"
    
    # Use TextBlob for basic natural language processing
    blob = TextBlob(full_summary)
    sentiment = blob.sentiment.polarity
    sentiment_text = "positive" if sentiment > 0 else "neutral" if sentiment == 0 else "negative"
    
    return f"AI Assistant Report:\n\n{full_summary}\n\nSentiment of the report: {sentiment_text}"

@app.route('/')
def index():
    return render_template('assistant_response.html')

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    query = request.form.get('query')
    if query.lower() == 'report':
        response = analyze_and_report()
    else:
        response = "I can provide a detailed report on the current state of the project. Type 'report' to get it."
    
    return jsonify({'response': response})

if __name__ == '__main__':
    # Ensure the templates directory exists
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
    
    # Create a simple index.html in the templates folder for the AI assistant
    with open(os.path.join(template_dir, 'assistant_response.html'), 'w') as f:
        f.write('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI Assistant for DOGE Project</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                #response { white-space: pre-wrap; border: 1px solid #ccc; padding: 10px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1>AI Assistant for DOGE Project</h1>
            <form id="queryForm" method="post" action="/ask_ai">
                <input type="text" id="query" name="query" placeholder="Type 'report' for a summary">
                <button type="submit">Ask AI</button>
            </form>
            <div id="response"></div>
            <script>
                document.getElementById('queryForm').addEventListener('submit', function(event) {
                    event.preventDefault();
                    fetch('/ask_ai', {
                        method: 'POST',
                        body: new FormData(this)
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('response').innerText = data.response;
                    });
                });
            </script>
        </body>
        </html>
        ''')
    
    app.run(debug=True)
