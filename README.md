
> [!NOTE] 
> A Dag tem como objetivo extrair metadados e logs do Airflow.
> Essa DAG é voltada para controle, auditoria e análise da execução de pipelines no Airflow, e está categorizada com as tags `data-gov`, `airflow` e `dag`.

⏰ Schedule:  
	Executada diariamente à meia-noite UTC (`0 0 * * *`)


---

# 💻 Tasks:

## ▶️ list_airflow_dags


> [!NOTE] 
> Extrai todas as DAGs registradas no ambiente atual do Composer e exporta os metadados para arquivos `.yaml`, um para cada ambiente (develop, homolog, prod).
> Os arquivos são enviados para buckets GCS específicos de cada ambiente.

### 📁 GCS Location - Yaml Output
<br>
**Exemplo**:  
&nbsp;composer: [airflow-dataeng-210](https://f15ee860cc8342aa96394d786a0ef819-dot-us-east1.composer.googleusercontent.com/)  
projeto: allos-eng-dados-nonprd  
environment: homolog  

**filename_pattern**:  `/composer/dag/<gcp_project_id>-<composer_name>-<environment>.yaml`  


  
O Yaml vai ser salvo no path:  
/composer/dag/allos-eng-dados-nonprd-airflow-dataeng-210-homolog.yaml

