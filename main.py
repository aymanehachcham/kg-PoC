from sqlalchemy import create_engine
import sqlite3
import pandas as pd
from kg_poc.etl.chembl import ChemblETL
from pathlib import Path

if __name__ == '__main__':
    etl_chembl = ChemblETL(
        db_path=Path('datasets/test_data_model.db')
    )
    etl_chembl.extract(raw_data_path='chembl_34.db')
    etl_chembl.transform()
    etl_chembl.load()
