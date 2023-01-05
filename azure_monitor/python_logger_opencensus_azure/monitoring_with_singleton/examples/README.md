# Overview

This document will give the overview about examples created using AppLogger class.

## Examples

1. **api_1.py**: This is a flask api which exposes one rest end point and uses AppLogger
1. **api_2.py**: This is a flask api which exposes one rest end point and uses AppLogger. This rest end point calls:
    1. Rest end point exposed in **api_1.py**
1. **client**: This is client code which calls:
    1. Rest end point exposed in **api_2.py**

## Usage

Following are the steps to execute the examples:

1. Follow Prerequisites mentioned in [section.](../../README.md#prerequisites-for-using-applogger)

2. Get Application Insights Instrumentation Key (app_insights_instrumentation_key) and add it as an environment variable.

```bash
export APPLOGGER_APPINSIGHT_KEY=<app_insights_instrumentation_key>
```


3. Install pip packages

```bash
pip install -r .\monitoring_with_singleton\requirements.txt
```

4. Execute examples in following sequence:

    1. Run `api_1.py` flask app

    ```bash
    python .\monitoring_with_singleton\examples\api_1.py 
    ```

    2. Run `api_2.py` flask app

    ```bash
    python .\monitoring_with_singleton\examples\api_2.py 
    ```

    3. Run client.py

    ```bash
    python .\monitoring_with_singleton\examples\client.py 
    ```

## Results of executing examples:

1. Execution of `client.py` produces some logs on console
```sh
❯ python .\monitoring_with_singleton\examples\client.py
2023-01-05 11:26:33,450 name=client linenumber=17 level=INFO Calling API 2
response = b'{\n  "data": "Success API2"\n}\n'
```
2. Use following Kusto query to get the logs in application insights.

```py
traces
```

3. Use following Kusto query to get the dependency in application insights.
```py
dependencies
```
