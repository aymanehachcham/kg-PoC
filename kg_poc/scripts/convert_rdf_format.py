
import typer
from pathlib import Path
import pandas as pd
import sqlite3
from rdflib import Graph, Namespace, Literal
from kg_poc.logger_config import logger
from tqdm import tqdm


def convert_to_rdf(
        table_name: str,
        conn: sqlite3.Connection,
        graph: Graph,
        namespace: Namespace
) -> None:
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 10000", conn)
    for index, row in df.iterrows():
        # Assuming the first column is the primary key
        tp_subject = namespace[str(row.iloc[0])]
        for col in df.columns[1:]:
            tp_predicate = namespace[col]
            tp_object = Literal(row[col])
            graph.add((tp_subject, tp_predicate, tp_object))


def main(
        db_store_path: Path = typer.Argument(..., dir_okay=False),
        namespace: str = typer.Argument(...),
        destination_path: Path = typer.Argument(..., dir_okay=False)
):
    conn = sqlite3.connect(db_store_path)
    g = Graph()
    n = Namespace(namespace)

    tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
    tables = pd.read_sql_query(tables_query, conn).to_dict()

    for table_name in tqdm([v for k, v in tables.get('name').items()], desc="Converting tables to RDF"):
        logger.info(f"Converting table {table_name} to RDF")
        convert_to_rdf(table_name, conn, g, n)

    # Serialize the graph to an RDF file
    g.serialize(destination=destination_path, format='xml')


if __name__ == "__main__":
    typer.run(main)
