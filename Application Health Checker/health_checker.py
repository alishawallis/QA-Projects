import urllib.request
import time
from datetime import datetime
import socket

class HealthChecker:
    def __init__(self, url, timeout=10):
        self.url = url
        self.timeout = timeout
        self.start_time = datetime.now()
    
    def check_status(self):
        try:
            response = urllib.request.urlopen(self.url, timeout=self.timeout)
            status_code = response.getcode()
            
            # Calculate uptime
            current_time = datetime.now()
            uptime = current_time - self.start_time
            
            status = {
                'url': self.url,
                'status': 'UP' if 200 <= status_code < 400 else 'DOWN',
                'status_code': status_code,
                'response_time': response.info().get('X-Response-Time', 'N/A'),
                'uptime': str(uptime).split('.')[0],  # Format without microseconds
                'last_checked': current_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except urllib.error.HTTPError as e:
            status = {
                'url': self.url,
                'status': 'DOWN',
                'status_code': e.code,
                'error': str(e),
                'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except (urllib.error.URLError, socket.timeout) as e:
            status = {
                'url': self.url,
                'status': 'DOWN',
                'error': str(e),
                'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        return status

def main():
    # Example URLs to monitor
    urls = [
        'https://www.google.com',
        'https://www.example.com',
        'https://thisurldoesnotexist.com'  # This will fail
    ]
    
    checkers = {url: HealthChecker(url) for url in urls}
    
    try:
        while True:
            print("\n=== Health Check Results ===")
            print("-" * 50)
            
            for url, checker in checkers.items():
                status = checker.check_status()
                
                print(f"\nURL: {status['url']}")
                print(f"Status: {status['status']}")
                
                if 'status_code' in status:
                    print(f"Status Code: {status['status_code']}")
                if 'uptime' in status:
                    print(f"Uptime: {status['uptime']}")
                if 'error' in status:
                    print(f"Error: {status['error']}")
                    
                print(f"Last Checked: {status['last_checked']}")
                print("-" * 50)
            
            # Wait for 60 seconds before next check
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")

if __name__ == "__main__":
    main()