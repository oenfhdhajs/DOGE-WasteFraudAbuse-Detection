// Using Fetch API to get data from Python script or a local JSON file
function fetchData(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

// Function to display summary statistics
function displaySummaryStats(data) {
    const summaryDiv = document.getElementById('summary-stats');
    summaryDiv.innerHTML = `
        <h2>Summary Statistics</h2>
        <p>Total Records: ${data.totalRecords}</p>
        <p>Fraudulent Cases Detected: ${data.fraudulentCases}</p>
        <p>Waste Identified: $${data.wasteAmount}</p>
        <p>Abuse Incidents: ${data.abuseIncidents}</p>
    `;
}

// Function to create and display a chart for fraud detection
function displayFraudDetectionChart(data) {
    const ctx = document.getElementById('fraud-detection-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.categories,
            datasets: [{
                label: 'Fraudulent Cases',
                data: data.fraudCounts,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to display waste analysis
function displayWasteAnalysis(data) {
    const wasteDiv = document.getElementById('waste-analysis');
    wasteDiv.innerHTML = `
        <h2>Waste Analysis</h2>
        <table>
            <tr>
                <th>Department</th>
                <th>Waste Amount ($)</th>
            </tr>
            ${data.wasteData.map(item => `
                <tr>
                    <td>${item.department}</td>
                    <td>$${item.amount}</td>
                </tr>
            `).join('')}
        </table>
    `;
}

// Function to display abuse monitoring
function displayAbuseMonitoring(data) {
    const abuseDiv = document.getElementById('abuse-monitoring');
    abuseDiv.innerHTML = `
        <h2>Abuse Monitoring</h2>
        <ul>
            ${data.abuseEvents.map(event => `<li>${event.description} - ${event.timestamp}</li>`).join('')}
        </ul>
    `;
}

// Function to display real-time updates
function displayRealTimeUpdates(data) {
    const updatesDiv = document.getElementById('real-time-updates');
    updatesDiv.innerHTML = `
        <h2>Real-Time Updates</h2>
        <p>Last Update: ${new Date(data.lastUpdate).toLocaleString()}</p>
        <ul id="updates-list">
            ${data.updates.map(update => `<li>${update}</li>`).join('')}
        </ul>
    `;
}

// Main function to initialize dashboard
function initDashboard() {
    // Assuming data is served from a local server or file for this example
    fetchData('data.json') // or 'http://localhost:5000/data' if using a server
        .then(data => {
            displaySummaryStats(data);
            displayFraudDetectionChart(data);
            displayWasteAnalysis(data);
            displayAbuseMonitoring(data);
            displayRealTimeUpdates(data);
            
            // Simulate real-time updates
            setInterval(() => {
                fetchData('data.json') // or real-time API endpoint
                    .then(newData => {
                        const updatesList = document.getElementById('updates-list');
                        updatesList.innerHTML += `<li>New update: ${new Date().toLocaleString()}</li>`;
                    });
            }, 60000); // Update every minute
        });
}

// Initialize the dashboard when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initDashboard);
