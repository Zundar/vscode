import json

class MetricsBatch:
    
    def __init__(self):
        self.batch = []
        
    def add_metric(self, metric):
        self.batch.append(metric)
        
    def get_batch(self):
        return self.batch
                
    def to_json(self):
        return json.dumps(self.batch, ensure_ascii=False)

# Создаем экземпляр класса MetricsBatch
metrics_batch = MetricsBatch()

# Добавляем в батч несколько метрик в виде словарей
metrics_batch.add_metric({'metric_name': 'clicks', 'value': 120})
metrics_batch.add_metric({'metric_name': 'views', 'value': 4500})
metrics_batch.add_metric({'metric_name': 'conversions', 'value': 47})

# Выводим содержимое батча
print(metrics_batch.get_batch())

# Добавляем еще одну метрику
metrics_batch.add_metric({'metric_name': 'bounces', 'value': 32})

# Преобразовываем содержимое батча в формат JSON и выводим его
print(metrics_batch.to_json())
