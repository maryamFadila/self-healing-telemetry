from flask import Flask, Response, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP Requests', 
    ['method', 'endpoint', 'status_code']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'HTTP Request Latency', 
    ['endpoint']
)
FAILURE_COUNT = Counter(
    'app_failures_total', 
    'Total Simulated App Failures'
)

@app.route('/')
def home():
    start_time = time.time()
    status_code = 200
    
    duration = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint='/').observe(duration)
    REQUEST_COUNT.labels(method='GET', endpoint='/', status_code=status_code).inc()
    
    return jsonify({"status": "healthy", "message": "App is running smoothly!"}), status_code

@app.route('/simulate-failure')
def simulate_failure():

    status_code = 500
    FAILURE_COUNT.inc()
    REQUEST_COUNT.labels(method='GET', endpoint='/simulate-failure', status_code=status_code).inc()
    
    return jsonify({"status": "error", "message": "Simulated failure triggered!"}), status_code

@app.route('/metrics')
def metrics():
   
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
