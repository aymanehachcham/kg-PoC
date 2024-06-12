
from kg_poc.llm_engine import NaturalLanguageQueryEngine
import sqlite3

if __name__ == '__main__':
    query_engine = NaturalLanguageQueryEngine(database_path='kg_poc/datasets/eb_data.db')
    result = query_engine.execute_query(
        """
        List the species names associated with the usage Analgesic.
        """
    )

    # Print the result
    print(result)

    # Close the database connection
    query_engine.close()

