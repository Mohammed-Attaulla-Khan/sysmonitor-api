# 🖥️ SysMonitor: OS Cloud Daemon
**Live Demo:** [View SysMonitor on Render](https://sysmonitor-api.onrender.com)

## Overview
SysMonitor is a system-level tracking tool designed to bridge the gap between Operating System hardware and cloud application monitoring. It extracts real-time kernel metrics and serves them via a RESTful endpoint to a dynamic visual dashboard.

## 🚀 Key Features
* **Kernel-Level Extraction:** Leverages the `psutil` library to safely interface with the OS kernel, retrieving real-time data on active process IDs (PIDs), logical CPU cores, and memory allocation.
* **Cloud Infrastructure Monitoring:** Actively monitors the remote Linux (AWS) environment where it is deployed, proving an understanding of remote server diagnostics.
* **Dynamic Visual UI:** Features a dark-mode frontend that executes continuous asynchronous polling (every 2 seconds) to dynamically update CSS progress bars based on server strain.

## 🛠️ Technical Stack
* **Backend Systems:** Python 3, Flask, `psutil`, `platform`
* **Cloud Deployment:** Render (Linux Environment), Gunicorn
* **Frontend Analytics:** HTML/CSS, JavaScript Auto-Polling
