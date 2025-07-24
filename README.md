## 🧩 Function: get_environment_context

> [!NOTE] 
>  **Descrição**:
>  Retorna informações de ambiente necessárias para identificar o contexto de execução no Composer/Airflow. 
>  Usada em pipelines, logging ou configuração dinâmica baseada no ambiente atual.

#### 💻 Code

```python
import os

def get_environment_context() -> dict:
    return {
        "google_cloud_project": os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "airflow_env": os.environ.get("AIRFLOW_ENV"),
        "composer_environment": os.environ.get("COMPOSER_ENVIRONMENT"),
    }
```

#### 📥 Input

| Nome | Tipo | Padrão | Descrição                      |
| ---- | ---- | ------ | ------------------------------ |
| —    | —    | —      | A função não recebe parâmetros |
#### 📤Output

**Type**: `dict`

**Description**:

	Dicionário com as variáveis de ambiente extraídas do sistema. 
	Contém as chaves:
	- `"google_cloud_project"`
	- `"airflow_env"`
	- `"composer_environment"`



