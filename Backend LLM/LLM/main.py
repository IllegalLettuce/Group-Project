import os
import config
from crewai import Agent, Task, Crew, LLM
# from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

# for groq
from langchain_groq import ChatGroq
from groq import Groq

# accountant

# Environment configurations
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3-70b-8192"
os.environ["GROQ_API_KEY"] = config.groqapiekey
os.environ["OPENAI_API_KEY"] = config.chatopenaiapikey

# llm1 = ChatOpenAI(
#     model="llama3.2:3b",
#     base_url="http://localhost:11434"
# )
ollama3 = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

Gllm = ChatGroq(
    model_name="groq/llama3-70b-8192",
    temperature=0.3,
    max_tokens=4096
)

researcher_agent = Agent(
    role="Company Researcher",
    goal="To research the given company or crypto coin, and give financial information about the company or crypto coin, from which predictions could be made",
    backstory="You love to give accurate information about how a company is doing from company stocks, always keeping up with the news about how each company is doing",
    # llm=ollama3
)

accountant_agent = Agent(
    role="Accountant Agent",
    goal="Perform general accounting tasks including transaction processing, financial verification, and report generation.",
    backstory="You are an professional accountant responsible for Financial report generation, budget analysis, tax preparation",
    llm=Gllm
)

blogger_agent = Agent(
    role="Blogger Agent",
    goal="Use the given company financial data and give accurate information about how the company is doing currently and make a prediction on how it would become stronger or weaker in the economy",
    backstory="You love writing short blogs which readers love to read",
    llm=ollama3
)

# to be used later
# recommender_agent = Agent(
#     role="Blogger Agent",
#     goal="Use the given company financial data and give accurate information about how the company is doing currently and make a prediction on how it would become stronger or weaker in the economy",
#     backstory="You love writing short blogs which readers love to read",
#     llm=ollama3
# )


researcher_task = Task(
    description="Research doge coin using google",
    expected_output="Latest financial information from which predictions can be made and a date on this information so it is known how up to date it is",
    agent=researcher_agent
)

accountant_task = Task(
    description="Calculate accounting ratios",
    agent=accountant_agent,  # Assign the agent to the task
    details="Create a summary of recent financial transactions for the month.",
    expected_output="This ratio suggests that the company has $0.80 in debt for every dollar of equity, reflecting a moderate level of financial leverage.",
    priority="medium"
)

blogger_task = Task(
    description=f"{researcher_task}",
    expected_output="A short summary of how the company is doing now and how it is expected to perform in the comming year",
    agent=blogger_agent
)

crew = Crew(
    agents=[researcher_agent, accountant_agent, blogger_agent],
    tasks=[researcher_task, accountant_task, blogger_task],
    verbose=True
)

results = crew.kickoff()

print("###################")
print(results)
