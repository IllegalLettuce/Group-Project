import json
import matplotlib.pyplot as plt
from datetime import datetime



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
