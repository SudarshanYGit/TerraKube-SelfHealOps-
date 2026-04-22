from flask import Flask, jsonify, render_template_string, request
import logging
import os
import psutil

app = Flask(__name__)

# -------------------- LOG SETUP --------------------
if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/app.log")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# -------------------- REAL REQUEST LOGGING --------------------
@app.before_request
def log_request():
    logger.info(f"Request: {request.method} {request.path}")

# -------------------- ERROR RATE FUNCTION --------------------
def calculate_error_rate():
    try:
        with open("logs/app.log") as f:
            lines = f.readlines()
        total = len(lines)
        errors = [l for l in lines if "ERROR" in l or "CRITICAL" in l]
        return int((len(errors) / max(total, 1)) * 100)
    except:
        return 0

# -------------------- DASHBOARD UI --------------------
dashboard_html = """
<!DOCTYPE html>
<html>
<title>AI Live-Log Monitoring Dashboard</title> <!-- Elegant Serif Font --> <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&display=swap" rel="stylesheet"> <style> body { margin: 0; font-family: 'Playfair Display', serif; background: #E5D0B6; /* cream background */ text-align: center; } /* HEADER (same maroon style) */ .header { background: #6B0F1A; /* maroon */ color: #F2B418; /* golden text */ padding: 20px; font-size: 30px; font-weight: 700; letter-spacing: 1px; }


.metrics { display:flex; justify-content:center; margin-top:20px; }
.metric-card {
    background:white; padding:20px; margin:10px;
    border-radius:10px; width:180px; font-size:22px;
    box-shadow:0 0 10px rgba(0,0,0,0.5);
}

.logs {
    background:black; color:white;
    margin:30px auto; padding:15px;
    height:300px; overflow:auto;
    width:90%; border-radius:10px;
    text-align:left; font-family:monospace;
}

.info { color:#22c55e; }
.warning { color:#facc15; }
.error { color:#ef4444; }
.critical { color:#f97316; font-weight:bold; }
</style>
</head>
<body>

<div class="header">AI Live-Log Monitoring Dashboard</div>

<div class="metrics">
    <div class="metric-card">CPU<br><h2 id="cpu">0%</h2></div>
    <div class="metric-card">Memory<br><h2 id="memory">0%</h2></div>
    <div class="metric-card">Error Rate<br><h2 id="error">0%</h2></div>
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
    });
}

function loadMetrics(){
    fetch('/metrics')
    .then(res => res.json())
    .then(data => {
        document.getElementById("cpu").innerText = data.cpu_usage + "%";
        document.getElementById("memory").innerText = data.memory_usage + "%";
        document.getElementById("error").innerText = data.error_rate + "%";
    });
}

setInterval(loadLogs, 2000);
setInterval(loadMetrics, 3000);
</script>

</body>
</html>
"""

# -------------------- ROUTES --------------------
@app.route("/")
def dashboard():
    return render_template_string(dashboard_html)

@app.route("/logs")
def get_logs():
    try:
        with open("logs/app.log") as f:
            lines = f.readlines()[-20:]
        return jsonify(lines)
    except:
        return jsonify(["No logs yet"])

@app.route("/metrics")
def metrics():
    return jsonify({
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "error_rate": calculate_error_rate()
    })

@app.route("/health")
def health():
    return "OK", 200

# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
