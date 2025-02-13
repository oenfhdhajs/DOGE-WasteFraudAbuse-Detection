from flask import Flask, render_template, jsonify
import pandas as pd
import os
import logging

# Setting up logging
logging.basicConfig(filename='interactive_dashboard.log', level=logging.INFO,
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    df = load_data('government_spending_data.csv')
    # Convert DataFrame to a list of dictionaries for JSON serialization
    data = df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    # Ensure the templates directory exists
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
    
    # Create a simple index.html in the templates folder
    with open(os.path.join(template_dir, 'index.html'), 'w') as f:
        f.write('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Interactive DOGE Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Interactive DOGE Dashboard</h1>
            <div id="dataDisplay"></div>
            <script>
                fetch('/data')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('dataDisplay').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                    });
            </script>
        </body>
        </html>
        ''')
    
    app.run(debug=True)
