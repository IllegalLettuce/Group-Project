import os

import json
import time

# from google.cloud.firestore_v1 import FieldFilter
# from sagemaker.workflow.airflow import processing_config
# from sympy import false

import datetime

from sympy.physics.units import temperature

import config
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import logging
import re
from crewai import Agent, Task, Crew, LLM
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import (
    WebsiteSearchTool
)


# Import required modules from langchain_community, crewai, etc.


# Configure environment variables for API keys and model names
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3-70b-8192"
os.environ["GROQ_API_KEY"] = config.groqapiekey
os.environ["GOOGLE_API_KEY"] = config.googleapikey
os.environ["GEMINI_API_KEY"] = config.googleapikey

# web_rag_tool = WebsiteSearchTool()



# Set up Flask and logging
app = Flask(__name__)
# CORS(app, origins=["http://localhost:4200"])
CORS(app)
logging.basicConfig(level=logging.DEBUG)





# Define a function to format text by converting Markdown bold syntax to HTML strong tags
def format_output(text):
    """Convert Markdown bold syntax to HTML strong tags."""
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)


# Set up agents and tasks
ollama3 = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
Gllm = ChatGroq(model_name="groq/llama3-70b-8192", temperature=0.3, max_tokens=4096)
gemini = ChatGoogleGenerativeAI(model="gemini/gemini-1.5-flash",temperature=0.5)
gem = LLM(model="gemini/gemini-1.5-flash",temperature=0.5)
researcher_agent = Agent(
    role="Company Researcher",
    goal="To research the given company or crypto coin and provide financial insights.",
    backstory="In-depth knowledge of stocks and company financials.",
    # tools = [web_rag_tool],
    llm = gem
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



autopurchase_agent = Agent(
    role="Stock analysis and future predictor",
    goal="Give the predicted buy, sell and hold percentages ",
    backstory="Enjoys looking at stock analysis from people and coming up with their own prediction ",
    llm=ollama3
)


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
##r is necessary to tell python that its a file path
cred = credentials.Certificate(r"C:\Users\spenc\Desktop\MTU stuff\Software Dev Year 3\Semester 1\Group Project\firebasekey\year3groupproject-ee682-firebase-adminsdk-zdtvf-2484fe8f8a.json")

firebase_admin.initialize_app(cred)

db = firestore.client()

data = {
    'task' : 'Waayaya',
    'status': 'Toodoo'
}

##the collection you want data in
collection = db.collection('shares').document()
##addint data to the collection
collection.set(data)

print("Document ID: ",collection.id)


@app.route('/manages', methods=['POST','OPTIONS','GET'])
#receive a request with the ticker symbol
#the funds which can be used to purchase
#the separate percentages



def autopurchase():

    if request.method == 'POST':
        print("Hi")
        # while(True):
        #
        #     time.sleep((60*60*2)) for a constant loop put this around the code below
        # try:
        #
        #
        #     ##gotta figure out how to run this for ones that dont have any stock purchased and others which do,
        #     #in the stock, we gotta save USER ID and Ticker, to identify the stuff
        #     data = request.get_json()
        #     company = data.get('company')
        #     ticker = data.get('ticker')
        #     buy = data.get('buy_percent')
        #     sell = data.get('sell_percent')
        #     funds = data.get('funds_dollar')
        #
        #
        #     autopurchase_task = Task(
        #         description="From the data given make a prediction as to whether the given stock buy, sell and hold percentages are going to increase is decrease"
        #                     " the data is here "+ datafromapi,
        #         agent=autopurchase_agent,
        #         expected_output="I expect the output to be given like this and nothing more."
        #                         "{"
        #                         '"buy"": "x%",'
        #                         '"sell": "z%"'
        #                         "}"
        #     )
        #     crew = Crew(agents=[autopurchase_agent],
        #                 tasks=[autopurchase_task], verbose=True)
        #     result = crew.kickoff()
        #
        #     result = str(result)
        #     jsonobject = json.loads(result)
        #
        #
        #
        #     agent_buy = jsonobject.get('buy')
        #     agent_sell = jsonobject.get('sell')
        #     price_per_share = pricefromapi
        #
        #
        #     docs = (
        #         db.collection("shares")
        #         .where(filter=FieldFilter("user_id", "==", userid) and FieldFilter("ticker", "==", ticker) )
        #         .stream()
        #     )
        #
        #     docs = list(docs)
        #
        #     sharesowned = 0
        #     document_id = 0
        #     if docs:
        #         for doc in docs:
        #             sharesowned = doc.get('sharebought')
        #             document_id = doc.id
        #     #if the buy from API is greater than the given from user, then go ahead and buy as many stocks as possible until you can buy anymore
        #     #then save that into the firebase database
        #
        #     if agent_buy>=buy:
        #         sharesowned  += funds / price_per_share
        #
        #         #save share bought , ticker, user id into database so it can be retrieved for future use
        #     else:
        #         if agent_sell >= sell:
        #         #get the share from database and sell them all
        #             newfunds = price_per_share * sharesowned
        #             sharesowned = 0
        #         #remove share from the database
        #
        #     if document_id != 0:
        #         doc_ref = db.collection("shares").document(document_id)
        #         doc_ref.set({"sharesOwned": 100}, merge=True)
        #
        #
        #     return jsonify({
        #         "status": "success",
        #         "message": company
        #     }), 200
        # except Exception as e:
        #     logging.error(f"Error during task execution: {e}")
        #     output = "Sorry, an error occurred while processing your request."






# Define route for home page

@app.route('/report', methods=['GET', 'POST'])
def main():
    query_input = None
    output = None


    if request.method == 'POST' or request.method == 'GET':

        # test at home
        # query_input = request.form.get('query-input')

        # actual implementation
        # query_input = json.loads(request.data.decode('utf-8'))
        query_input = request.data
        # companyname = query_input.get('company')
        # print(companyname)




        if query_input:

            ##TESTING




            try:

                researcher_task = Task(
                    description="Research financial data for " + str(
                        query_input) + " using yahoo finance news as of todays date",
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
                    dependency=[researcher_task]

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
                                    '"extended_blog": "{Information of blog goes here but a bit more detail}"'
                                    ' "recommendation": {'
                                    '"buy"": "x%",'
                                    '"hold": "y%",'
                                    '"sell": "z%"'
                                    " },"
                                    '"date":(date from which you got this information from)'
                                    " }"

                )
                crew = Crew(agents=[researcher_agent, accountant_agent,recommender_agent, blogger_agent],
                            tasks=[researcher_task, accountant_task,recommender_task, blogger_task], verbose=True)

                # crew = Crew(agents=[researcher_agent],
                #             tasks=[researcher_task], verbose=True)
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


#auto purchase
@app.route('/manages', methods=['POST','OPTIONS','GET'])
def maintesing():
    query_input = None
    output = None

    if request.method == 'Posts':
        # Ensure the request contains JSON data
        if request.content_type != 'application/json':
            return jsonify({
                "status": "error",
                "message": "Content-Type must be application/json"
            }), 42069

    if request.method == 'GET':
        # Ensure the request contains JSON data

        return jsonify({
            "company": "NewCOmpz",
            "buy_percent": 50,
            "sell_percent":50,
            "funds_dollar":100
        }), 200
        if request.content_type != 'application/json':
            return jsonify({
                "status": "error",
                "message": "Content-Type must be application/json"
            }), 42069


    if request.method == 'POST':

        # test at home
        # query_input = request.form.get('query-input')

        # actual implementation
        query_input = request.data.ty
        companyname = query_input.get('company', None)
        print(companyname)

        if query_input:


            ##TESTING

            # resp = '{"hello":"WAASASASA"}'
            # jsonobject = json.loads(resp)
            return str(companyname)
            try:

                researcher_task = Task(
                    description="Research financial data for " + str(
                        query_input) + " using yahoo finance news as of todays date",
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
                    dependency=[researcher_task]

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
                crew = Crew(agents=[researcher_agent, accountant_agent, blogger_agent],
                            tasks=[researcher_task, accountant_task, blogger_task], verbose=True)
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



@app.route('/manage', methods=['POST', 'OPTIONS'])
def maintes():
    if request.method == 'POST':
        # Log the Content-Type header
        print(f"Content-Type received: {request.content_type}")
        if request.content_type != 'application/json':
            return jsonify({
                "status": "error",
                "message": "Content-Type must be application/json"
            }), 200

        else:
            # Example success response for valid JSON POST request

            data = request.get_json()
            company = data.get('company')
            # buy = data.get('buy_percent')
            # sell = data.get('sell_percent')
            # funds = data.get('funds_dollar')


            return jsonify({
                "status": "success",
                "message": company
            }), 200

    elif request.method == 'OPTIONS':
        # Respond to preflight requests if needed
        return jsonify({
            "status": "info",
            "message": "OPTIONS request received"
        }), 200

    # Fallback for unexpected cases
    return jsonify({
        "status": "error",
        "message": "Unexpected method"
    }), 400




#report
@app.route('/report', methods=['POST','GET'])
def reporttes():
    query_input = None
    output = None

    if request.method == 'POST':
        # Ensure the request contains JSON data
        return jsonify({
            "status": "OK",
            "response": "POST request received"
        }), 200


    if request.method == 'GET':
        # Ensure the request contains JSON data

        return "Post Request Recived", 200

import datetime
date = datetime.datetime.now()


@app.route('/', methods=['GET', 'POST'])
def home():
    query_input = None
    output = None


    if request.method == 'POST' or request.method == 'GET':

        # test at home
        query_input = request.form.get('query-input')



        # actual implementation
        # query_input = json.loads(request.data.decode('utf-8'))
        # query_input = request.data
        # companyname = query_input.get('company')
        # print(companyname)




        if query_input:

            ##TESTING




            try:

                researcher_task = Task(
                    description="Research financial data for " + str(
                        query_input) + " using yahoo finance news as of " +str(date),
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
                    dependency=[researcher_task]

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
                                    '"extended_blog": "{Information of blog goes here but a bit more detail}"'
                                    ' "recommendation": {'
                                    '"buy"": "x%",'
                                    '"hold": "y%",'
                                    '"sell": "z%"'
                                    " },"
                                    '"date":(date from which you got this information from)'
                                    " }"

                )
                crew = Crew(agents=[researcher_agent, accountant_agent,recommender_agent, blogger_agent],
                            tasks=[researcher_task, accountant_task,recommender_task, blogger_task], verbose=True)

                result = crew.kickoff()

                result = str(result)

                print(result)

                output = format_output(result)
                # for json
                # jsonobject = json.loads(output)
                # actual implementation
                # return jsonobject



            except Exception as e:
                logging.error(f"Error during task execution: {e}")
                output = "Sorry, an error occurred while processing your request."

    # else:
    #     return 'Welcome! Send a POST request to submit data.', 200

    # test at home
    return render_template('index.html', query_input=query_input, output=output)



if __name__ == '__main__':
    app.run(debug=True)
