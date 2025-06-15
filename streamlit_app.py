import streamlit as st
import os
from dotenv import load_dotenv

# LangChain imports
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import create_sql_agent

# --- Configuration & Setup ---
DB_FILE_PATH = 'flights.db'

# Function to load the AI agent
# We use st.cache_resource to load this only once and save resources
@st.cache_resource
def get_sql_agent():
    """
    Initializes and returns the LangChain SQL Agent.
    Caches the agent for performance so it doesn't reload on every interaction.
    """
    # Load the Google API Key from the .env file
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("Google API Key not found. Please add it to your .env file.")
        st.stop()
        
    if not os.path.exists(DB_FILE_PATH):
        st.error(f"Database file '{DB_FILE_PATH}' not found. Please run prepare_database.py first.")
        st.stop()

    # Connect to the database
    db = SQLDatabase.from_uri(f"sqlite:///{DB_FILE_PATH}")
    
    # Initialize the Google Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=api_key)
    
    # Create and return the SQL agent
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    
    return agent_executor

# --- Streamlit App UI ---
st.set_page_config(page_title="Talk to Your Flight Data", page_icon="✈️", layout="wide")

st.title("✈️ Talk to Your Flight Data")
st.write("Ask questions in plain English about your flight database, and the AI will find the answers for you.")

# Initialize or get the agent from cache
try:
    agent_executor = get_sql_agent()

    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input from the chat input box
    if prompt := st.chat_input("Ask a question, e.g., 'What is the average price to Delhi?'"):
        # Add user's question to chat history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process the question with the AI agent
        with st.chat_message("assistant"):
            # Use a spinner to show that the AI is "thinking"
            with st.spinner("Analyzing your question and querying the database..."):
                try:
                    response = agent_executor.invoke({"input": prompt})
                    answer = response['output']
                    st.markdown(answer)
                    # Add AI's answer to chat history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    error_message = f"An error occurred: {e}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

except Exception as e:
    st.error(f"Failed to initialize the application. Please check your setup. Error: {e}")

