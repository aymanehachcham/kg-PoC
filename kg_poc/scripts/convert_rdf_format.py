
import typer
from pathlib import Path
from kg_poc.etl.rdf_converter import SQLiteToRDFConverter


def main(
        db_store_path: Path = typer.Argument(..., dir_okay=False),
        namespace: str = typer.Argument(...),
        destination_path: Path = typer.Argument(..., dir_okay=False)
):
    converter = SQLiteToRDFConverter(db_store_path, namespace, destination_path)
    converter.run()


if __name__ == "__main__":
    typer.run(main)
