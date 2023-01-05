import logging;

class SingletonLoggerFactory(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonLoggerFactory, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class AppLogger(object, metaclass=SingletonLoggerFactory):
    
    HANDLER_NAME = "Azure Application Insights Handler"

    def __init__(self, config):
        self.config = {"log_level": "INFO", "logging_enabled": "true"}
        logging.basicConfig(
                format="%(asctime)s name=%(name)s linenumber=%(lineno)d level=%(levelname)s %(message)s"
            )

    def get_logger(self, component_name="AppLogger2"):
        """Get Logger Object.

        Args:
            component_name (str, optional): Name of logger. Defaults to "AppLogger".
            
        Returns:
            Logger: A logger.
        """
        logger = logging.getLogger(component_name)
        return logger
    

def test_function():
    logger = AppLogger({}).get_logger()
    logger.error("Hello, World!")
    
    
    logger2 = AppLogger({}).get_logger("Updated")
    logger2.error("Hello, World!")


if __name__ == "__main__":
    test_function()