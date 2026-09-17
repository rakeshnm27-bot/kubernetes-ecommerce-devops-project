# Architecture

## Application Flow

```text
User
 |
 v
Kubernetes Ingress
 |
 +----------------------+
 |                      |
 v                      v
Frontend Service     Backend Service
 |                      |
 v                      v
Frontend Pods        Backend Pods
                         |
                         v
                    MySQL Service
                         |
                         v
                  MySQL StatefulSet
                         |
                         v
                      mysql-pvc
                         |
                         v
                 Persistent Storage
Monitoring Flow
Backend /metrics
       |
       v
ServiceMonitor
       |
       v
Prometheus
       |
       v
Grafana
Backup Flow
MySQL Database
       |
       v
Backup Job / CronJob
       |
       v
mysqldump
       |
       v
mysql-backup-pvc
Workload Design
Component	Kubernetes Resource	Purpose
Frontend	Deployment	Stateless web frontend
Backend	Deployment	Stateless Flask API
MySQL	StatefulSet	Stateful database workload
Frontend	ClusterIP Service	Stable internal frontend endpoint
Backend	ClusterIP Service	Stable internal backend endpoint
MySQL	Headless Service	StatefulSet service identity
Application entry point	Ingress	HTTP routing
Backend autoscaling	HPA	CPU-based scaling
Database backup	CronJob	Scheduled MySQL backups
Storage
Storage	Purpose	Capacity
mysql-pvc	MySQL data	1Gi
mysql-backup-pvc	SQL backups	1Gi
Grafana PVC	Grafana state	5Gi

The existing MySQL and backup PVCs are reused by Helm rather than recreated.

Security

Application containers are hardened with non-root execution, disabled privilege escalation, and dropped Linux capabilities.

The backend runs with UID/GID 1000. The frontend runs as a non-root Nginx container.

The MySQL official image uses a compatible runtime configuration because applying the same restrictive application-container security context caused initialization to fail with setgid: Operation not permitted.

Monitoring

The backend exposes /metrics.

Prometheus discovers the backend through a ServiceMonitor named backend-servicemonitor.

Grafana visualizes application traffic, latency, errors, resource usage, and HPA replica count.
