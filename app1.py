import streamlit as st
from sqlalchemy.engine import URL
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.sql import SQLTools

# -----------------------
# Azure SQL Connection
# -----------------------
server = "sqlpjt.database.windows.net"
database = "sqldb"
username = "azureadmin"
password = "Shiba@3048"

# ✅ Build SQLAlchemy-style connection string
connection_url = URL.create(
    "mssql+pyodbc",
    username=username,
    password=password,
    host=server,
    port=1433,
    database=database,
    query={"driver": "ODBC Driver 18 for SQL Server"}   # or "ODBC Driver 17 for SQL Server"
)

# -----------------------
# Initialize SQLTools
# -----------------------
try:
    sql_tool = SQLTools(url=str(connection_url))   # ✅ Pass URL string, not engine
    st.success("✅ Connected to Azure SQL Database")
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    st.stop()

# -----------------------
# Create Agent
# -----------------------
agent = Agent(
    model=Ollama(id="llama3.2:3b"),   # use a model installed in Ollama
    tools=[sql_tool],
    instructions="You are an AI that queries Azure SQL and explains results clearly.",
    show_tool_calls=True,
)

# -----------------------
# Streamlit UI
# -----------------------
st.title("🤖 AI Agent with Ollama + Azure SQL")

question = st.text_input("Enter your question (e.g., 'What is total sales?')")

if st.button("Ask AI") and question.strip():
    with st.spinner("Thinking... querying Azure SQL..."):
        try:
            response = agent.run(question)
            st.write("### ✅ Answer")
            st.write(response)
        except Exception as e:
            st.error(f"❌ Error: {e}")

