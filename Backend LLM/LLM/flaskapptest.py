import os
import config
from flask import Flask, request, render_template
import logging
import re

# Import required modules from langchain_community, crewai, etc.
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from crewai import Agent, Task, Crew, LLM
from langchain_groq import ChatGroq
from groq import Groq

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
# ollama3 = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
ollama3 = LLM(model="ollama/llama3.2", base_url="https://d482-213-233-155-177.ngrok-free.app")
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

blogger_agent = Agent(
    role="Blogger Agent",
    goal="Provide summaries and predictions on company performance.",
    backstory="Writes short, informative blogs.",
    llm=ollama3
)





accountant_task = Task(
    description="Calculate accounting ratios for the company",
    agent=accountant_agent,
    expected_output="A summary of financial leverage, such as debt-to-equity ratio."
)

blogger_task = Task(
    description="Summarize financial data and make predictions",
    agent=blogger_agent,
    expected_output="A short blog summary on company performance and outlook."
)



# Define route for home page
@app.route('/', methods=['GET', 'POST'])
def main():
    query_input = None
    output = None
    if request.method == 'POST':
        query_input = request.form.get('query-input')
        if query_input:
            try:
                researcher_task = Task(
                    description="Research financial data for " + query_input,
                    agent=researcher_agent,
                    expected_output="Latest financial insights for making predictions."
                )
                crew = Crew(agents=[researcher_agent, accountant_agent, blogger_agent], tasks=[researcher_task, accountant_task, blogger_task], verbose=True)
                result = crew.kickoff()
                result = str(result)

                output = format_output(result)

            except Exception as e:
                logging.error(f"Error during task execution: {e}")
                output = "Sorry, an error occurred while processing your request."
    return render_template('index.html', query_input=query_input, output=output)

if __name__ == '__main__':
    app.run(debug=True)
