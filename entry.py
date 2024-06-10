
from kg_poc.llm_engine import NaturalLanguageQueryEngine

if __name__ == '__main__':
    query_engine = NaturalLanguageQueryEngine(database_path='kg_poc/datasets/eb_data.db')
    result = query_engine.execute_query("List all species name with usage name Analgesic.")

    # Print the result
    print(result)

    # Close the database connection
    query_engine.close()

