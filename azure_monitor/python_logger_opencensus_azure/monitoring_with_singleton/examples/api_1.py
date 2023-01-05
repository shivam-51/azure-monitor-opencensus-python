"""REST API Module using AppLogger"""

from flask import Flask, jsonify
import sys 
import os
sys.path.append(os.path.join(os.getcwd(),'monitoring'))

from src.logger import AppLogger
component_name ="API_1"
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
    logger.info("In API1 home function")
    return jsonify({'data': 'Success API1'})

app.run(host="localhost", port=8100, debug=True)
