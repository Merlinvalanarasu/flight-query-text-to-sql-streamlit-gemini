# **Natural Language Flight Query Engine**

A user-friendly web application that allows you to have a conversation with your flight data. Ask questions in plain English and get instant answers, powered by Google's Gemini AI model and LangChain.

## **🔴 Project Status**

This application is fully functional and can be run on a local machine by following the instructions below. A live web deployment is not yet available.

## **📸 Screenshot**

A screenshot of the application running locally.  
(You can replace the placeholder link below with the screenshot you upload to your GitHub repository)

## **✨ Features**

* **Natural Language Queries:** Ask complex questions like *"What is the average price for a flight from Delhi to Mumbai?"* without writing any SQL code.  
* **AI-Powered:** Utilizes Google's powerful gemini-1.5-flash model for accurate SQL generation.  
* **Relational Database Backend:** Demonstrates data normalization by structuring a single CSV file into a relational SQLite database with multiple tables (flights, airlines, routes).  
* **Interactive Chat Interface:** A clean and intuitive UI built with Streamlit that maintains conversation history.  
* **Agent-Based Logic:** Built with LangChain's SQL Agent, which can intelligently inspect the database schema, write queries, execute them, and interpret the results.

## **🛠️ Tech Stack**

* **Backend:** Python  
* **AI Framework:** LangChain  
* **LLM:** Google Gemini (gemini-1.5-flash)  
* **Web Framework:** Streamlit  
* **Data Manipulation:** Pandas  
* **Database:** SQLite

## **🏗️ Project Architecture**

This project follows a simple yet powerful architecture:

1. **Data Preparation (prepare\_database.py):** A Python script reads the raw goibibo\_flights\_data.csv, normalizes the data, and creates a structured flights.db SQLite database.  
2. **Backend (streamlit\_app.py):**  
   * A Streamlit application provides the user interface.  
   * It connects to the flights.db database.  
   * It uses the LangChain SQL Agent, configured with the Google Gemini LLM.  
3. **Execution Flow:**  
   * The user enters a question in the Streamlit app.  
   * The LangChain agent receives the question and the database schema.  
   * The Gemini model generates the appropriate SQL query.  
   * The agent executes the query on the flights.db database.  
   * The final answer is returned and displayed in the chat interface.

## **🚀 How to Run This Project Locally**

Follow these steps to set up and run the project on your local machine.

#### **1\. Clone the Repository**

git clone https://github.com/your-username/flight-query-streamlit-gemini.git  
cd flight-query-streamlit-gemini

*Replace your-username and the repository name with your actual GitHub details.*

#### **2\. Create a Virtual Environment**

It's highly recommended to use a virtual environment to keep dependencies isolated.

\# For Windows  
python \-m venv venv  
venv\\Scripts\\activate

\# For macOS/Linux  
python3 \-m venv venv  
source venv/bin/activate

#### **3\. Install Dependencies**

Install all the required Python libraries from the requirements.txt file.

pip install \-r requirements.txt

#### **4\. Set Up Your API Key**

* Create a file named .env in the root of your project folder.  
* Get your free API key from [Google AI Studio](https://aistudio.google.com/).  
* Add your key to the .env file like this:

GOOGLE\_API\_KEY="your\_google\_api\_key\_here"

#### **5\. Prepare the Database**

Run the preparation script to create the flights.db file from the CSV data.

python prepare\_database.py

#### **6\. Launch the Streamlit App**

You are now ready to run the application\!

streamlit run streamlit\_app.py

A new tab will open in your browser at http://localhost:8501.

## **🙏 Acknowledgements**

* The flight dataset used in this project is the **Goibibo Flights Dataset**, available on [Kaggle](https://www.kaggle.com/datasets/iamavyukt/goibibo-flight-data).  
* This project was built using the incredible open-source tools provided by [Streamlit](https://streamlit.io/) and [LangChain](https://www.langchain.com/).
