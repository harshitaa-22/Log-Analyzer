import re
from collections import defaultdict

def read_logs(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def parse_log(log):
    pattern = r'(\d+\.\d+\.\d+\.\d+).*"(\w+) (.*?) HTTP.*" (\d{3})'
    match = re.search(pattern, log)

    if match:
        return {
            "ip" : match.group(1),
            "method" : match.group(2),
            "endpoint" : match.group(3),
            "status" : match.group(4)
        }
    return None

def main():
    file_path = "logs/sample.log"
    logs = read_logs(file_path)

    ip_count = defaultdict(int)
    failed_attempts = defaultdict(int)

    for log in logs:
        parsed = parse_log(log)
        if parsed:
            ip = parsed["ip"]
            status = parsed["status"]

            ip_count[ip] += 1

            if status in ["401","403"]:
                failed_attempts[ip] += 1
        
    print("\nIP Request Count:")
    for ip, count in ip_count.items():
        print(ip, "→", count)

    print("\nFailed Attempts:")
    for ip, count in failed_attempts.items():
        print(ip, "→", count)

    print("\nSuspicious IPs:")

    for ip in ip_count:
        if ip_count[ip] > 2 or failed_attempts[ip] > 1:
            print(ip)

if __name__ == "__main__":
    main()