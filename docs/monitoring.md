
Monitoring and Observability
Components

The project uses:

Prometheus
Grafana
kube-prometheus-stack
Kubernetes ServiceMonitor

The monitoring stack is deployed in the monitoring namespace.

Application Metrics

The Flask backend exposes:

/metrics

Custom metrics:

http_requests_total
http_request_duration_seconds
ServiceMonitor

The ServiceMonitor is:

backend-servicemonitor

Configuration:

Setting	Value
Namespace	ecommerce
Port	http
Path	/metrics
Interval	15s
Scrape timeout	10s
PromQL
Backend target availability
up{job="backend"}
Request rate
sum by (exported_endpoint) (
  rate(http_requests_total{job="backend"}[5m])
)
Average request latency
(
  sum by (exported_endpoint) (
    rate(http_request_duration_seconds_sum{job="backend"}[5m])
  )
  /
  sum by (exported_endpoint) (
    rate(http_request_duration_seconds_count{job="backend"}[5m])
  )
) * 1000
Error rate
(
  sum(rate(http_requests_total{job="backend",http_status=~"4..|5.."}[5m]))
  /
  sum(rate(http_requests_total{job="backend"}[5m]))
) * 100
Backend CPU
sum by (pod) (
  rate(container_cpu_usage_seconds_total{
    namespace="ecommerce",
    pod=~"backend-.*",
    cpu="total"
  }[5m])
)
Backend memory
sum by (pod) (
  container_memory_working_set_bytes{
    namespace="ecommerce",
    pod=~"backend-.*"
  }
)
HPA replica count
kube_deployment_status_replicas_available{
  namespace="ecommerce",
  deployment="backend"
}
Grafana Dashboard

Dashboard:

E-Commerce Application Monitoring

Panels:

#	Panel
1	Backend Targets UP
2	Request Rate by Endpoint
3	Average Request Latency
4	Backend Error Rate
5	Backend CPU Usage
6	Backend Memory Usage
7	HPA Replica Count

Grafana persistence was configured with a 5Gi PVC using the standard StorageClass and ReadWriteOnce access mode.

Local Access

The tested local port-forward was:

kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
