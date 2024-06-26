## KG PoC for the Case Study: AI Platform engineer

This package provides an ETL data pipeline that ingests EB datasets into a Relational and Graph database.
The following datasets are ingested:
- NAEB (Natural Products Activity and Species Source Database): Focuses on the biological activities of natural products and their species sources.
- NPASS (Natural Product Activity and Species Source Database): Contains data on natural product molecules including their biological activities and source organisms.
- ChEMBL: A large-scale bioactivity database for drug discovery, containing chemical, bioactivity, and genomic data.

## Infrastructure

The ETL pipeline is built using the Weasel framework, which is a lightweight framework that allows you to build pipelines using Python.
The overall schema of the pipeline looks as follows:

![image](images/kg_etl.png)

The ETL pipeline can either load data into a DB Store, or a Triple Store like Apache Jena Fuseki. The pipeline is built in a way that it can be easily extended to support other databases.

## 🔧 Quick Install
- Steps for usage:

1. Clone the repository.
```bash
  git clone git@github.com:aymanehachcham/kg-PoC.git
```

2. Download the resources like the NAEB, NPASS datasets
3. Download the Chembl dataset from the [ChEMBL website](https://www.ebi.ac.uk/chembl/).

4. Install poetry in your system. For more information, visit the [Poetry documentation](https://python-poetry.org/docs/).

```bash
  curl -sSL https://install.python-poetry.org | python3 -
```

5. Install the dependencies using poetry.
```bash
  poetry install
```

6. Use weasel to run the ETL pipeline.
```bash
  weasel run all
```

## Usage

- You also have a playground with juypter notebooks to explore the integrity of the database in the main.ipynb file.
- The ``èntry.py`` file contains an entry point to test the ``NaturalLanguageQueryEngine`` that can query the SQL database with natural language queries.
