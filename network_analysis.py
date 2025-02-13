import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import logging

# Setting up logging
logging.basicConfig(filename='network_analysis.log', level=logging.INFO,
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

def build_network(df):
    """
    Build a network graph from transaction data to find relationships.
    
    :param df: DataFrame with transaction details
    :return: NetworkX graph object
    """
    G = nx.Graph()
    
    # Adding edges based on transactions between departments or entities
    for _, row in df.iterrows():
        G.add_edge(row['department'], row['vendor'], weight=row['amount'])
    
    logging.info(f"Network graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G

def analyze_network(G):
    """
    Analyze the network for potential collusion or unusual patterns.
    
    :param G: NetworkX graph object
    """
    # Degree centrality - to find key players
    degree_centrality = nx.degree_centrality(G)
    
    # Betweenness centrality - to find nodes that control the flow
    betweenness_centrality = nx.betweenness_centrality(G)
    
    # Plot the network
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=8, font_weight='bold')
    plt.title('Network of Transactions')
    plt.savefig('transaction_network.png')
    plt.close()
    
    # Log top 5 nodes by degree and betweenness centrality
    top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    
    logging.info("Top 5 nodes by degree centrality:")
    for node, centrality in top_degree:
        logging.info(f"{node}: {centrality}")
    
    logging.info("Top 5 nodes by betweenness centrality:")
    for node, centrality in top_betweenness:
        logging.info(f"{node}: {centrality}")

def main():
    data_path = 'government_spending_data.csv'
    df = load_data(data_path)
    G = build_network(df)
    analyze_network(G)

if __name__ == "__main__":
    main()
