import json
import os
import matplotlib.pyplot as plt
from datetime import datetime
from flask import Blueprint, send_from_directory, jsonify,current_app


# Create a Blueprint for stock graph routes
stock_graphs_bp = Blueprint('stock_graphs', __name__)

#this works right now in just python this TEST
#if you run this be sure to delete the png images it makes 
#  to work ,warning must put into flask backend if we want graphs in this way png and save them to static/graph 

#can be called this way in frontend dashboard
# <!-- dashboard.component.html -->
# <div *ngFor="let stock of stocks">
#   <h3>{{stock.name}}</h3>
#   <!-- Display the stock graph -->
#   <img [src]="'http://localhost:5000/graphs/' + stock.ticker + '_stock_prices.png'" alt="{{stock.name}} Stock Price Graph">
# </div>

# # Create a Blueprint for stock graph routes
# stock_graphs_bp = Blueprint('stock_graphs', __name__)

def generate_stock_graphs(stock_data_path='stock_data.json', output_dir='static/graphs'):
    """
    Generate stock price graphs from JSON data and save them to specified directory.
    
    :param stock_data_path: Path to the stock data JSON file
    :param output_dir: Directory to save generated graph images
    :return: Dictionary of graph filenames
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Dictionary to store graph filenames
    graph_filenames = {}

    try:
        # Load the stock data from the JSON file
        with open(stock_data_path, 'r') as json_file:
            stock_data = json.load(json_file)

        # Loop through each company's data to generate a plot
        for company, data in stock_data.items():
            try:
                # Extract time and closing prices for plotting
                times = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in data.keys()]
                closing_prices = [entry["Close"] for entry in data.values()]

                # Create a plot
                plt.figure(figsize=(10, 6))

                # Plotting the data with a line
                plt.plot(times, closing_prices, linestyle='-', color='b', linewidth=2, label=company)
                plt.title(f"Stock Price for {company} (Last 7 Days)", fontsize=16)
                plt.xlabel("Date and Time", fontsize=12)
                plt.ylabel("Stock Price (USD)", fontsize=12)

                plt.xticks(rotation=45, ha='right', fontsize=10)
                plt.tight_layout()

                # Add grid for better readability
                plt.grid(True, linestyle='--', alpha=0.6)

                # Add legend
                plt.legend()

                # Save the plot as a PNG file
                filename = f"{company.replace(' ', '_')}_stock_prices.png"
                filepath = os.path.join(output_dir, filename)
                plt.savefig(filepath, dpi=300)
                plt.close()  # Close the plot to free up memory

                # Store the filename
                graph_filenames[company] = filename
                print(f"Graph for {company} saved as {filename}")

            except Exception as e:
                print(f"Error generating graph for {company}: {e}")

    except Exception as e:
        print(f"Error in generate_stock_graphs: {e}")

    return graph_filenames

@stock_graphs_bp.route('/generate_graphs', methods=['GET'])
def generate_graphs_route():
    """
    Route to generate stock graphs on-demand
    """
    try:
        graph_filenames = generate_stock_graphs()
        return jsonify({
            "status": "success", 
            "graphs": graph_filenames,
            "message": "Graphs generated successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

@stock_graphs_bp.route('/graphs/<filename>')
def serve_graph(filename):
    """
    Serve stock graph images from the static/graphs directory
    """
    return send_from_directory('static/graphs', filename)

@stock_graphs_bp.route('/list_graphs', methods=['GET'])
def list_graphs():
    """
    List available graph files
    """
    try:
        graph_dir = 'static/graphs'
        if not os.path.exists(graph_dir):
            os.makedirs(graph_dir)
        
        graph_files = [f for f in os.listdir(graph_dir) if f.endswith('_stock_prices.png')]
        return jsonify({
            "status": "success",
            "graphs": graph_files
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500





# Load the stock data from the JSON file
with open('stock_data.json', 'r') as json_file:
    stock_data = json.load(json_file)

# Loop through each company's data to generate a plot
for company, data in stock_data.items():
    # Extract time and closing prices for plotting
    times = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in data.keys()]
    closing_prices = [entry["Close"] for entry in data.values()]

    # Create a plot
    plt.figure(figsize=(10, 6))

    # Plotting the data with a  line
    plt.plot(times, closing_prices, linestyle='-', color='b', linewidth=2, label=company)
    plt.title(f"Stock Price for {company} (Last 7 Days)", fontsize=16)
    plt.xlabel("Date and Time", fontsize=12)
    plt.ylabel("Stock Price (USD)", fontsize=12)

    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()

    # Add grid for better readability
    plt.grid(True, linestyle='--', alpha=0.6)

    # Save the plot as a PNG file
    plt.savefig(f"{company}_stock_prices.png", dpi=300)

    # Show the plot
    plt.show()

    print(f"Graph for {company} saved as {company}_stock_prices.png")
