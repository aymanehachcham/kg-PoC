import sqlite3
from langchain import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class NaturalLanguageQueryEngine:
    def __init__(self, database_path, llm=None):
        self.db = sqlite3.connect(database_path)
        self.cursor = self.db.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        # Create the database object for LangChain
        self.db_lang = SQLDatabase.from_uri(f"sqlite:///{database_path}")

        # Create the SQL Agent
        if llm is None:
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
        self.agent_executor = create_sql_agent(llm, db=self.db_lang, agent_type="openai-tools", verbose=True)

    def execute_query(self, natural_language_query):
        try:
            result = self.agent_executor.invoke(natural_language_query)
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def close(self):
        self.db.close()
