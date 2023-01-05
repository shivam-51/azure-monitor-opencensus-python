"""Test rprs_ds/monitoring/app_logger.py."""
import os

from src.logger import AppLogger

def get_logger():
    app_logger = AppLogger();

    # logger = app_logger.get_logger();
    return app_logger

def test_logger_creation(get_logger):
    """Test with valid formatted instrumentation key."""
    try:
        app_logger = get_logger
        assert app_logger is not None
    except Exception:
        assert False

def test_logging(get_logger):
    """Test to use logging functions."""
    try:
        component_name = "TestComponent"
        app_logger = get_logger
        assert app_logger is not None
        test_logger = app_logger.get_logger(
            component_name=component_name,
        )

        assert test_logger is not None
        test_logger.info("Test Logging")
    except Exception:
        assert False

def test_exception(get_logger):
    """Test for calling logger.exception method."""
    try:
        component_name = "TestComponent"
        app_logger = get_logger
        assert app_logger is not None

        test_logger = app_logger.get_logger(
            component_name=component_name,
        )
        assert test_logger is not None
        try:
            raise Exception("Testing exception logging")
        except Exception as exp:
            test_logger.exception(exp)
    except Exception:
        assert False

def test_logging_extra_params(get_logger):
    """Test logging extra params."""
    try:
        component_name = "TestComponent"
        app_logger = get_logger
        test_logger = app_logger.get_logger(
            component_name=component_name,
        )
        extra_params = {"custom_dimensions": {"key1": "value1"}}
        test_logger.info("Logging extra params", extra=extra_params)
    except Exception:
        assert False
