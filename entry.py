
from kg_poc.llm_engine import NaturalLanguageQueryEngine

if __name__ == '__main__':
    query_engine = NaturalLanguageQueryEngine(database_path='kg_poc/datasets/eb_data.db')
    result = query_engine.execute_query(
        """
        List the species names associated with the usage Analgesic.
        Once you list them, find the targets associated to these species names, by joining the species name to natural_product table
        through the np_id and then looking up the np_id in the target table. 
        """
    )

    # Print the result
    print(result)

    # Close the database connection
    query_engine.close()

