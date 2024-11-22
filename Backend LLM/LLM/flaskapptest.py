import os
import json
import config
from flask import Flask, request, render_template
import logging
import re
from crewai import Agent, Task, Crew, LLM
from langchain_groq import ChatGroq
import yfinance as yf

# Configure environment variables for API keys and model names
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3-70b-8192"
os.environ["GROQ_API_KEY"] = config.groqapiekey
os.environ["OPENAI_API_KEY"] = config.chatopenaiapikey

# Set up Flask and logging
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Define a function to format text by converting Markdown bold syntax to HTML strong tags
def format_output(text):
    """Convert Markdown bold syntax to HTML strong tags."""
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

# Set up agents and tasks
ollama3 = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
Gllm = ChatGroq(model_name="groq/llama3-70b-8192", temperature=0.3, max_tokens=4096)

# Define agents
researcher_agent = Agent(
    role="Company Researcher",
    goal="To research the given company or crypto coin and provide financial insights.",
    backstory="In-depth knowledge of stocks and company financials.",
    llm=ollama3
)

accountant_agent = Agent(
    role="Accountant Agent",
    goal="General accounting tasks, including transaction processing and financial reporting.",
    backstory="Responsible for financial report generation.",
    llm=Gllm
)

recommender_agent = Agent(
    role="Recommender Agent",
    goal="To recommend whether it is a good financial decision to purchase, hold or sell stocks, and give a percentage out of 100 for each option.",
    backstory="You are an experienced financial analyst specializing in stock recommendations. You are an expert in technical market trends and patterns and work closely with the Accountant agent to receive financial data for accurate recommendations.",
    llm=ollama3
)

Yahoo_Recommender_agent = Agent(
    role="Yahoo Recommender Agent",
    goal="To recommend whether it is a good financial decision to purchase, hold or sell stocks, and give a percentage out of 100 for each option. Provide a timeline for the past 7 days.",
    backstory="You are an experienced financial analyst specializing in stock recommendations with a focus on technical market trends and patterns. You work closely with the Accountant agent to receive financial data for accurate recommendations.",
    llm=ollama3
)

blogger_agent = Agent(
    role="Blogger Agent",
    goal="Write short and informative blogs in a structured format to aid quick decision-making.",
    backstory="Loves to write short, accurate, and detailed blogs on a given input query.",
    llm=ollama3
)

# Define route for home page
@app.route('/', methods=['GET', 'POST'])
def main():
    query_input = None
    output = None
    if request.method == 'POST':
        # Test at home
        query_input = request.form.get('query-input')

        # Actual implementation
        # query_input = request.data

        if query_input:
            try:
                # Define tasks
                researcher_task = Task(
                    description="Research financial data for " + str(query_input) + " using Yahoo Finance news as of today's date",
                    agent=researcher_agent,
                    expected_output="Latest financial insights for making predictions."
                )

                accountant_task = Task(
                    description=f"Calculate accounting ratios for the company, {researcher_task}",
                    agent=accountant_agent,
                    expected_output="""A summary of financial leverage, such as debt-to-equity ratio.
                    {
                        "stock_symbol": str,
                        "financial_metrics": {
                            "pe_ratio": float,
                            "debt_to_equity": float,
                            "current_ratio": float,
                            "profit_margin": float
                        },
                        "cash_flow_analysis": {
                            "operating_cash_flow": float,
                            "free_cash_flow": float
                        },
                        "growth_metrics": {
                            "revenue_growth": float,
                            "earnings_growth": float
                        }
                    }""",
                    dependencies=[researcher_task]
                )

                recommender_task = Task(
                    description=f"Generate stock recommendations based on financial analysis {accountant_task}",
                    agent=recommender_agent,
                    expected_output="""{
                        "recommendation": {
                            "stock_symbol": str,
                            "action": "BUY" | "HOLD" | "SELL",
                            "target_price": float,
                            "position_size": float,
                            "risk_level": str,
                            "rationale": str,
                            "supporting_metrics": {
                                "technical_indicators": dict,
                                "fundamental_factors": dict,
                                "risk_metrics": dict
                            },
                            "entry_strategy": str,
                            "exit_criteria": str,
                            "timeline": str
                        },
                        "market_context": {
                            "current_market_conditions": str,
                            "sector_analysis": str,
                            "relevant_news": list
                        },
                        "risk_assessment": {
                            "potential_upside": float,
                            "potential_downside": float,
                            "risk_reward_ratio": float
                        }
                    }""",
                    dependencies=[accountant_task]
                )

                Yahoo_Recommender_Task = Task(
                    description=f"Generate stock recommendations based on financial analysis {accountant_task}",
                    agent=Yahoo_Recommender_agent,
                    expected_output="""{
                        "recommendation": {
                            "stock_symbol": str,
                            "action": "BUY" | "HOLD" | "SELL",
                            "target_price": float,
                            "position_size": float,
                            "risk_level": str,
                            "rationale": str,
                            "supporting_metrics": {
                                "technical_indicators": dict,
                                "fundamental_factors": dict,
                                "risk_metrics": dict
                            },
                            "entry_strategy": str,
                            "exit_criteria": str,
                            "timeline": str
                        },
                        "market_context": {
                            "current_market_conditions": str,
                            "sector_analysis": str,
                            "relevant_news": list
                        },
                        "risk_assessment": {
                            "potential_upside": float,
                            "potential_downside": float,
                            "risk_reward_ratio": float
                        }
                    }""",
                    dependencies=[accountant_task]
                )

                blogger_task = Task(
                    description=f"{recommender_task}",
                    agent=blogger_agent,
                    expected_output="""{
                        "blog": "{Informative detailed blog goes here}",
                        "recommendation": {
                            "buy": "x%",
                            "hold": "y%",
                            "sell": "z%"
                        },
                        "date": "{Date from which you got this information}"
                    }"""
                )

                # Execute tasks with Crew
                crew = Crew(agents=[researcher_agent, accountant_agent, blogger_agent,Yahoo_Recommender_agent], tasks=[researcher_task, accountant_task, blogger_task,Yahoo_Recommender_Task], verbose=False)
                result = crew.kickoff()

                output = format_output(str(result))
            except Exception as e:
                logging.error(f"Error during task execution: {e}")
                output = "Sorry, an error occurred while processing your request."

    return render_template('index.html', query_input=query_input, output=output)

# Yahoo Recommender agent function
@app.route('/stock', methods=['GET', 'POST'])
def stock_recommendation():
    if request.method == 'POST':
        # Use the stock symbol from accountant_task
        stock_symbol = accountant_task.result.get("stock_symbol")  # Assume accountant_task has run and has a result

        if stock_symbol:
            latest_prices = get_stock_data(stock_symbol)
            if latest_prices:
                output = f"The latest closing prices for {stock_symbol} over the past 7 days are: {latest_prices}. Use this data for financial recommendations."
            else:
                output = "Failed to fetch the latest stock prices."
        else:
            output = "Stock symbol not found in accountant_task result."

        return output

    return "Please send a POST request to get stock recommendations."

# Function to fetch stock data using Yahoo Finance
def get_stock_data(stock_symbol):
    """Fetch the latest stock data using Yahoo Finance."""
    try:
        stock = yf.Ticker(stock_symbol)
        latest_prices = stock.history(period='7d')['Close'].tolist()  # Get the last 7 closing prices as a list
        return latest_prices
    except Exception as e:
        logging.error(f"Error fetching stock data for {stock_symbol}: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
