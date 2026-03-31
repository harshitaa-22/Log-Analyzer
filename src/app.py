from flask import Flask, request, jsonify
from log_analyzer import read_logs, analyze_logs, detect_suspicious, generate_report

app = Flask(__name__)


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("logfile")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    logs = file.read().decode("utf-8").splitlines()

    ip_count, failed_attempts = analyze_logs(logs)
    suspicious_ips = detect_suspicious(ip_count, failed_attempts)
    report = generate_report(logs, ip_count, failed_attempts, suspicious_ips)

    return jsonify(report)


if __name__ == "__main__":
    app.run(debug=True)