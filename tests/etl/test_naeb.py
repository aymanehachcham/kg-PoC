import unittest
from unittest.mock import patch, MagicMock
from kg_poc.etl.naeb import NAEBETL


class TestNAEBETL(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures, if any."""
        self.db_path = "test_database.db"
        self.etl = NAEBETL(db_path=self.db_path)

    def test_initialization_creates_db_if_not_exist(self):
        """Test if the database is created if not already present."""
        with patch('os.path.exists', return_value=False), \
             patch('builtins.open', unittest.mock.mock_open()) as mocked_file:
            etl = NAEBETL(db_path=self.db_path)
            mocked_file.assert_called_once_with(self.db_path, 'a')

    def test_initialization_raises_error_for_invalid_db_extension(self):
        """Test if initialization raises an error for non-db file extensions."""
        with self.assertRaises(ValueError):
            NAEBETL(db_path="invalidfile.txt")

    def test_extract_raises_error_if_not_directory(self):
        """Test that the correct error is raised if the path is not a directory."""
        with self.assertRaises(ValueError):
            self.etl.extract("not_a_directory_path")

    @patch('os.walk')
    @patch('os.path.isdir', return_value=True)
    def test_extract_process_files(self, mock_isdir, mock_os_walk):
        """Test that CSV files are processed correctly in the extract method."""
        mock_os_walk.return_value = [
            ("root", ("dirs"), ["file1.csv", "file2.csv"])
        ]
        with patch('tqdm') as mock_tqdm:
            self.etl.extract("some_directory")
            self.assertIn('file1', self.etl.table_info)
            self.assertIn('file2', self.etl.table_info)
            self.assertEqual(mock_tqdm.call_count, 1)

    @patch('pandas.read_csv')
    def test_transform(self, mock_read_csv):
        """Test transformation logic to ensure it processes dataframes correctly."""
        mock_df = MagicMock()
        mock_read_csv.return_value = mock_df
        mock_df.merge.return_value = mock_df
        mock_df.drop.return_value = mock_df
        mock_df.rename.return_value = mock_df

        self.etl.table_info = {
            'uses': 'uses.csv',
            'use_subcategories': 'use_subcategories.csv',
            'species': 'species.csv',
            'sources': 'sources.csv'
        }
        self.etl.transform()
        self.assertTrue('usage' in self.etl.tables)

    @patch('pandas.DataFrame.to_sql')
    def test_load(self, mock_to_sql):
        """Test if data is loaded into the database correctly."""
        self.etl.tables = {
            'usage': MagicMock(),
            'species': MagicMock(),
            'sources': MagicMock()
        }
        self.etl.load()
        self.assertEqual(mock_to_sql.call_count, 3)


if __name__ == '__main__':
    unittest.main()
