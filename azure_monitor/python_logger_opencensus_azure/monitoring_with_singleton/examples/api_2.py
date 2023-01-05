"""REST API Module using AppLogger"""
import logging
import json
from flask import Flask, jsonify
import requests
import sys 
import os
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger
component_name ="API_2"
app = Flask(component_name)

app_logger = AppLogger()

app_logger.enable_flask(flask_app=app,component_name= component_name)
logger = app_logger.get_logger(component_name=component_name)

@app.route('/', methods=['GET'])
def home():
    """End point for API2

    Returns:
        [Json]: [{'data': '<return string>'}]
    """
    logger.info("In API2 home function")


    logger.info("Calling API 1")
    response = requests.get(url='http://localhost:8100/')
    print(f"response = {response.content}")

    return jsonify({'data': 'Success API2'})


if __name__ == "__main__":
    app.run(host="localhost", port=8300,debug=True)