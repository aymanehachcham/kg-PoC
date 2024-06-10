from kg_poc.etl.chembl import ChemblETL
import typer
from pathlib import Path


def main(
    db_store_path: Path = typer.Argument(..., dir_okay=False),
    raw_data_path: Path = typer.Argument(..., dir_okay=False),
):
    naeb_etl = ChemblETL(
        db_path=db_store_path
    )
    naeb_etl.extract(raw_data_path=raw_data_path)
    naeb_etl.transform()
    naeb_etl.load()


if __name__ == "__main__":
    typer.run(main)