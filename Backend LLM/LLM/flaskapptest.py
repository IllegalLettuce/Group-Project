import os

import json

import config
from flask import Flask, request, render_template
import logging
import re
from crewai import Agent, Task, Crew, LLM
from langchain_groq import ChatGroq


# Import required modules from langchain_community, crewai, etc.



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
# ollama3 = LLM(model="ollama/llama3.2", base_url="https://quiet-yak-presently.ngrok-free.app")
Gllm = ChatGroq(model_name="groq/llama3-70b-8192", temperature=0.3, max_tokens=4096)

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
    goal="To recommend whether it is a good financial decision to purchase, hold or sell stocks, and give a percentage out of a 100 for each option",
    backstory="You are an experienced financial analyst specializing in stock recommendations, you are an expert in technical market trends and patterns , you work closely with the Accountant agent to recieve financial data to give accurate recommendations",
    llm=ollama3
)
 
blogger_agent = Agent(
    role="Blogger Agent",
    goal="write short and informative blogs in a set stucture where quick decisions need to be made ",
    backstory="loves to Write  short accurate detailed informative blogs, on a given input query.",
    llm=ollama3
)










# Define route for home page
@app.route('/', methods=['GET', 'POST'])
def main():
    query_input = None
    output = None
    if request.method == 'POST':

        # test at home
        # query_input = request.form.get('query-input')

        # actual implementation
        query_input = request.data


        if query_input:
            try:

                researcher_task = Task(
                    description="Research financial data for " + str(query_input) + " using yahoo finance news as of todays date",
                    agent=researcher_agent,
                    expected_output="Latest financial insights for making predictions."
                )


                accountant_task = Task(
                    description=f"Calculate accounting ratios for the company,{researcher_task}",
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
                        }
                        """,
                        dependency =[researcher_task]

                )



                recommender_task = Task(
                    description=f"Generate stock recommendations based on financial analysis {accountant_task}",
                    agent=recommender_agent,
                    expected_output="""
                        {
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
                        }
                        """,
                    dependencies=[accountant_task]
                )


                blogger_task = Task(
                    description=f"{recommender_task}",
                    agent=blogger_agent,
                    # expected_output="A very short informative detailed blog about how well a company is doing, and recommended percentages for buy|sell|hold"
                    expected_output="A very short informative detailed blog about how well a company is doing (about 20 words), and recommended percentages for buy|sell|hold which would be in the format of Buy : x% , Hold: y% , Sell: z% (dont write anything extra, and output it in this Json format"
                                    "{"
                                    '"blog": "{Informative detailed blog goes here}",'
                                   ' "recommendation": {'
                                  '"buy"": "x%",'
                                '"hold": "y%",'
                                '"sell": "z%"'
                               " },"
                                '"date":(date from which you got this information from)'
                               " }"

                )
                crew = Crew(agents=[researcher_agent, accountant_agent, blogger_agent], tasks=[researcher_task, accountant_task, blogger_task], verbose=True)
                result = crew.kickoff()

                result = str(result)

                print(result)

                output = format_output(result)
                # for json
                jsonobject = json.loads(output)
                # actual implementation
                return jsonobject



            except Exception as e:
                logging.error(f"Error during task execution: {e}")
                output = "Sorry, an error occurred while processing your request."

    # else:
    #     return 'Welcome! Send a POST request to submit data.', 200

    # test at home
    # return render_template('index.html', query_input=query_input, output=output)


if __name__ == '__main__':
    app.run(debug=True)