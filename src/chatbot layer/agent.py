%pip install langchain langchain-google-genai google-generativeai databricks-sql-connector python-dotenv
%restart_python

import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

# Load environment variables
load_dotenv("/Workspace/Repos/ziaarzoo21@gmail.com/spark-etl/connection.env")

api_key = os.getenv("GOOGLE_API_KEY")
catalog = os.getenv("CATALOG_NAME")
schema = os.getenv("SCHEMA_NAME")
table = os.getenv("TABLE_NAME")

# Configure Gemini
genai.configure(api_key=api_key)

# Initialize LangChain LLM wrapper
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

# Connect to Databricks SQL
db_uri = (
    f"databricks://token:{os.getenv('DATABRICKS_TOKEN')}@"
    f"{os.getenv('DATABRICKS_SERVER_HOSTNAME')}"
    f"{os.getenv('DATABRICKS_HTTP_PATH')}"
)
db = SQLDatabase.from_uri(db_uri)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Create LangChain SQL agent
agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

def query_agent(question: str):
    context = f"You are querying Databricks Unity Catalog table {catalog}.{schema}.{table}. Respond using its data."
    return agent.run(f"{context}\nUser question: {question}")
