import os

from sqlalchemy import create_engine
from typing import Dict, Union
from ..logger_config import logger


class BaseETL:
    """
    Base class for ETL operations. Subclasses should implement the transform method.
    """
    _tables: Dict = []
    _table_info: Dict = {}

    def __init__(
            self,
            db_path: os.PathLike,
    ):
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found at {db_path}")
        if not str(db_path).endswith('.db'):
            raise ValueError("Database file must be a SQLite database.")

        self.engine = create_engine(f'sqlite:///{db_path}', echo=True)

    @property
    def tables(self) -> Dict:
        return self._tables

    @tables.setter
    def tables(self, value: Dict) -> None:
        self._tables = value

    @property
    def table_info(self) -> Dict:
        return self._table_info

    @table_info.setter
    def table_info(self, value: Dict) -> None:
        self._table_info = value

    def extract(self, raw_data_path: Union[os.PathLike, str]) -> None:
        """ Extracts data from SQLite and returns a list of dataframes (to be implemented in subclass) """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def transform(self) -> None:
        """ Transform data as needed (to be implemented in subclass) """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def load(self) -> None:
        """ Load data into a new database. """
        if self.tables is None:
            raise ValueError("No data to load. Run the extract method first.")

        for name, df in self.tables.items():
            df.to_sql(name, con=self.engine, if_exists='replace', index=False)
            logger.info(f"Table {name} loaded successfully.")
