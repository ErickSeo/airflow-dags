import six
import time
import logging

from airflow.exceptions import AirflowException
from airflow.providers.databricks.hooks.databricks import DatabricksHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


XCOM_RUN_ID_KEY = "run_id"
XCOM_RUN_PAGE_URL_KEY = "run_page_url"
logger = logging.getLogger(__name__)


class DatabricksCreateJobCluster(BaseOperator):
    # UI task display
    ui_color = "#55efc4"
    ui_fgcolor = "#000"

    # templated fields
    template_fields = ["notebook_task", "libraries", "new_cluster"]

    @apply_defaults
    def __init__(
        self,
        notebook_task,
        job_date='{{ execution_date.strftime("%Y-%m-%d") }}',
        new_cluster=None,
        libraries=[],
        access_control_list=None,
        databricks_retry_limit=3,
        databricks_retry_delay=1,
        priority_weight=18,
        weight_rule='absolute',
        **kwargs,
    ):
        super(DatabricksCreateJobCluster, self).__init__(
            priority_weight=priority_weight, weight_rule=weight_rule, **kwargs
        )
        self.job_date = job_date
        self.notebook_task = notebook_task
        self.new_cluster = new_cluster
        self.libraries = libraries
        self.access_control_list = access_control_list
        self._hook = None
        self.databricks_retry_limit = databricks_retry_limit
        self.databricks_retry_delay = databricks_retry_delay

        self._hook = DatabricksHook(
            retry_limit=self.databricks_retry_limit,
            retry_delay=self.databricks_retry_delay,
        )

    def execute(self, context):
        json_to_submit = {}
        json_to_submit["run_name"] = self.task_id
        json_to_submit["notebook_task"] = self.notebook_task
        json_to_submit["new_cluster"] = self.new_cluster
        json_to_submit["libraries"] = self.libraries

        if self.access_control_list is not None:
            json_to_submit["access_control_list"] = self.access_control_list
        json_to_submit = self._deep_string_coerce(json_to_submit)
        logger.info(json_to_submit)
        self.run_id = self._hook.submit_run(json_to_submit)
        self._handle_databricks_operator_execution(context)

    @staticmethod
    def _deep_string_coerce(content, json_path="json"):
        c = DatabricksCreateJobCluster._deep_string_coerce
        if isinstance(content, six.string_types):
            return content
        elif isinstance(content, six.integer_types + (float,)):
            return str(content)
        elif isinstance(content, (list, tuple)):
            return [
                c(e, "{0}[{1}]".format(json_path, i)) for i, e in enumerate(content)
            ]
        elif isinstance(content, dict):
            return {
                k: c(v, "{0}[{1}]".format(json_path, k))
                for k, v in list(content.items())
            }
        else:
            param_type = type(content)
            msg = "Type {0} used for parameter {1} is not a number or a string".format(
                param_type, json_path
            )
            raise AirflowException(msg)

    def _handle_databricks_operator_execution(self, context):
        logger.info("Run submitted with run_id: {}".format(self.run_id))
        self.run_page_url = self._hook.get_run_page_url(self.run_id)
        self._wait_for_cluster_initialization()
        # push xcom variables
        logger.info("Pushing run_id and run_page_url...")
        context["ti"].xcom_push(key=XCOM_RUN_ID_KEY, value=self.run_id)
        context["ti"].xcom_push(key=XCOM_RUN_PAGE_URL_KEY, value=self.run_page_url)

    def _wait_for_cluster_initialization(self):
        api_retry_counter = 0
        while True:
            try:
                run_state = self._hook.get_run_state(self.run_id)
                if run_state.is_terminal:
                    if run_state.is_successful:
                        logger.info("{} completed successfully.".format(self.task_id))
                        logger.info(
                            "View run status, Spark UI, and logs at {}".format(
                                self.run_page_url
                            )
                        )
                        break
                    else:
                        logger.info(
                            "View run status, Spark UI, and logs at {}".format(
                                self.run_page_url
                            )
                        )
                        error_message = "{t} failed with terminal state: {s}".format(
                            t=self.task_id, s=run_state
                        )
                        raise AirflowException(error_message)
                else:
                    if run_state.life_cycle_state != "PENDING":
                        logger.info("Cluster is now running.")
                        break
                    logger.info(
                        "{t} is in PENDING state: {s}".format(
                            t=self.task_id, s=run_state
                        )
                    )
                    logger.info(
                        "View run status, Spark UI, and logs at {}".format(
                            self.run_page_url
                        )
                    )
                    logger.info("Sleeping for 30 seconds.")
                    time.sleep(30)
            except AirflowException as e:
                raise AirflowException(e)
            except Exception as e:
                # API request error etc
                logger.info(e)
                if api_retry_counter == 5:
                    raise Exception(e)
                else:
                    api_retry_counter = api_retry_counter + 1
                # 2 seconds above requests peak
                time.sleep(12)