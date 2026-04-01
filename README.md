# TerraKube-SelfHealOps 🚀

> **Cloud-Native CI/CD + Terraform Infrastructure + Intelligent Log Monitoring + Kubernetes Auto-Healing**
- **🤖 AI Log Anomaly Detection** — Real-time scanning of application logs to detect unusual patterns and error spikes
- **🔄 Kubernetes Auto-Healing** — Automatically restarts crashed pods and reschedules failed containers
- **🏗️ Infrastructure as Code** — Full AWS EC2 environment provisioned via Terraform (reproducible, version-controlled)
- **🚢 Automated CI/CD** — Push to `main` triggers Docker build → image push → Kubernetes rollout via GitHub Actions
- **📊 Live Dashboard** — Flask-based monitoring UI with real-time CPU, memory, and error rate metrics
- **📋 Live Log Stream** — Color-coded logs (INFO / WARNING / ERROR / CRITICAL) streamed to the browser
- **🛠️ Service Simulation** — Buttons to simulate login, API calls, payments, errors, and container crashes for demo

### AI Live-Log Monitoring Dashboard
> Real-time CPU, Memory, and Error Rate metrics with color-coded log stream and AI anomaly detection.


## 🏗️ Architecture


Python Flask App
      │
      ▼
GitHub Actions (CI/CD)
      │
      ▼
Docker (Build & Push Image)
      │
   ┌──┴──┐
   ▼     ▼
Terraform  AWS EC2
(IaC)   (Cloud Nodes)
   └──┬──┘
      ▼
 Kubernetes (Orchestration)
      │
   ┌──┴──┐
   ▼     ▼
Prometheus  Grafana
(Metrics)  (Dashboard)
   └──┬──┘
      ▼
Log Anomaly Detection + Auto-Healing
      │
      └──► (feedback loop back to Kubernetes)
```

## 🛠️ Tech Stack

| Layer            | Technology                          |
|------------------|-------------------------------------|
| Application      | Python Flask                        |
| Containerization | Docker                              |
| Infrastructure   | Terraform                           |
| Cloud            | AWS EC2                             |
| Orchestration    | Kubernetes                          |
| CI/CD            | GitHub Actions                      |
| Monitoring       | Prometheus                          |
| Visualization    | Grafana                             |
| Reliability      | Log anomaly detection + auto-healing|

Visit `http://127.0.0.1:5000` to open the AI Live-Log Monitoring Dashboard

## 📊 Monitoring

| Tool       | Purpose                        | Access                  |
|------------|--------------------------------|-------------------------|
| Flask Dashboard | Live log stream + AI alerts | `http://localhost:5000` |
| Prometheus | Metrics scraping               | `http://localhost:9090` |
| Grafana    | Dashboards and visualization   | `http://localhost:3000` |

---

## 🧠 AI Anomaly Detection Logic

The system continuously parses application logs and uses pattern recognition to flag anomalies:

- **High error rate** — Triggers WARNING when ERROR/CRITICAL log count exceeds threshold
- **Latency spikes** — Detects API response times above baseline
- **Container crashes** — Identifies CRITICAL crash events and triggers Kubernetes pod restart
- **Cascade failures** — Detects repeated failures across multiple services

When anomalies are detected, a Kubernetes auto-heal action is triggered:
AI detects anomaly → Alert logged → K8s pod restarted → System recovers it.
