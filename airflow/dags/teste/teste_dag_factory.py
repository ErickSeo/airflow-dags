import os
from pathlib import Path

# The following import is here so Airflow parses this file
# from airflow import DAG

import dagfactory


config_file = Path.cwd() / "dags/repo/airflow/dags/teste/config.yaml"

example_dag_factory = dagfactory.DagFactory(config_file)

# Creating task dependencies
example_dag_factory.clean_dags(globals())
example_dag_factory.generate_dags(globals())
