from airflow.exceptions import AirflowException
from airflow.providers.databricks.hooks.databricks import DatabricksHook
from airflow.providers.databricks.operators.databricks import DatabricksJobRunLink
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

import datetime, json


XCOM_RUN_ID_KEY = 'run_id'
XCOM_RUN_PAGE_URL_KEY = 'run_page_url'
XCOM_RUN_STARTED_AT_KEY = 'started_at'
XCOM_RUN_FINISHED_AT_KEY = 'finished_at'

class DatabricksJobSensor(BaseSensorOperator):

    # Databricks brand color (blue) under white text
    ui_color = '#FFCCCC'
    ui_fgcolor = '#000'

    # templated fields
    template_fields = ['run_id', 'run_page_url']
    operator_extra_links = (DatabricksJobRunLink(),)

    @apply_defaults
    def __init__(
            self,
            run_id,
            run_page_url,
            polling_period_seconds=60,
            databricks_retry_limit=6,
            databricks_retry_delay=1,
            priority_weight=19,
            weight_rule='absolute',
            **kwargs):
        self.timeout = 43200 #12 horas
        super(DatabricksJobSensor, self).__init__(poke_interval=polling_period_seconds,
                                                  priority_weight=priority_weight,
                                                  weight_rule=weight_rule,
                                                  **kwargs)
        self.run_id = run_id
        self.run_page_url = run_page_url
        self.polling_period_seconds = polling_period_seconds
        self.databricks_retry_limit = databricks_retry_limit
        self.databricks_retry_delay = databricks_retry_delay
        self._hook = DatabricksHook(
            retry_limit=self.databricks_retry_limit,
            retry_delay=self.databricks_retry_delay
        )

    def _write_information_to_xcom(self, context):
        context['ti'].xcom_push(key=XCOM_RUN_ID_KEY, value=self.run_id)
        self.log.info('Set run_id in Xcom: %s', self.run_id)

        context['ti'].xcom_push(key=XCOM_RUN_PAGE_URL_KEY, value=self.run_page_url)
        self.log.info('Set run_page_url in Xcom %s', self.run_page_url)

        context['ti'].xcom_push(key=XCOM_RUN_STARTED_AT_KEY, value=str(context["task_instance"].start_date))
        self.log.info('Set started_at in Xcom %s', str(context["task_instance"].start_date))

        context['ti'].xcom_push(key=XCOM_RUN_FINISHED_AT_KEY, value=str(datetime.datetime.now())+'+00:00')
        self.log.info('Set finished_at in Xcom %s', str(datetime.datetime.now())+'+00:00')
    
    def _get_previous_task_info(self, context):
        try:
            previous_task = context['task'].upstream_list[0]
            spark_vars = previous_task.spark_env_vars
            return json.loads(spark_vars['TAGS'])
        except:
            self.log.warn('Could not retrieve previous task info')
        
        return None
        
    def poke(self, context):
        run_state = self._hook.get_run_state(self.run_id)
        if run_state.is_terminal:
            self._write_information_to_xcom(context)
            table_name = context["task_instance"].task_id
            previous_task_info = self._get_previous_task_info(context)
            if run_state.is_successful:
                self.log.info('{} completed successfully.'.format(self.task_id))
                self.log.info('View run status, Spark UI, and logs at {}'.format(self.run_page_url))
                return True
            else:
                self.log.info('View run status, Spark UI, and logs at {}'.format(self.run_page_url))
                error_message = '{t} failed with terminal state: {s}'.format(
                    t=self.task_id,
                    s=run_state)
                raise AirflowException(error_message)
        else:
            self.log.info('{t} in run state: {s}'.format(t=self.task_id, s=run_state))
            self.log.info('View run status, Spark UI, and logs at {}'.format(self.run_page_url))
            self.log.info('Sleeping for {} seconds.'.format(str(self.polling_period_seconds)))
            return False