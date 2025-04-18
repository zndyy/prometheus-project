from flask import Flask, Response
from prometheus_client import Counter, Gauge, generate_latest
import platform
import os

app = Flask(__name__)

# Счётчик для HTTP запросов
REQUESTS = Counter("http_requests_total", "Total HTTP requests")

# Метрика для типа хоста
HOST_ENV = Gauge("host_environment", "Host environment type", ["type"])

# Функция для определения типа хоста (виртуальная машина, контейнер или физический сервер)
def detect_environment():
    if os.path.exists("/.dockerenv"):
        return "container"
    elif os.path.exists("/sys/class/dmi/id/product_name"):
        with open("/sys/class/dmi/id/product_name") as f:
            name = f.read().lower()
            if "virtual" in name or "vmware" in name:
                return "virtual_machine"
    return "physical_machine"

# Маршрут для метрик
@app.route("/")
def metrics():
    REQUESTS.inc()  # Увеличиваем счётчик запросов
    env_type = detect_environment()  # Определяем тип хоста
    HOST_ENV.labels(type=env_type).set(1)  # Обновляем метрику типа хоста
    return Response(generate_latest(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
