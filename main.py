import json
import yaml
import requests
import time
from collections import defaultdict
import re

# Function to load endpoints with request information from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    try:
        url = endpoint['url']
        method = endpoint.get('method')
        headers = endpoint.get('headers')
        body = endpoint.get('body')
        response = requests.request(method, url, headers=headers, json=body)
        if 200 <= response.status_code < 300:
            if (response.elapsed.total_seconds() <= .5):
                print(f"Endpoint {url} is UP with status code: {response.status_code} and response time: {response.elapsed.total_seconds()} seconds")
                return "UP"
        else:
            print(f"Endpoint {url} is DOWN with status code: {response.status_code}")
            return "DOWN"
    except requests.RequestException:
        print(f"Endpoint {url} is DOWN with exception")
        return "DOWN"
    
def validate_endpoint(endpoint):
    required_keys = ['url', 'method']
    for key in required_keys:
        if key not in endpoint:
            print(f"Missing required key: {key}")
            if key == 'url':
                print("URL is required for health check")
            elif key == 'method':
                print("Method is required for health check, setting to default GET")
                endpoint['method'] = 'GET'
    if endpoint['method'].upper() not in ['GET', 'POST', 'PUT', 'DELETE']:
        print(f"Unsupported method: {endpoint['method']}")
    elif endpoint['method'].upper() == 'POST':
        if 'headers' not in endpoint and 'body' in endpoint:
            print("Headers are missing but body is present, setting to default JSON-encoded body")
            endpoint['headers'] = {'content-type': 'application/json'}
        if 'body' in endpoint and 'content-type' in endpoint['headers']:
            if endpoint['headers']['content-type'] != 'application/json':
                print("Content-Type is not application/json")
            elif not isinstance(endpoint.get('body'), dict):
                print("Body is not a valid JSON object")
                if type(endpoint['body']) is str:
                    print("Body is a string, attempting to parse as JSON object")
                    try:
                        endpoint['body'] = json.loads(endpoint['body'])
                        print("Parsed body: ", endpoint['body'])
                    except:
                        print(f"Failed to parse body: {endpoint['body']}")
    return endpoint

# Main function to monitor endpoints every 15 seconds
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            endpoint=validate_endpoint(endpoint)
            if endpoint is None:
                continue
            result = check_health(endpoint)
            domain=endpoint["url"].split("//")[-1].split("/")[0]
            if ":" in domain:
                domain = re.sub(r':\d*', '', domain)
            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")