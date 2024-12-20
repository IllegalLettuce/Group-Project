import os

import json
import time
from threading import Thread

from google.cloud.firestore_v1 import FieldFilter


import config
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import logging
import re
from crewai import Agent, Task, Crew, LLM
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import yfinance as yf
from crewai_tools import WebsiteSearchTool

import datetime
date = datetime.datetime.now()


# Configure environment variables for API keys and model names
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3-70b-8192"
os.environ["GROQ_API_KEY"] = config.groqapiekey
os.environ["GOOGLE_API_KEY"] = config.googleapikey
os.environ["GEMINI_API_KEY"] = config.googleapikey
os.environ["OTEL_SDK_DISABLED"] = "true" ## to get rid of that telemetry error at after executing agent tasks
os.environ["OPENAI_API_KEY"] = config.chatopenaiapikey # need this cause otherwise the app has a meltdown even though we arent using this anyway

web_rag_tool = WebsiteSearchTool



# Set up Flask and logging
app = Flask(__name__)
# CORS(app, origins=["http://localhost:4200"])
CORS(app)
logging.basicConfig(level=logging.DEBUG)

##################################################################
#yfinance stocks 
stocks = [
    {"name": "Lockheed Martin", "ticker": "LMT"},
    {"name": "General Dynamics", "ticker": "GD"},
    {"name": "Northrop Grumman", "ticker": "NOC"},
    {"name": "RTX", "ticker": "RTX"},
    {"name": "Boeing", "ticker": "BA"},
    {"name": "L3Harris", "ticker": "LHX"},
    {"name": "Rheinmetall", "ticker": "RHM.DE"},
    {"name": "SAAB", "ticker": "SAAB-B.ST"},
    {"name": "Hensoldt", "ticker": "HAG.DE"},
    {"name": "Leonardo", "ticker": "LDO.MI"},
    {"name": "Dodge","ticker":""},
    {"name": "Bitcoin","ticker":""},
    {"name":"XHR","ticker":""}
]

# Define a function to format text by converting Markdown bold syntax to HTML strong tags
def format_output(text):
    """Convert Markdown bold syntax to HTML strong tags."""
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

# Set up agents and tasks
ollama3 = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
Gllm = ChatGroq(model_name="groq/llama3-70b-8192", temperature=0.3, max_tokens=4096)
gemini = ChatGoogleGenerativeAI(model="gemini/gemini-1.5-flash",temperature=0.5)
gem = LLM(model="gemini/gemini-1.5-flash",temperature=0.5)

tool = WebsiteSearchTool(
    website="https://google.com",
    config=dict(
        llm=dict(
            provider="google", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="gemini/gemini-1.5-flash",
                temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)

researcher_agent = Agent(
    role="Company Researcher",
    goal="To research the given company or crypto coin and provide financial insights.",
    backstory="In-depth knowledge of stocks and company financials.",
    tools = [tool],
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
    goal="Give the predicted buy and sell ",
    backstory="Enjoys looking at stock analysis from people and coming up with their own prediction ",
    llm=ollama3
)


import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
##r is necessary to tell python that its a file path
#############################################################################################################################################
# cred = credentials.Certificate(r"C:\Users\rthar\OneDrive\Desktop\firebase llm copy\firebasekey.json")#rory firebase key
cred = credentials.Certificate(r"C:\Users\spenc\Desktop\MTU stuff\Software Dev Year 3\Semester 1\Group Project\firebasekey\year3groupproject-ee682-firebase-adminsdk-zdtvf-2484fe8f8a.json")#ferenc firebase key
#################################################################################################################################################
firebase_admin.initialize_app(cred)

db = firestore.client()



#############################################################################################
def fetch_intraday_data_yahoo(ticker, interval="15m", period="5d"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(interval=interval, period=period)
        
        if hist.empty:
            print(f"No intraday data found for {ticker}.")
            return None

        data = hist[["Open", "High", "Low", "Close", "Volume"]].to_dict(orient="index")
        
        formatted_data = {
            date.strftime("%Y-%m-%d %H:%M:%S"): {
                "Open": float(values["Open"]),
                "High": float(values["High"]),
                "Low": float(values["Low"]),
                "Close": float(values["Close"]),
                "Volume": int(values["Volume"]),
            }
            for date, values in data.items()
        }
        
        return formatted_data
    
    except Exception as e:
        print(f"Error fetching intraday data for {ticker}: {e}")
        return None
    
def get_stock_data(stock_symbol):
    """Fetch the latest stock data using Yahoo Finance."""
    try:
        stock = yf.Ticker(stock_symbol)
        latest_prices = stock.history(period='7d')['Close'].tolist()
        return latest_prices
    except Exception as e:
        logging.error(f"Error fetching stock data for {stock_symbol}: {e}")
        return None

# Add a new route for stock data
@app.route('/stock', methods=['GET', 'POST'])
def stock_recommendation():
    if request.method == 'POST':
        data = request.get_json()
        stock_symbol = data.get("companay_ticker")  # Note: there's a typo in the original (companay)

        if stock_symbol:
            latest_prices = get_stock_data(stock_symbol)

            if latest_prices:
                output = f"The latest closing prices for {stock_symbol} over the past 7 days are: {latest_prices}. Use this data for financial recommendations."
            else:
                output = "Failed to fetch the latest stock prices."
        else:
            output = "Stock symbol not found in accountant_task result."

        return output

# Add a function to fetch and save stock data
def main_stock_data():
    stock_data = {}
    for stock in stocks:
        # print(f"Fetching 15-minute interval data for {stock['ticker']}...")
        data = fetch_intraday_data_yahoo(stock["ticker"], interval="15m", period="5d")
        if data:
            stock_data[stock["name"]] = data

    output_filename = "stock_data.json"
    with open(output_filename, "w") as json_file:
        json.dump(stock_data, json_file, indent=2)
    print(f"Data saved to {output_filename}")

# Define route for home page

@app.route('/report', methods=['GET', 'POST'])
def main():
    query_input = None
    output = None
    if request.method == 'POST':
        query_input = request.data
        if query_input:
            try:

                researcher_task = Task(
                    description="Research financial data for " + str(
                        query_input) + " using www.google.com as of "+str(date),
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


@app.route('/managestock', methods=['POST','OPTIONS'])
def burorsell():
    if request.method == "POST":
        print(request.data)
        datainput = json.loads(request.data.decode('utf-8'))

        ticker = datainput.get('ticker')
        amount = datainput.get('amount')
        userid = datainput.get('userId')
        action = datainput.get('action')
        print(ticker,amount,userid,action)

        try:
            docs = (
                    db.collection("shares")
                    .where(filter=FieldFilter("user_id", "==", userid))
                    .stream()
                )

            docs = list(docs)


            shares_owned = 0
            document_id = 0
            if docs:
                for doc in docs:
                    if doc.get('ticker') == ticker:
                        shares_owned = doc.get('shares_owned')
                        document_id = doc.id
            if document_id == 0 and action == "buy":
                db.collection("shares").document().create({"user_id":userid , "ticker": ticker, "shares_owned": amount})
                return jsonify({
                    "status": "Success",
                    "message": "You purchased "+str(amount)+" "+ticker+" stocks"
                }), 200
            else:
                
                if action == 'buy':
                    shares_owned += amount
                    db.collection("shares").document(document_id).set({ "shares_owned": shares_owned,}, merge=True)

                    return jsonify({
                        "status": "Success",
                     "message": "You purchased "+str(amount)+" "+ticker+" stocks.\nNow you own "+str(shares_owned)+" stocks."
                    }), 200
                else:
                    if amount > shares_owned:
                        return jsonify({
                            "status": "Error",
                            "message": "You cannot sell more shares than what you have"
                        }), 200
                    else:
                        shares_owned -= amount
                        if shares_owned > 0 :
                            db.collection("shares").document(document_id).set({ "shares_owned": shares_owned,}, merge=True)
                            return jsonify({
                                "status": "Success",
                                "message": "You sold "+str(amount)+" "+ticker+" stocks.\nNow you own "+str(shares_owned)+" stocks."
                            }), 200
                        else:
                            db.collection("shares").document(document_id).delete()
                            return jsonify({
                                "status": "Success",
                                "message": "You sold all your "+ticker+" stocks."
                            }), 200
        except Exception as e:
            logging.error(f"Error during task execution: {e}")
        return jsonify({
            "status": "Error",
            "message": "Invalid request or unhandled condition."
        }), 400


# this is for testing stuff at home it you dont need to comment stuff out
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

                # researcher_task = Task(
                #     description="Research financial data for " + str(
                #         query_input) + " using yahoo finance news as of " +str(date),
                #     agent=researcher_agent,
                #     expected_output="Latest financial insights for making predictions."
                # )
                researcher_task = Task(
                    description="Research financial data for " + str(
                        query_input) + "on https://google.com/"+str(query_input) +" as of "+str(date),
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

@app.route('/getcompanies', methods=['POST'])
def getcompanies():
    if request.method == 'POST':
        datainput = json.loads(request.data.decode('utf-8'))
        managerID = datainput.get('managerID')
        adminarray = []
        try:
            docs = (
                db.collection("managers").stream()
            )
            docs = list(docs)
            for doc in docs:
                if doc.id == managerID:
                    adminarray = doc.get('adminID')
                    break
            adminsArray = []
            docs = (
                db.collection("admins").stream()
            )
            docs = list(docs)
            for doc in docs:
                for admin in adminarray:
                    if doc.id == admin:
                        adminsArray.append({
                            'adminID':admin,
                            'companyName':doc.get('companyName')
                        })
            return jsonify(adminsArray), 200
        except Exception as e:
            logging.error(f"Error during task execution: {e}")
        return jsonify({
            "status": "Error",
            "message": "Invalid request or unhandled condition."
        }), 400

@app.route('/createuser',methods=['POST'])
def createuser():

    if request.method == "POST":
        datainput = json.loads(request.data.decode('utf-8'))
        userType = datainput.get('userType')
        if userType == "admin":
            try:
                name = datainput.get('name')
                password = datainput.get('password')
                email = datainput.get('email')
                capital = int(datainput.get('funds'))
                companyName = datainput.get('companyName')
                user_record = auth.create_user(
                    email=email,
                    password=password,
                    display_name=name
                )
                user_id = user_record.uid
                user_ref = db.collection('admins').document(user_id)
                user_ref.set({
                    'capital':capital,
                    'companyName':companyName
                })
                return jsonify({
                    "message":"created"
                }), 200
            except Exception as e:
                logging.error(f"Error during task execution: {e}")
        elif userType == "manager":
            try:
                name = datainput.get('name')
                password = datainput.get('password')
                email = datainput.get('email')
                user_record = auth.create_user(
                    email=email,
                    password=password,
                    display_name=name
                )
                user_id = user_record.uid
                emails = datainput.get('adminEmails')
                matching_user_ids = []
                page = auth.list_users()
                while page:
                    for user in page.users:
                        for email in emails:
                            if user.email == email:
                                matching_user_ids.append(user.uid)
                    page = page.get_next_page()
                user_ref = db.collection('managers').document(user_id)
                user_ref.set({
                    'adminID':matching_user_ids
                })
                return jsonify({
                    "message":"created"
                }), 200
            except Exception as e:
                logging.error(f"Error during task execution: {e}")
    return jsonify({
        "message":"Invalid Method"
    }), 400



@app.route('/addadmin',methods=['POST'])

def addadmin():
    if request.method == 'POST':
        datainput = json.loads(request.data.decode('utf-8'))
        managerid = datainput.get('managerID')
        email = datainput.get('email')
        matching_user_ids = []
        page = auth.list_users()
        while page:
            for user in page.users:
                if user.email == email:
                    matching_user_ids.append(user.uid)
            page = page.get_next_page()
        manager = db.collection("manager").document(managerid)
        from google.cloud import firestore
        manager.update({"adminID":firestore.ArrayUnion([matching_user_ids])})
        return jsonify({
            "message":"Updated manager with more admins"
        }), 200



@app.route('/getstocks',methods=['POST'])
def getstocks():
    if request.method == "POST":
        return jsonify(stocks), 200



@app.route('/useradmin',methods=['POST'])
def useradmin():
    if request.method == "POST":
<<<<<<< Updated upstream
        print(request.data)
=======
        print("admin")
>>>>>>> Stashed changes
        datainput = json.loads(request.data.decode('utf-8'))
        userid = datainput.get('uid')
        print(userid)
        docs = (
            db.collection("admins").stream()
        )
        docs = list(docs)
        for doc in docs:
            if doc.id == userid:
                return jsonify({
                    'response':"yes"
                }),200
<<<<<<< Updated upstream
    return jsonify({
        'response':"no"
    }),200
=======
        return jsonify({
            'response':"no"
        }),200

>>>>>>> Stashed changes




@app.route('/usermanager',methods=['POST'])
def usermanager():
    if request.method == "POST":
<<<<<<< Updated upstream
        print(request.data)
        datainput = json.loads(request.data.decode('utf-8'))
        userid = datainput.get('uid')
        docs = (
            db.collection("manager").stream()
=======
        print("manager")
        datainput = json.loads(request.data.decode('utf-8'))
        userid = datainput.get('uid')
        docs = (
            db.collection("managers").stream()
>>>>>>> Stashed changes
        )
        docs = list(docs)
        for doc in docs:
            if doc.id == userid:
                return jsonify({
                    'response':"yes"
                }),200
<<<<<<< Updated upstream
    return jsonify({
        'response':"no"
    }),200
=======
        return jsonify({
            'response':"no"
        }),200

>>>>>>> Stashed changes


@app.route('/userfunds',methods=['POST'])
def getUserFunds():
    if request.method == "POST":
        print(request.data)
        datainput = json.loads(request.data.decode('utf-8'))
        userid = datainput.get('uid')
        docs = (
            db.collection("admins").stream()
        )
        capital = 0
        docs = list(docs)
        for doc in docs:
            if doc.id == userid:
                capital = doc.get('capital')
                return jsonify({
                    'capital':capital
                }),200
        return jsonify({
            'capital':capital
        }),200



#this will be the autopurchase when its done
@app.route('/manage', methods=['POST', 'OPTIONS'])
def autopurchaseregister():
    if request.method == "POST":

        datainput = json.loads(request.data.decode('utf-8'))


        userid = datainput.get('userID')
        company = datainput.get('company')
        ticker = datainput.get('ticker')
        buy_percent = int(float(datainput.get('buy_percent'))*100)
        sell_percent = int(float(datainput.get('sell_percent'))*100)
        funds = int(datainput.get('funds_dollar'))
        shares_owned = 0

        docs = (
            db.collection("admins").stream()
        )

        adminobject = 0
        docs = list(docs)
        for doc in docs:
            if doc.id == userid:
                adminobject = doc
                break
        capital = adminobject.get('capital')
        if capital >= funds:
            capital -= funds

        try:
            db.collection("autopurchase").document().create({"userid":userid , "company":company,"ticker":ticker, "shares_owned": shares_owned,"buy_percent":buy_percent,"sell_percent":sell_percent,'funds_dollar':funds})
            db.collection('admins').document(userid).set({"capital":capital},merge=True)
            return jsonify({
                "status": "Success",
                "message": "Autopurchase set up"
            }), 200
        except Exception as e:
            logging.error(f"Error during task execution: {e}")
    return jsonify({
        "status": "Error",
        "message": "Invalid request or unhandled condition."
    }), 400

def autopurchase():

    while(True):

        # Load the stock data from the JSON file
        # main_stock_data()

        with open('stock_data.json', 'r') as json_file:
            stock_data = json.load(json_file)


        # time.sleep((60*60*2)) for a constant loop put this around the code below
        try:
            docs = (
                db.collection("autopurchase").stream()
            )

            docs = list(docs)

            if docs:
                for doc in docs:
                    # shares_owned = doc.get('shares_owned')

                    # company = doc.get('company')
                    # buy = doc.get('buy_percent')
                    # sell = doc.get('sell_percent')
                    # funds = 0
                    # user_id = doc.get('companyName')
                    # fundsid = 0
                    userid = doc.get('userID')
                    company = doc.get('company')
                    ticker = doc.get('ticker')
                    buy_percent = int(doc.get('buy_percent'))
                    sell_percent = int(doc.get('sell_percent'))
                    funds = int(doc.get('funds_dollar'))
                    shares_owned = 0
                    document_id = doc.id


                    company_stock = stock_data[company]
                    lastitemdate = list(company_stock)[-1]
                    closingorice = company_stock[lastitemdate]['Close']
                    autopurchase_task = Task(
                        description="From the data given here make a prediction as to whether it is a good idea to buy or sell the stock with the ticker of "+ ticker  +" and the previous 7 days data of "+ str(company_stock),
                        agent=autopurchase_agent,
                        expected_output="I expect the output to be given like this as whole numbers, just numbers even if its 0 and nothing more."
                                        "{"
                                        '"Buy"": "x%",'
                                        '"Sell": "z%"'
                                        "}"
                    )
                    crew = Crew(agents=[autopurchase_agent],
                                tasks=[autopurchase_task], verbose=True)
                    result = crew.kickoff()
                    result = str(result)
                    result = result.replace("%", "")
                    result = result.replace("-", "")
                    result = result.replace("+", "")
                    print(result)
                    jsonobject = json.loads(result)
                    agent_buy = int(jsonobject.get('Buy'))
                    agent_sell = int(jsonobject.get('Sell'))
                    #if the buy from agent is greater than the given from user, then go ahead and buy as many stocks as possible until you can buy anymore
                    #then save that into the firebase database

                    if int(agent_buy)>= buy_percent and funds > closingorice:
                        shares_owned  += funds / closingorice
                        funds -= shares_owned*closingorice
                        db.collection("autopurchase").document(document_id).set({ "shares_owned": shares_owned,'funds_dollar':funds}, merge=True)

                        #save share bought , ticker, user id into database so it can be retrieved for future use
                    else:
                        if agent_sell >= sell_percent and shares_owned > 0:
                            #get the share from database and sell them all
                            newfunds = closingorice * shares_owned
                            shares_owned = 0
                            docs = (
                                db.collection("admins").stream()
                            )

                            adminobject = 0
                            docs = list(docs)
                            for doc in docs:
                                if doc.id == userid:
                                    adminobject = doc
                                    break
                            capital = adminobject.get('capital')
                            capital += newfunds
                            db.collection("autopurchase").document(document_id).delete()
                            db.collection("admins").document(userid).set({'capital': capital})


        except Exception as e:
            logging.error(f"Error during task execution: {e}")
        time.sleep(1000)


if __name__ == '__main__':
    # no reason to run it always, we'll make it a app route call but we might not even use it
    # main_stock_data()
    app.run(debug=True)
    # thread = Thread(target = autopurchase,args = {})
    # thread.start()
    # thread.join()

