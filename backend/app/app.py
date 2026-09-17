from flask import Flask, jsonify, Response
import os
import mysql.connector
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "ecommerce"),
        user=os.getenv("DB_USER", "ecommerce"),
        password=os.environ["DB_PASSWORD"]
    )


@app.before_request
def start_timer():
    from time import time
    from flask import g

    g.start_time = time()


@app.after_request
def record_metrics(response):
    from time import time
    from flask import request, g

    latency = time() - g.start_time

    REQUEST_COUNT.labels(
        request.method,
        request.path,
        response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        request.method,
        request.path
    ).observe(latency)

    return response


@app.route("/health")
def health():
    return jsonify({"status": "UP"})


@app.route("/api/products")
def products():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id, name, price FROM products")
    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(products)


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
