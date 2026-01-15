from flask import Flask, request
import redis
import time
import os
from prometheus_flask_exporter import PrometheusMetrics # Перенесли импорт вверх

app = Flask(__name__)
metrics = PrometheusMetrics(app) # Инициализируем метрики сразу

# Подключаемся к Redis
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def hello():
    req_id = request.headers.get('X-Request-ID', 'no-id')
    hits = cache.incr('hits')
    
    log_entry = f"ID: {req_id} | Time: {time.ctime()} | Server: {os.uname()[1]}"
    cache.rpush('visit_logs', log_entry)

    return f'''
    <h1>Система мониторинга запущена! 🚀</h1>
    <p>Просмотров всего: {hits}</p>
    <p>Ваш уникальный Request ID: <code>{req_id}</code></p>
    <hr>
    <p>Запрос обработан контейнером: {os.uname()[1]}</p>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
