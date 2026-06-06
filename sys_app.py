from flask import Flask, jsonify
import psutil
import platform

app = Flask(__name__)

@app.route('/api/system/metrics', methods=['GET'])
def get_system_metrics():
    # Gathering core Operating System and Hardware fundamentals
    try:
        metrics = {
            "os_system": platform.system(),
            "os_release": platform.release(),
            "cpu_usage_percent": psutil.cpu_percent(interval=0.1),
            "cpu_logical_cores": psutil.cpu_count(logical=True),
            "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "memory_used_percent": psutil.virtual_memory().percent,
            "active_pids": len(psutil.pids()) # Process IDs
        }
        return jsonify({"status": "healthy", "system_metrics": metrics})
    except Exception as e:
        # Exception handling 
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
