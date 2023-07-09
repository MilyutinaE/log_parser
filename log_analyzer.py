import os
import json
import argparse
from collections import defaultdict
from datetime import datetime


def parse_log_file(log_file_path):
    stats = {
        "total_requests": 0,
        "http_methods": defaultdict(int),
        "top_ips": defaultdict(int),
        "top_requests": []
    }

    with open(log_file_path, "r") as log_file:
        for line in log_file:
            log_entry = parse_log_entry(line)
            if log_entry:
                stats["total_requests"] += 1
                stats["http_methods"][log_entry["method"]] += 1
                stats["top_ips"][log_entry["ip"]] += 1
                stats["top_requests"].append(log_entry)

    return stats


def parse_log_entry(log_entry_str):
    log_entry_parts = log_entry_str.split(" ")
    if len(log_entry_parts) < 10:
        return None

    log_entry = {
        "ip": log_entry_parts[0],
        "date_time": parse_date_time(log_entry_parts[3][1:] + " " + log_entry_parts[4][:-1]),
        "method": log_entry_parts[5][1:],
        "url": log_entry_parts[6][1:],
        "duration": int(log_entry_parts[-1])
    }

    return log_entry


def parse_date_time(date_time_str):
    timestamp_str = datetime.strptime(date_time_str, "%d/%b/%Y:%H:%M:%S %z")
    timestamp = datetime.strftime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return timestamp


def get_top_items(item_dict, count):
    return sorted(item_dict.items(), key=lambda x: x[1], reverse=True)[:count]


def save_stats_to_json(stats, output_file):
    with open(output_file, "w") as json_file:
        json.dump(stats, json_file, indent=4)


def print_stats(stats):
    print("Total requests:", stats["total_requests"])
    print("HTTP methods:")
    for method, count in stats["http_methods"].items():
        print(f"{method}: {count}")
    print("Top IP addresses:")
    for ip, count in get_top_items(stats["top_ips"], 3):
        print(f"{ip}: {count}")
    print("Top requests:")
    for request in stats["top_requests"][:3]:
        print(f"Method: {request['method']}, URL: {request['url']}, IP: {request['ip']}, "
              f"Duration: {request['duration']} ms, "
              f"Date and Time: {request['date_time']}")


def analyze_log(log_path, output_file):
    if os.path.isfile(log_path):
        stats = parse_log_file(log_path)
        save_stats_to_json(stats, output_file)
        print_stats(stats)
    elif os.path.isdir(log_path):
        for file_name in os.listdir(log_path):
            file_path = os.path.join(log_path, file_name)
            if os.path.isfile(file_path):
                stats = parse_log_file(file_path)
                save_stats_to_json(stats, output_file)
                print_stats(stats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze access.log files")
    parser.add_argument("log_path", help="Path to the log file or directory")
    parser.add_argument("-o", "--output", help="Output file path (default: stats.json)", default="stats.json")
    args = parser.parse_args()

    analyze_log(args.log_path, args.output)
