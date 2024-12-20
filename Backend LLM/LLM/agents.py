# agents.py
import os
from crewai import Agent, LLM
from langchain_groq import ChatGroq
from pydantic.v1 import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
import config

# Configure environment variables
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3-70b-8192"
os.environ["GROQ_API_KEY"] = config.groqapiekey
os.environ["GOOGLE_API_KEY"] = config.googleapikey
os.environ["GEMINI_API_KEY"] = config.googleapikey
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["OPENAI_API_KEY"] = config.chatopenaiapikey

# Initialize LLMs
ollama3 = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
Gllm = ChatGroq(
    temperature=0.3,
    max_tokens=4096,
    model_name="llama3-70b-8192"
)
gemini = ChatGoogleGenerativeAI(model="gemini/gemini-1.5-flash", temperature=0.5)
gem = LLM(model="gemini/gemini-1.5-flash", temperature=0.5)

# Define agents
researcher_agent = Agent(
    role="Company Researcher",
    goal="To research the given company or crypto coin and provide financial insights.",
    backstory="In-depth knowledge of stocks and company financials.",
    llm=gem
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