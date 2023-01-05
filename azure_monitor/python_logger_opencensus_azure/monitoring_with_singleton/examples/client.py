""""REST API Client Module using AppLogger"""
import requests
import sys 
import os
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger

component_name = "client"

app_logger = AppLogger()
logger = app_logger.get_logger(component_name=component_name)

def call_api_2():
    """Function calling endpoint of API2
    """
    logger.info("Calling API 2")
    response = requests.get(url='http://localhost:8300/')
    print(f"response = {response.content}")


if __name__ == '__main__':
    call_api_2()