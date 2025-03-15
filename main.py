import time
import requests
from prometheus_client import Gauge, start_http_server

tfl_line_status = Gauge('tfl_line_status', 'TFL line status severity level', ['line', 'mode', 'status'])

def update_metrics():
    url = "https://api.tfl.gov.uk/Line/Mode/elizabeth-line,dlr,tube/Status"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to fetch data")
            return
        for line in response.json():
            for status in line["lineStatuses"]:
                tfl_line_status.labels(line=line["name"], mode=line["modeName"], status=status["statusSeverityDescription"]).set(status["statusSeverity"])
    except Exception as e:
        print(f"Error updating metrics: {e}")

if __name__ == "__main__":
    start_http_server(8000)
    print("Prometheus exporter running on port 8000")
    while True:
        update_metrics()
        time.sleep(60)
