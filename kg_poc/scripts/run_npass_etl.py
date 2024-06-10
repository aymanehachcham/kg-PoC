from kg_poc.etl.npass import NPASSETL
import typer
from pathlib import Path


def main(
    db_store_path: Path = typer.Argument(..., dir_okay=False),
    raw_data_path: Path = typer.Argument(..., exists=True, dir_okay=True),
):
    npass_etl = NPASSETL(
        db_path=db_store_path
    )
    npass_etl.extract(raw_data_path=raw_data_path)
    npass_etl.transform()
    npass_etl.load()


if __name__ == "__main__":
    typer.run(main)