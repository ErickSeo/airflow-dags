from pathlib import Path
from dagfactory import load_yaml_dags


config_file = Path.cwd() / "dags/repo/airflow/dags/"

load_yaml_dags(
    globals_dict=globals(),
    dags_folder=config_file,
)
