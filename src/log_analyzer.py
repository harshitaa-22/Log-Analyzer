import json
import re
from collections import defaultdict

REQUEST_THRESHOLD = 2
FAILED_THRESHOLD = 1


def read_logs(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()


def parse_log(log):
    pattern = r'(\d+\.\d+\.\d+\.\d+).*"(\w+) (.*?) HTTP.*" (\d{3})'
    match = re.search(pattern, log)

    if match:
        return {
            "ip": match.group(1),
            "method": match.group(2),
            "endpoint": match.group(3),
            "status": match.group(4)
        }
    return None


def analyze_logs(logs):
    ip_count = defaultdict(int)
    failed_attempts = defaultdict(int)

    for log in logs:
        if not log.strip():
            continue

        parsed = parse_log(log)
        if parsed:
            ip = parsed["ip"]
            status = parsed["status"]

            ip_count[ip] += 1

            if status in ["401", "403"]:
                failed_attempts[ip] += 1

    return ip_count, failed_attempts


def detect_suspicious(ip_count, failed_attempts):
    suspicious_ips = []

    for ip in ip_count:
        if ip_count[ip] > REQUEST_THRESHOLD or failed_attempts[ip] > FAILED_THRESHOLD:
            suspicious_ips.append(ip)

    return suspicious_ips


def generate_report(logs, ip_count, failed_attempts, suspicious_ips):
    return {
        "total_requests": len(logs),
        "ip_counts": dict(ip_count),
        "failed_attempts": dict(failed_attempts),
        "suspicious_ips": suspicious_ips
    }