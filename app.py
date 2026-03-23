#Open the Browser for the Dashboard: http://127.0.0.1:5000/
from flask import Flask, jsonify, render_template_string, redirect
import logging
import random
import os
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

# Create logs folder
if not os.path.exists("logs"):
    os.makedirs("logs")

# Setup application logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/app.log")
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)
file_handler.setFormatter(formatter)    
logger.addHandler(file_handler)

# Disable Flask default logs
werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.setLevel(logging.ERROR)

dashboard_html = """
<!DOCTYPE html>
<html>
<head>
<title>AI Log Monitoring Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron&display=swap" rel="stylesheet">

<style>
body {
    margin: 0;
    font-family: tim;
    background: #F8E0C9;
    color: #F2B418;
}

.header {
    text-align: center;
    padding: 20px;
    font-size: 28px;
    font-weight: bold;
    background: #5E1525;
    border-bottom: 2px solid #1e293b;
}

.metrics {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.metric-card {
    background: #ffffff;
    color: #333;
    padding: 20px;
    margin: 10px;
    border-radius: 10px;
    width: 180px;
    text-align: center;
    font-size: 28px;
    box-shadow: 0 0 10px rgba(0,0,0,0.6);
}

.cards {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 20px;
}

.card {
    background: #ffffff;
    color: #333;
    padding: 20px;
    margin: 10px;
    border-radius: 10px;
    width: 180px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0,0,0,0.6);
}

.card button {
    padding: 10px;
    width: 100%;
    border: none;
    border-radius: 5px;
    background: #160D08;
    color: white;
    cursor: pointer;
}

.card button:hover {
    background: #800000;
}

.logs {
    background: black;
    margin: 30px auto;
    padding: 15px;
    height: 320px;
    overflow: auto;
    width: 90%;
    border-radius: 10px;
    font-family: monospace;
    text-align: left;
}

.info { color: #22c55e; }
.warning { color: #facc15; }
.error { color: #ef4444; }
.critical { color: #f97316; font-weight: bold; }
</style>
</head>
<body>

<div class="header">
AI Live-Log Monitoring Dashboard
</div>

<div class="metrics">
<div class="metric-card">CPU Usage<br><h2 id="cpu">45%</h2></div>
<div class="metric-card">Memory Usage<br><h2 id="memory">60%</h2></div>
<div class="metric-card">Error Rate<br><h2 id="error">3%</h2></div>
</div>

<div class="cards">
<div class="card"><h3>Login Service</h3><a href="/simulate/login"><button>Simulate Login</button></a></div>
<div class="card"><h3>API Gateway</h3><a href="/simulate/api"><button>Send API Request</button></a></div>
<div class="card"><h3>Payment</h3><a href="/simulate/payment"><button>Process Payment</button></a></div>
<div class="card"><h3>Generate Error</h3><a href="/simulate/error"><button>Create Error</button></a></div>
<div class="card"><h3>Crash Service</h3><a href="/simulate/crash"><button>Crash Container</button></a></div>
<div class="card"><h3>AI Analyzer</h3><a href="/analyze"><button>Run AI Analysis</button></a></div>
</div>

<div class="logs" id="logs"></div>

<script>
function loadLogs(){
fetch('/logs')
.then(res => res.json())
.then(data => {
let html = "";
data.forEach(line => {
    if(line.includes("INFO")) html += "<div class='info'>" + line + "</div>";
    else if(line.includes("WARNING")) html += "<div class='warning'>" + line + "</div>";
    else if(line.includes("ERROR")) html += "<div class='error'>" + line + "</div>";
    else if(line.includes("CRITICAL")) html += "<div class='critical'>" + line + "</div>";
    else html += "<div>" + line + "</div>";
});
document.getElementById("logs").innerHTML = html;
})
}

function loadMetrics(){
fetch('/metrics')
.then(res => res.json())
.then(data => {
document.getElementById("cpu").innerText = data.cpu_usage + "%";
document.getElementById("memory").innerText = data.memory_usage + "%";
document.getElementById("error").innerText = data.error_rate + "%";
})
}

setInterval(loadLogs,2000)
setInterval(loadMetrics,3000)
</script>

</body>
</html>
"""

@app.route("/")
def dashboard():
    return render_template_string(dashboard_html)

services = ["Auth-Service", "Payment-Service", "API-Gateway", "Database", "AI-Service"]

@app.route("/simulate/<event>")
def simulate(event):
    service = random.choice(services)

    if event == "login":
        logger.info(f"{service} | User login successful")

    elif event == "api":
        response_time = random.randint(100,2000)
        logger.info(f"{service} | API response time {response_time}ms")
        if response_time > 1500:
            logger.warning(f"{service} | High latency detected")

    elif event == "payment":
        logger.info(f"{service} | Payment processed")

    elif event == "error":
        logger.error(f"{service} | Database connection failed")

    elif event == "crash":
        logger.critical(f"{service} | Container crashed")

    return redirect("/")

@app.route("/logs")
def get_logs():
    try:
        with open("logs/app.log") as f:
            lines = f.readlines()[-20:]
        return jsonify(lines)
    except:
        return jsonify(["No logs yet"])

# AI Log Analysis
@app.route("/analyze")
def analyze_logs():
    data = []

    with open("logs/app.log") as f:
        for line in f:
            if "ERROR" in line or "CRITICAL" in line:
                data.append([1])
            else:
                data.append([0])

    if len(data) < 5:
        return redirect("/")

    model = IsolationForest(contamination=0.2)
    model.fit(data)
    preds = model.predict(data)

    anomalies = preds.tolist().count(-1)

    logger.warning(f"AI detected {anomalies} anomalies")

    return redirect("/")

# Health check endpoint (for Kubernetes auto-healing)
@app.route("/health")
def health():
    return "OK", 200

# Metrics endpoint (for Prometheus later)
@app.route("/metrics")
def metrics():
    return jsonify({
        "cpu_usage": random.randint(20,80),
        "memory_usage": random.randint(30,90),
        "error_rate": random.randint(0,10)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)