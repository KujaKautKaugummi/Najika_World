"""
Performance Monitoring Module
Monitors system performance, API response times, and resource usage
"""

import time
import psutil
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from collections import deque, defaultdict
from dataclasses import dataclass, asdict
from functools import wraps


logger = logging.getLogger(__name__)


@dataclass
class APIMetrics:
    """API endpoint metrics"""
    endpoint: str
    method: str
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    avg_response_time: float = 0.0
    p95_response_time: float = 0.0
    p99_response_time: float = 0.0
    error_rate: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class SystemMetrics:
    """System resource metrics"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_percent: float
    disk_used_gb: float
    disk_free_gb: float
    network_sent_mb: float
    network_recv_mb: float
    process_count: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class PerformanceAlert:
    """Performance alert"""
    alert_id: str
    alert_type: str
    severity: str
    message: str
    timestamp: float
    metric_name: str
    metric_value: float
    threshold: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class PerformanceMonitor:
    """
    Performance monitoring system
    """

    def __init__(
        self,
        api_history_size: int = 1000,
        system_history_size: int = 1000,
        alert_threshold_cpu: float = 80.0,
        alert_threshold_memory: float = 85.0,
        alert_threshold_disk: float = 90.0,
        alert_threshold_response_time: float = 1.0
    ):
        """
        Initialize performance monitor

        Args:
            api_history_size: Size of API request history
            system_history_size: Size of system metrics history
            alert_threshold_cpu: CPU usage alert threshold (%)
            alert_threshold_memory: Memory usage alert threshold (%)
            alert_threshold_disk: Disk usage alert threshold (%)
            alert_threshold_response_time: Response time alert threshold (seconds)
        """
        # API metrics
        self.api_metrics: Dict[str, APIMetrics] = {}
        self.api_request_history: deque = deque(maxlen=api_history_size)
        self.response_times: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))

        # System metrics
        self.system_metrics_history: deque = deque(maxlen=system_history_size)
        self.last_network_io = psutil.net_io_counters()

        # Alerts
        self.alerts: List[PerformanceAlert] = []
        self.alert_threshold_cpu = alert_threshold_cpu
        self.alert_threshold_memory = alert_threshold_memory
        self.alert_threshold_disk = alert_threshold_disk
        self.alert_threshold_response_time = alert_threshold_response_time

        # Monitoring state
        self.monitoring_enabled = True
        self.start_time = time.time()

    # ============================================================================
    # API MONITORING
    # ============================================================================

    def track_api_request(
        self,
        endpoint: str,
        method: str,
        response_time: float,
        status_code: int
    ):
        """
        Track API request

        Args:
            endpoint: API endpoint
            method: HTTP method
            response_time: Response time in seconds
            status_code: HTTP status code
        """
        if not self.monitoring_enabled:
            return

        # Get or create metrics
        metrics_key = f"{method}:{endpoint}"
        if metrics_key not in self.api_metrics:
            self.api_metrics[metrics_key] = APIMetrics(
                endpoint=endpoint,
                method=method
            )

        metrics = self.api_metrics[metrics_key]

        # Update metrics
        metrics.total_requests += 1

        if 200 <= status_code < 400:
            metrics.successful_requests += 1
        else:
            metrics.failed_requests += 1

        metrics.total_response_time += response_time
        metrics.min_response_time = min(metrics.min_response_time, response_time)
        metrics.max_response_time = max(metrics.max_response_time, response_time)
        metrics.avg_response_time = metrics.total_response_time / metrics.total_requests

        # Store response time for percentile calculation
        self.response_times[metrics_key].append(response_time)

        # Calculate percentiles
        if len(self.response_times[metrics_key]) >= 10:
            sorted_times = sorted(self.response_times[metrics_key])
            p95_index = int(len(sorted_times) * 0.95)
            p99_index = int(len(sorted_times) * 0.99)
            metrics.p95_response_time = sorted_times[p95_index]
            metrics.p99_response_time = sorted_times[p99_index]

        # Calculate error rate
        metrics.error_rate = (metrics.failed_requests / metrics.total_requests) * 100

        # Store in history
        self.api_request_history.append({
            'endpoint': endpoint,
            'method': method,
            'response_time': response_time,
            'status_code': status_code,
            'timestamp': time.time()
        })

        # Check for alerts
        if response_time > self.alert_threshold_response_time:
            self.create_alert(
                'slow_response',
                'warning',
                f"Slow response time for {method} {endpoint}",
                'response_time',
                response_time,
                self.alert_threshold_response_time
            )

    def get_api_metrics(
        self,
        endpoint: Optional[str] = None,
        method: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get API metrics

        Args:
            endpoint: Filter by endpoint
            method: Filter by method

        Returns:
            List of API metrics
        """
        metrics_list = []

        for key, metrics in self.api_metrics.items():
            if endpoint and metrics.endpoint != endpoint:
                continue
            if method and metrics.method != method:
                continue

            metrics_list.append(metrics.to_dict())

        return metrics_list

    def get_slowest_endpoints(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get slowest API endpoints

        Args:
            limit: Number of endpoints to return

        Returns:
            List of slowest endpoints
        """
        metrics_list = [m.to_dict() for m in self.api_metrics.values()]
        metrics_list.sort(key=lambda x: x['avg_response_time'], reverse=True)
        return metrics_list[:limit]

    def get_most_used_endpoints(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most used API endpoints

        Args:
            limit: Number of endpoints to return

        Returns:
            List of most used endpoints
        """
        metrics_list = [m.to_dict() for m in self.api_metrics.values()]
        metrics_list.sort(key=lambda x: x['total_requests'], reverse=True)
        return metrics_list[:limit]

    # ============================================================================
    # SYSTEM MONITORING
    # ============================================================================

    def collect_system_metrics(self) -> SystemMetrics:
        """
        Collect current system metrics

        Returns:
            System metrics
        """
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)

        # Memory
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_mb = memory.used / (1024 * 1024)
        memory_available_mb = memory.available / (1024 * 1024)

        # Disk
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024 * 1024 * 1024)
        disk_free_gb = disk.free / (1024 * 1024 * 1024)

        # Network
        network_io = psutil.net_io_counters()
        network_sent_mb = (network_io.bytes_sent - self.last_network_io.bytes_sent) / (1024 * 1024)
        network_recv_mb = (network_io.bytes_recv - self.last_network_io.bytes_recv) / (1024 * 1024)
        self.last_network_io = network_io

        # Processes
        process_count = len(psutil.pids())

        metrics = SystemMetrics(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_used_mb=memory_used_mb,
            memory_available_mb=memory_available_mb,
            disk_percent=disk_percent,
            disk_used_gb=disk_used_gb,
            disk_free_gb=disk_free_gb,
            network_sent_mb=network_sent_mb,
            network_recv_mb=network_recv_mb,
            process_count=process_count
        )

        # Store in history
        self.system_metrics_history.append(metrics)

        # Check for alerts
        self.check_system_alerts(metrics)

        return metrics

    def check_system_alerts(self, metrics: SystemMetrics):
        """
        Check for system alerts

        Args:
            metrics: System metrics
        """
        # CPU alert
        if metrics.cpu_percent > self.alert_threshold_cpu:
            self.create_alert(
                'high_cpu',
                'warning' if metrics.cpu_percent < 95 else 'critical',
                f"High CPU usage: {metrics.cpu_percent:.1f}%",
                'cpu_percent',
                metrics.cpu_percent,
                self.alert_threshold_cpu
            )

        # Memory alert
        if metrics.memory_percent > self.alert_threshold_memory:
            self.create_alert(
                'high_memory',
                'warning' if metrics.memory_percent < 95 else 'critical',
                f"High memory usage: {metrics.memory_percent:.1f}%",
                'memory_percent',
                metrics.memory_percent,
                self.alert_threshold_memory
            )

        # Disk alert
        if metrics.disk_percent > self.alert_threshold_disk:
            self.create_alert(
                'high_disk',
                'warning',
                f"High disk usage: {metrics.disk_percent:.1f}%",
                'disk_percent',
                metrics.disk_percent,
                self.alert_threshold_disk
            )

    def get_system_metrics_history(
        self,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get system metrics history

        Args:
            start_time: Start timestamp
            end_time: End timestamp
            limit: Maximum number of metrics

        Returns:
            List of system metrics
        """
        metrics = list(self.system_metrics_history)

        # Filter by time
        if start_time:
            metrics = [m for m in metrics if m.timestamp >= start_time]
        if end_time:
            metrics = [m for m in metrics if m.timestamp <= end_time]

        # Limit results
        metrics = metrics[-limit:]

        return [m.to_dict() for m in metrics]

    def get_current_system_status(self) -> Dict[str, Any]:
        """
        Get current system status

        Returns:
            System status summary
        """
        latest_metrics = self.collect_system_metrics()

        # Calculate uptime
        uptime = time.time() - self.start_time

        # Determine health status
        health = 'healthy'
        if (latest_metrics.cpu_percent > self.alert_threshold_cpu or
            latest_metrics.memory_percent > self.alert_threshold_memory):
            health = 'degraded'
        if (latest_metrics.cpu_percent > 95 or
            latest_metrics.memory_percent > 95 or
            latest_metrics.disk_percent > self.alert_threshold_disk):
            health = 'critical'

        return {
            'status': health,
            'uptime': uptime,
            'cpu_usage': latest_metrics.cpu_percent,
            'memory_usage': latest_metrics.memory_percent,
            'disk_usage': latest_metrics.disk_percent,
            'active_processes': latest_metrics.process_count,
            'timestamp': latest_metrics.timestamp
        }

    # ============================================================================
    # GPU MONITORING (if available)
    # ============================================================================

    def get_gpu_metrics(self) -> Optional[Dict[str, Any]]:
        """
        Get GPU metrics if available

        Returns:
            GPU metrics or None if not available
        """
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()

            if not gpus:
                return None

            gpu_list = []
            for gpu in gpus:
                gpu_list.append({
                    'id': gpu.id,
                    'name': gpu.name,
                    'utilization': gpu.load * 100,
                    'memory_used': gpu.memoryUsed,
                    'memory_total': gpu.memoryTotal,
                    'memory_percent': (gpu.memoryUsed / gpu.memoryTotal) * 100,
                    'temperature': gpu.temperature
                })

            return {
                'available': True,
                'devices': gpu_list,
                'count': len(gpu_list)
            }

        except ImportError:
            return {'available': False, 'error': 'GPUtil not installed'}
        except Exception as e:
            logger.error(f"Error getting GPU metrics: {e}")
            return {'available': False, 'error': str(e)}

    # ============================================================================
    # ALERTS
    # ============================================================================

    def create_alert(
        self,
        alert_type: str,
        severity: str,
        message: str,
        metric_name: str,
        metric_value: float,
        threshold: float
    ):
        """
        Create performance alert

        Args:
            alert_type: Type of alert
            severity: Severity level
            message: Alert message
            metric_name: Metric name
            metric_value: Current metric value
            threshold: Threshold value
        """
        import uuid

        alert = PerformanceAlert(
            alert_id=str(uuid.uuid4()),
            alert_type=alert_type,
            severity=severity,
            message=message,
            timestamp=time.time(),
            metric_name=metric_name,
            metric_value=metric_value,
            threshold=threshold
        )

        self.alerts.append(alert)

        # Log alert
        log_level = logging.WARNING if severity == 'warning' else logging.CRITICAL
        logger.log(log_level, f"Performance Alert: {message}")

        # Keep only recent alerts (last 100)
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]

    def get_alerts(
        self,
        severity: Optional[str] = None,
        alert_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get performance alerts

        Args:
            severity: Filter by severity
            alert_type: Filter by alert type
            limit: Maximum number of alerts

        Returns:
            List of alerts
        """
        alerts = self.alerts

        # Filter
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        if alert_type:
            alerts = [a for a in alerts if a.alert_type == alert_type]

        # Sort by timestamp (newest first)
        alerts = sorted(alerts, key=lambda a: a.timestamp, reverse=True)

        return [a.to_dict() for a in alerts[:limit]]

    # ============================================================================
    # PERFORMANCE SUMMARY
    # ============================================================================

    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive performance summary

        Returns:
            Performance summary
        """
        # API metrics summary
        total_api_requests = sum(m.total_requests for m in self.api_metrics.values())
        avg_response_time = (
            sum(m.avg_response_time * m.total_requests for m in self.api_metrics.values()) /
            total_api_requests if total_api_requests > 0 else 0
        )
        total_errors = sum(m.failed_requests for m in self.api_metrics.values())
        overall_error_rate = (total_errors / total_api_requests * 100) if total_api_requests > 0 else 0

        # System metrics summary
        latest_system = self.collect_system_metrics()

        return {
            'api': {
                'total_requests': total_api_requests,
                'avg_response_time': avg_response_time,
                'error_rate': overall_error_rate,
                'unique_endpoints': len(self.api_metrics),
                'slowest_endpoints': self.get_slowest_endpoints(5),
                'most_used_endpoints': self.get_most_used_endpoints(5)
            },
            'system': latest_system.to_dict(),
            'alerts': {
                'total': len(self.alerts),
                'critical': len([a for a in self.alerts if a.severity == 'critical']),
                'warning': len([a for a in self.alerts if a.severity == 'warning']),
                'recent': self.get_alerts(limit=5)
            },
            'uptime': time.time() - self.start_time
        }


# ============================================================================
# DECORATORS
# ============================================================================

def monitor_performance(endpoint: str, method: str = 'GET'):
    """
    Decorator to monitor function performance

    Args:
        endpoint: Endpoint name
        method: HTTP method

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            status_code = 200

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status_code = 500
                raise
            finally:
                response_time = time.time() - start_time
                monitor = get_performance_monitor()
                monitor.track_api_request(endpoint, method, response_time, status_code)

        return wrapper
    return decorator


# Global performance monitor instance
_performance_monitor = None


def get_performance_monitor() -> PerformanceMonitor:
    """
    Get global performance monitor instance

    Returns:
        Performance monitor instance
    """
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor
