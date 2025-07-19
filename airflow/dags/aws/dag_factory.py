from pathlib import Path
from dagfactory import load_yaml_dags


config_file = Path.cwd() / "dags/repo/airflow/dags/aws/"

load_yaml_dags(
    globals_dict=globals(),
    config_file=config_file,
)
