from pathlib import Path
import pandas as pd
import sqlite3
from rdflib import Graph, Namespace, Literal
from kg_poc.logger_config import logger
from tqdm import tqdm


class SQLiteToRDFConverter:
    def __init__(self, db_store_path: Path, namespace: str, destination_path: Path):
        self.db_store_path = db_store_path
        self.namespace = namespace
        self.destination_path = destination_path
        self.conn = sqlite3.connect(db_store_path)
        self.graph = Graph()
        self.namespace_obj = Namespace(namespace)

    def convert_to_rdf(self, table_name: str) -> None:
        df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 10000", self.conn)
        for index, row in df.iterrows():
            # Assuming the first column is the primary key
            tp_subject = self.namespace_obj[str(row.iloc[0])]
            for col in df.columns[1:]:
                tp_predicate = self.namespace_obj[col]
                tp_object = Literal(row[col])
                self.graph.add((tp_subject, tp_predicate, tp_object))

    def convert_tables_to_rdf(self):
        tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables = pd.read_sql_query(tables_query, self.conn).to_dict()

        for table_name in tqdm([v for k, v in tables.get('name').items()], desc="Converting tables to RDF"):
            logger.info(f"Converting table {table_name} to RDF")
            self.convert_to_rdf(table_name)

    def serialize_graph(self):
        self.graph.serialize(destination=self.destination_path, format='xml')

    def run(self):
        self.convert_tables_to_rdf()
        self.serialize_graph()
