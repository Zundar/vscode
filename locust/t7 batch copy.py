import json
import time
import requests

from termcolor import colored

class MetricsBatch:

    def __init__(self):
        self.batch = []

    def add_metric(self, metric_name, values, labels={}):
        timestamps = [int(time.time()) for _ in values]
        metric = {
            'metric': {**{'__name__': metric_name}, **labels},
            'values': values,
            'timestamps': timestamps
        }
        self.batch.append(metric)

    def to_json(self):
        return json.dumps(self.batch)

class VictoriaMetricsWriter:

    def __init__(self, host='http://localhost:8428', endpoint='/api/v1/write'):
        self.host = host
        self.endpoint = endpoint
        self.metrics_batch = MetricsBatch()

    def add_metric(self, metric_name, values, labels={}):
        self.metrics_batch.add_metric( metric_name, values, labels={})

    def write(self, data):
        response = requests.post(f"{self.host}{self.endpoint}", data=data)
        if response.status_code != 204:
            raise Exception(f'Couldn\'t write data to VictoriaMetrics: {response.text}')

    def write_print2(self):
        print((f"==>> self.metrics_batch.to_json(): {self.metrics_batch.to_json()}", "red"))

    def write_print(self, data):
        # response = requests.post(self.url, data=data)
        print((f"==>> data: {data}", "red"))
        # if response.status_code != 204:
        #     raise Exception(f'Couldn\'t write data to VictoriaMetrics: {response.text}')

# metrics_batch = MetricsBatch()
# metrics_batch.add_metric('temperature', [22.5], [1638524171], {'room': 'kitchen'})
# metrics_batch.add_metric('humidity', [45.3], [1638524171], {'room': 'living_room', 'fp': '1'})

# writer = VictoriaMetricsWriter('http://localhost:8428/api/v1/write')
# writer.write_print(metrics_batch.to_json())
# # writer.write(metrics_batch.to_json())
        
writer = VictoriaMetricsWriter('http://localhost:8428')
writer.add_metric('temperature', [22.5], {'room': 'kitchen'})
writer.add_metric('humidity', [45.3], {'room': 'living_room', 'fp': '1'})
writer.write_print2()

print(colored(f"==>> time.time(): {int(time.time())}", "red"))