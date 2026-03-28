def read_logs(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()
    return logs

def main():
    file_path = "logs/sample.log"
    logs = read_logs(file_path)

    for log in logs:
        print(log.strip())

if __name__ == "__main__":
    main()