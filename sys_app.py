from flask import Flask, jsonify, render_template_string
import psutil
import platform

app = Flask(__name__)

# The new Graphical User Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>SysMonitor | OS Daemon</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 90vh; }
        .card { background: #161b22; padding: 30px; border-radius: 12px; width: 100%; max-width: 500px; border: 1px solid #30363d; box-shadow: 0 8px 24px rgba(0,0,0,0.8); }
        h2 { margin-top: 0; text-align: center; color: #fff; }
        p { text-align: center; color: #8b949e; margin-bottom: 25px; }
        .metric { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #30363d; font-size: 16px; }
        .metric span { font-weight: bold; color: #58a6ff; }
        .bar-container { text-align: left; padding: 15px 0; font-size: 16px; font-weight: bold; color: #e6edf3;}
        .progress-bar { width: 100%; background: #21262d; border-radius: 6px; overflow: hidden; margin-top: 8px; height: 12px; border: 1px solid #30363d;}
        .progress { height: 100%; transition: width 0.5s ease-in-out; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🖥️ SysMonitor Daemon</h2>
        <p>Real-Time Cloud OS Resource Tracker</p>
        <div id="metrics">
            <div style="text-align:center; color:#8b949e;">Connecting to Kernel...</div>
        </div>
    </div>
    <script>
        async function fetchMetrics() {
            try {
                const response = await fetch('/api/system/metrics');
                const data = await response.json();
                const m = data.system_metrics;
                
                // Change color to red if usage is over 80%
                const cpuColor = m.cpu_usage_percent > 80 ? '#f85149' : '#3fb950';
                const memColor = m.memory_used_percent > 80 ? '#f85149' : '#a371f7';

                document.getElementById('metrics').innerHTML = `
                    <div class="metric"><div>Operating System</div><span>${m.os_system} ${m.os_release}</span></div>
                    <div class="metric"><div>Logical Cores</div><span>${m.cpu_logical_cores} Cores</span></div>
                    <div class="metric"><div>Total Server Memory</div><span>${m.memory_total_gb} GB</span></div>
                    <div class="metric"><div>Active Thread PIDs</div><span>${m.active_pids}</span></div>
                    
                    <div class="bar-container">
                        CPU Usage (${m.cpu_usage_percent}%)
                        <div class="progress-bar"><div class="progress" style="width: ${m.cpu_usage_percent}%; background: ${cpuColor};"></div></div>
                    </div>
                    <div class="bar-container">
                        Memory Allocation (${m.memory_used_percent}%)
                        <div class="progress-bar"><div class="progress" style="width: ${m.memory_used_percent}%; background: ${memColor};"></div></div>
                    </div>
                `;
            } catch (e) {
                console.log('Error fetching metrics');
            }
        }
        
        fetchMetrics(); // Load immediately
        setInterval(fetchMetrics, 2000); // Auto-refresh data every 2 seconds
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/system/metrics', methods=['GET'])
def get_system_metrics():
    try:
        metrics = {
            "os_system": platform.system(),
            "os_release": platform.release(),
            "cpu_usage_percent": psutil.cpu_percent(interval=0.1),
            "cpu_logical_cores": psutil.cpu_count(logical=True),
            "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "memory_used_percent": psutil.virtual_memory().percent,
            "active_pids": len(psutil.pids())
        }
        return jsonify({"status": "healthy", "system_metrics": metrics})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
