import re

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

    for log in logs:
        parsed = parse_log(log)
        if parsed:
            print(parsed)

if __name__ == "__main__":
    main()