import base64, os, logging

from airflow.providers.databricks.hooks.databricks import DatabricksHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

logger = logging.getLogger(__name__)

class UploadDatabricksNotebook(BaseOperator):
    @apply_defaults
    def __init__(
            self,
            local_file_path,
            remote_file_path,
            databricks_conn_id='databricks_default',
            databricks_retry_limit=3,
            databricks_retry_delay=1,
            *args, **kwargs):

        self.databricks_conn_id = databricks_conn_id

        self.local_file_path = local_file_path
        self.remote_file_path = remote_file_path

        self.databricks_retry_limit = databricks_retry_limit
        self.databricks_retry_delay = databricks_retry_delay

        super(UploadDatabricksNotebook, self).__init__(*args, **kwargs)

    def execute(self, context):
        hook = self._get_hook()
        
        self._create_dirs(hook)
        
        if self._exists_file(hook):
            self._delete_file(hook)

        self._upload_file(hook)

    def _create_dirs(self, hook):

        all_directories = self.remote_file_path.split('/')[1:-1]
        parsed_directories = ['']

        for directory in all_directories:
            parsed_directories.append(directory)
            current_path = '/'.join(parsed_directories)
            self._create_dir(current_path, hook)

    def _get_hook(self):
        return DatabricksHook(
            self.databricks_conn_id,
            retry_limit=self.databricks_retry_limit,
            retry_delay=self.databricks_retry_delay)

    def _exists_file(self, hook):

        try:

            response = hook._do_api_call(
                ("GET", "api/2.0/workspace/get-status"),
                self.remote_file_path
            )

            response.raise_for_status()

            return True

        except Exception as e:
            
            logger.error(f"The file {self.remote_file_path} does not exists in databricks!!")
            logger.error(e)

            return False

    def _create_dir(self, dir_path, hook):

        return hook._do_api_call(('POST',
                                  'api/2.0/workspace/mkdirs'),
                                 {'path': dir_path})

    def _delete_file(self, hook):
        response = None

        data = {
            "path": self.remote_file_path,
            "recursive": "true"
        }

        try:
            response = hook._do_api_call(('POST',
                                  'api/2.0/workspace/delete'),
                                 data)

        except Exception as e:
            logger.error("Error while deleting file")
            logger.error(e)

        return response


    def _upload_file(self, hook):

        local_file_data = self._get_local_file_content()
        logger.info("Logging file content from local:")
        logger.info(local_file_data)

        logger.info("Uploading file from local")
        file_content = local_file_data

        data = {
            "path": self.remote_file_path,
            "format": "SOURCE",
            "language": "PYTHON",
            "content": base64.b64encode(file_content.encode('utf-8')).decode('utf-8'),
            "overwrite": "true"
        }

        return hook._do_api_call(('POST',
                                  'api/2.0/workspace/import'),
                                 data)

    def _get_local_file_content(self):
        f = open(self.local_file_path, 'r')
        filedata = f.read()
        f.close()
        return filedata