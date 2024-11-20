import os
import sys
import time
import datetime
import psutil

class SystemMonitor:
    def __init__(self):
        self.thresholds = {
            'cpu': 80.0,  # CPU usage threshold (%)
            'memory': 80.0,  # Memory usage threshold (%)
            'disk': 80.0,  # Disk usage threshold (%)
            'process_count': 100  # Maximum process count
        }
        
    def check_cpu(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        return cpu_percent > self.thresholds['cpu'], cpu_percent
    
    def check_memory(self):
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        return memory_percent > self.thresholds['memory'], memory_percent
    
    def check_disk(self):
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        return disk_percent > self.thresholds['disk'], disk_percent
    
    def check_processes(self):
        process_count = len(psutil.pids())
        return process_count > self.thresholds['process_count'], process_count
    
    def log_alert(self, component, value, threshold):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alert = f"[{timestamp}] ALERT: {component} usage is {value:.1f}% (threshold: {threshold}%)"
        print(alert)
        with open('system_health.log', 'a') as f:
            f.write(alert + '\n')
    
    def monitor(self):
        print(f"Starting system monitoring (Press Ctrl+C to stop)...")
        print(f"Thresholds: CPU {self.thresholds['cpu']}%, Memory {self.thresholds['memory']}%, "
              f"Disk {self.thresholds['disk']}%, Process Count {self.thresholds['process_count']}")
        
        try:
            while True:
                # Check CPU
                cpu_alert, cpu_value = self.check_cpu()
                if cpu_alert:
                    self.log_alert('CPU', cpu_value, self.thresholds['cpu'])
                
                # Check Memory
                mem_alert, mem_value = self.check_memory()
                if mem_alert:
                    self.log_alert('Memory', mem_value, self.thresholds['memory'])
                
                # Check Disk
                disk_alert, disk_value = self.check_disk()
                if disk_alert:
                    self.log_alert('Disk', disk_value, self.thresholds['disk'])
                
                # Check Process Count
                proc_alert, proc_count = self.check_processes()
                if proc_alert:
                    self.log_alert('Process Count', proc_count, self.thresholds['process_count'])
                
                # Print current status
                print(f"\rCPU: {cpu_value:.1f}% | Memory: {mem_value:.1f}% | "
                      f"Disk: {disk_value:.1f}% | Processes: {proc_count}", end='')
                
                time.sleep(5)  # Check every 5 seconds
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.monitor()