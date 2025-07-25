
> [!NOTE] 
> A Dag tem como objetivo extrair metadados e logs do Airflow.
> Essa DAG é voltada para controle, auditoria e análise da execução de pipelines no Airflow, e está categorizada com as tags `data-gov`, `airflow` e `dag`.

⏰ Schedule:  
<div style="margin-left: 2em;">Executada diariamente à meia-noite UTC (`0 0 * * *`)</div>

---

# 💻 Tasks:

## ▶️ list_airflow_dags


> [!NOTE] 
> Extrai todas as DAGs registradas no ambiente atual do Composer e exporta os metadados para arquivos `.yaml`, um para cada ambiente (develop, homolog, prod).
> Os arquivos são enviados para buckets GCS específicos de cada ambiente.

---
### 📁 GCS Location - Yaml Output
**filename_pattern**:  `/composer/dag/<gcp_project_id>-<composer_name>-<environment>.yaml`    
**Exemplo**:  
- composer: airflow-dataeng-210
- projeto: allos-eng-dados-nonprd
- environment: homolog

O Yaml vai ser salvo no path:  
<div style="margin-left: 2em;">/composer/dag/allos-eng-dados-nonprd-airflow-dataeng-210-homolog.yaml</div>

---
### 📄 Yaml Output

```yaml
- _dag_display_property_value: ''
  airflow_env: homolog
  composer_environment: airflow-dataeng-210
  dag_id: motor_missao__admin_mission
  dataset_expression: ''
  default_view: grid
  description: ''
  fileloc: /home/airflow/gcs/dags/dags/motor_missao__admin_mission.py
  google_cloud_project: allos-eng-dados-nonprd
  has_import_errors: false
  has_task_concurrency_limits: false
  is_active: true
  is_paused: false
  is_subdag: false
  last_expired: ''
  last_parsed_time: '2025-07-21T23:59:56.952646+00:00'
  last_pickled: ''
  max_active_runs: 25
  max_active_tasks: 100
  max_consecutive_failed_dag_runs: 0
  next_dagrun: '2025-07-21T07:00:00+00:00'
  next_dagrun_create_after: '2025-07-22T07:00:00+00:00'
  next_dagrun_data_interval_end: '2025-07-22T07:00:00+00:00'
  next_dagrun_data_interval_start: '2025-07-21T07:00:00+00:00'
  owners: airflow
  pickle_id: ''
  processor_subdir: /home/airflow/gcs/dags
  root_dag_id: ''
  schedule_interval: 0 7 * * *
  scheduler_lock: ''
  timetable_description: At 07:00
```

---

### 📦 Estrutura de metadados do DAG (`DagModel` serializado)

| 🔑 Campo                          | 📝 Tipo       | 💬 Descrição                                                     |
| --------------------------------- | ------------- | ---------------------------------------------------------------- |
| `_dag_display_property_value`     | `str`         | Valor de exibição customizado (normalmente vazio)                |
| `airflow_env`                     | `str`         | Nome do ambiente do Airflow (`develop`, `homolog`, `prod`, etc.) |
| `composer_environment`            | `str`         | Nome da instância do Cloud Composer                              |
| `dag_id`                          | `str`         | Identificador único do DAG                                       |
| `dataset_expression`              | `str`         | Expressão associada a datasets (se usado)                        |
| `default_view`                    | `str`         | Visualização padrão no UI (`graph`, `tree`, `grid`, etc.)        |
| `description`                     | `str`         | Descrição textual do DAG (se definida)                           |
| `fileloc`                         | `str`         | Caminho absoluto do arquivo `.py` que define o DAG               |
| `google_cloud_project`            | `str`         | ID do projeto GCP                                                |
| `has_import_errors`               | `bool`        | Indica se o DAG teve erro ao ser importado                       |
| `has_task_concurrency_limits`     | `bool`        | Indica se tarefas possuem limites de concorrência                |
| `is_active`                       | `bool`        | Se o DAG está ativo (pode ser executado)                         |
| `is_paused`                       | `bool`        | Se o DAG está pausado (não será executado automaticamente)       |
| `is_subdag`                       | `bool`        | Indica se o DAG é um subDAG                                      |
| `last_expired`                    | `str` ou `''` | Última data de expiração registrada                              |
| `last_parsed_time`                | `datetime`    | Data/hora da última análise/snapshot do DAG                      |
| `last_pickled`                    | `str`         | Data/hora de serialização do DAG (usado com pickling)            |
| `max_active_runs`                 | `int`         | Número máximo de execuções simultâneas do DAG                    |
| `max_active_tasks`                | `int`         | Número máximo de tarefas ativas simultaneamente                  |
| `max_consecutive_failed_dag_runs` | `int`         | Máximo de falhas consecutivas permitidas em execuções            |
| `next_dagrun`                     | `datetime`    | Próxima data agendada para execução do DAG                       |
| `next_dagrun_create_after`        | `datetime`    | Quando a próxima DAGRun poderá ser criada                        |
| `next_dagrun_data_interval_start` | `datetime`    | Início do intervalo de dados da próxima DAGRun                   |
| `next_dagrun_data_interval_end`   | `datetime`    | Fim do intervalo de dados da próxima DAGRun                      |
| `owners`                          | `str`         | Responsável(s) pelo DAG (geralmente `airflow`, `team`, etc.)     |
| `pickle_id`                       | `str`         | ID de serialização (se for pickled)                              |
| `processor_subdir`                | `str`         | Diretório base onde os DAGs estão sendo processados              |
| `root_dag_id`                     | `str`         | Se for um subdag, aponta para o DAG raiz                         |
| `schedule_interval`               | `str`         | Expressão cron ou intervalo do agendamento                       |
| `scheduler_lock`                  | `str`         | Lock interno do scheduler (normalmente vazio)                    |
| `timetable_description`           | `str`         | Descrição amigável do schedule (ex: "At 07:00")                  |

## ▶️ list_airflow_tasks
>[!NOTE]  
Extrai as **tasks** de todos os DAGs registrados no ambiente atual do Cloud Composer, serializa seus metadados como `.yaml` e envia o resultado para buckets do GCS específicos de cada ambiente (`develop`, `homolog`, `prod`).

---

### 📁 GCS Location - Yaml Output
**filename_pattern**:  
`/composer/task/<gcp_project_id>-<composer_name>-<environment>.yaml`

**Exemplo**:
- composer: airflow-dataeng-210
- projeto: allos-eng-dados-nonprd
- environment: homolog

O arquivo será salvo no caminho:  
<div style="margin-left: 2em;">/composer/task/allos-eng-dados-nonprd-airflow-dataeng-210-homolog.yaml</div>

---
### 🛠️ Funções principais
#### 🔹 `_fetch_task_metadata(context)`
- Itera por todos os DAGs carregados no `DagBag`    
- Para cada DAG, coleta os metadados de todas as tasks    
- Anexa os dados do contexto do ambiente (projeto, Composer, etc.)    
- Retorna uma lista de dicionários (um por task)    

#### 🔹 `list_all_tasks()`

- Obtém o contexto do ambiente com `get_environment_context()`    
- Chama `_fetch_task_metadata()`    
- Serializa os metadados em YAML    
- Para cada `env` em `TARGET_ENVIRONMENTS`, envia o YAML para o bucket GCS correspondente via `GCSHook`

---

### 📄 Exemplo de saída (`task.yaml`)

```yaml
- dag_id: motor_missao__admin_mission
  task_id: salvar_resultado
  task_type: PythonOperator
  owner: airflow
  retries: 2
  retry_delay: '0:05:00'
  queue: default
  pool: default_pool
  upstream_task_ids: []
  downstream_task_ids: [validar_entrada]
  trigger_rule: all_success
  google_cloud_project: allos-eng-dados-nonprd
  composer_environment: airflow-dataeng-210
  airflow_env: homolog
```

---

### 📦 Estrutura de metadados da task

|🔑 Campo|📝 Tipo|💬 Descrição|
|---|---|---|
|`dag_id`|`str`|Identificador do DAG ao qual a task pertence|
|`task_id`|`str`|Nome único da task|
|`task_type`|`str`|Tipo do operador (ex: `PythonOperator`, `BashOperator`, etc.)|
|`owner`|`str`|Responsável pela task (default `airflow`)|
|`retries`|`int`|Número de tentativas em caso de falha|
|`retry_delay`|`str`|Tempo entre tentativas, serializado como string|
|`queue`|`str`|Fila onde a task será executada|
|`pool`|`str`|Pool de execução associado à task|
|`upstream_task_ids`|`list[str]`|Lista de `task_id` que devem ser executadas antes desta|
|`downstream_task_ids`|`list[str]`|Lista de `task_id` que dependem desta para executar|
|`trigger_rule`|`str`|Regra de disparo da task (`all_success`, `all_failed`, etc.)|
|`google_cloud_project`|`str`|ID do projeto GCP|
|`composer_environment`|`str`|Nome da instância do Composer|
|`airflow_env`|`str`|Nome do ambiente lógico (`develop`, `homolog`, `prod`, etc.)|

## ▶️ generate_airflow_report

>[!INFO]  
Esse script percorre todas as **execuções de DAGs com falha** no intervalo do último dia (de meia-noite a meia-noite UTC), extrai os **logs de erro** para cada tentativa (`try_number`) e os envia como arquivos `.yaml` para buckets GCS específicos de cada ambiente (`develop`, `homolog`, `prod`).

---
### 📁 GCS Location - Logs de Falhas

**Exemplo de path gerado**: `/composer/logs/2025/7/24/homolog_airflow-dataeng-210.yaml`  

---

### 🧠 Comportamento resumido

1. Define o intervalo de data como o **dia anterior completo** (UTC)
    
2. Consulta a base de dados do Airflow por todas as tasks que **falharam (`State.FAILED`)** nesse intervalo
    
3. Para cada tentativa de execução de cada task (`try_number`), extrai os **logs brutos**
    
4. Filtra apenas as **linhas contendo “ERROR -”**
    
5. Gera um YAML contendo todos os dados e logs
    
6. Envia o YAML para **vários buckets**, um por ambiente alvo (ex: `allos_develop_airflow_210`, `allos_prod_airflow_210`, etc.)

---
### 🔧 Principais funções

#### `find_and_report_failed_tasks()`

- Função agendada, com `@provide_session`
    
- Define `start_date` e `end_date` como o dia anterior
    
- Chama `report_failed_tasks_for_interval()`
    

#### `report_failed_tasks_for_interval(...)`

- Busca tasks com status `FAILED` no intervalo de tempo
    
- Para cada `try_number`, extrai logs com `getlog(...)`
    
- Cria dicionários com metadados + erros
    
- Serializa os dados com `yaml.safe_dump(...)`
    
- Envia para os buckets GCS definidos no template
    

#### `getlog(task_instance, try_number)`

- Usa `TaskLogReader` para ler os logs da task
    
- Tenta decodificar conteúdo para remover caracteres especiais
    
- Filtra apenas as linhas com `"ERROR -"`

---

### 📄 Exemplo de saída (`.yaml`)

```yaml
- dag_id: exemplo_dag
  task_id: transformar_dados
  run_id: manual__2025-07-24T01:00:00+00:00
  state: failed
  try_number: 1
  start_date: 2025-07-24 01:00:00
  end_date: 2025-07-24 01:05:00
  duration: 300.0
  operator: PythonOperator
  log_message:
    - "ERROR - Exception: Arquivo não encontrado"
    - "ERROR - Traceback (most recent call last): ..."
  project_id: allos-eng-dados-nonprd
  composer_env: airflow-dataeng-210
  airflow_env: homolog

```

---

### 📦 Estrutura de metadados do log de falha

|🔑 Campo|📝 Tipo|💬 Descrição|
|---|---|---|
|`dag_id`|`str`|Identificador do DAG|
|`task_id`|`str`|Nome da task que falhou|
|`run_id`|`str`|Identificador da execução|
|`state`|`str`|Estado da execução (esperado: `failed`)|
|`try_number`|`int`|Número da tentativa|
|`start_date`|`datetime`|Início da execução|
|`end_date`|`datetime`|Fim da execução|
|`duration`|`float`|Duração em segundos|
|`operator`|`str`|Nome do operador (ex: `PythonOperator`, `BashOperator`, etc.)|
|`log_message`|`list[str]`|Linhas dos logs que continham `"ERROR -"`|
|`project_id`|`str`|Projeto GCP|
|`composer_env`|`str`|Nome da instância do Composer|
|`airflow_env`|`str`|Ambiente lógico (`develop`, `homolog`, `prod`)|

---
### 🧪 Observações

- Em caso de falha na leitura do log, o script **tenta novamente após 60 segundos** (`time.sleep(60)`)
- É realizado o timesleep, pois existe uma restrição de chamadas ao log da gcp    
- Usa `TaskLogReader` do Airflow para garantir compatibilidade com vários tipos de log backend    