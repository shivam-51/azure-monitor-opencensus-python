import logging
import mlflow

from os import getenv

from opencensus.ext.azure.common import utils
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware

class SingletonLoggerFactory(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonLoggerFactory, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class AppLogger(object, metaclass=SingletonLoggerFactory):
    
    HANDLER_NAME = "Azure Application Insights Handler"

    def __init__(self):
        self.config = {"log_level": "INFO"}
        self._set_log_level()
        self.log_handler = self._initialize_azure_log_handler()

    def get_logger(self, component_name="AppLogger"):
        """Get Logger Object.

        Args:
            component_name (str, optional): Name of logger. Defaults to "AppLogger".
            
        Returns:
            Logger: A logger.
        """
        logger = logging.getLogger(component_name)
        logger.setLevel(logging._nameToLevel[self.log_level])
        logger.addHandler(self.log_handler)
        
        return logger
    
    def _set_log_level(self):
        """Set log level."""
        # Get log level from environment variables.
        env_log_level = getenv( "LOG_LEVEL", None)
        # Env log level overrides every other log_level, even if it's passed to the config.
        self.log_level = self.config.get("log_level") or self.log_level
        if env_log_level is not None:
            self.log_level = env_log_level
        self.config["log_level"] = self.log_level

    def _initialize_azure_log_handler(self):
        """Initialize azure log handler."""
        logging.basicConfig(
            format="%(asctime)s name=%(name)s linenumber=%(lineno)d level=%(levelname)s %(message)s"
        )
        app_insights_cs = "InstrumentationKey=" + self._get_app_insights_key()
        log_handler = AzureLogHandler(
            connection_string=app_insights_cs, export_interval=0.0
        )
        log_handler.name = self.HANDLER_NAME
        return log_handler

    def enable_flask(self,flask_app,component_name="AppLogger"):
        """Enable flask for tracing
        For more info : https://github.com/census-instrumentation/opencensus-python/blob/master/contrib/opencensus-ext-flask/opencensus/ext/flask/flask_middleware.py

        Args:
            flask_app ([type]): [description]
            component_name (str, optional): [description]. Defaults to "AppLogger".
        """
        FlaskMiddleware(
            flask_app
            )
    
    def _get_app_insights_key(self):
        """Get Application Insights Key."""
        try:
            app_insights_key = getenv("APPLOGGER_APPINSIGHT_KEY", None)
            self.app_insights_key = app_insights_key
            if self.app_insights_key is not None:
                utils.validate_instrumentation_key(self.app_insights_key)
                return self.app_insights_key
            else:
                raise Exception("ApplicationInsights Key is not set")
        except Exception as exp:
            raise Exception(f"Exception is getting app insights key-> {exp}")

class CustomDimensionsFilter(logging.Filter):
    """Add custom-dimensions like run_id in each log by using filters."""

    def __init__(self, custom_dimensions=None):
        """Initialize CustomDimensionsFilter."""
        self.custom_dimensions = custom_dimensions or {}

    def filter(self, record):
        """Add the default custom_dimensions into the current log record."""
        dim = {**self.custom_dimensions, **getattr(record, "custom_dimensions", {})}
        record.custom_dimensions = dim
        return True

#TODO update this
def add_mlflow_run_details(loggers):
        """Adding mlflow run details to logger custom_dimensions."""
        mlflow_run = mlflow.active_run()
        # Check if mlflow_run is not None
        if mlflow_run != None:
            mlflow_run = mlflow.active_run()
            mlflow_run_id = mlflow_run.info.run_id
            mlflow_experiment_id = mlflow_run.info.experiment_id
            mlflow_experiment_name = mlflow.get_experiment(mlflow_experiment_id).name
            custom_dimensions = {}
            custom_dimensions["mlflow_run_id"] = mlflow_run_id
            custom_dimensions["mlflow_experiment_id"] = mlflow_experiment_id
            custom_dimensions["mlflow_experiment_name"] = mlflow_experiment_name
            for x in range(len(loggers)):
                loggers[x].addFilter(CustomDimensionsFilter(custom_dimensions))