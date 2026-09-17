
Troubleshooting Notes

This document records significant troubleshooting scenarios encountered while building and validating the project.

Ingress 503
Symptom

The application initially returned HTTP 503 through the Ingress.

Investigation

The troubleshooting process checked:

kubectl get ingress -n ecommerce
kubectl get svc -n ecommerce
kubectl get endpoints -n ecommerce
kubectl get pods -n ecommerce

Selectors, labels, target ports, Service configuration, and backend readiness were inspected.

Result

Ingress routing was corrected and frontend/backend traffic was successfully verified.

CrashLoopBackOff

Pod logs and descriptions were used to distinguish application, dependency, configuration, image, and probe-related failures.

Useful commands:

kubectl logs <pod> -n ecommerce
kubectl describe pod <pod> -n ecommerce
kubectl exec -it <pod> -n ecommerce -- sh
ImagePullBackOff

The project uses locally built Minikube images for the application workloads.

Backend:

ecommerce-backend:1.3

Frontend:

ecommerce-frontend:1.3

The local application deployments use imagePullPolicy: Never.

HPA and PromQL Troubleshooting

CPU and memory metrics were inspected directly because the available metric labels differ by environment.

The final working queries use metrics available in the project environment, including:

container_cpu_usage_seconds_total
container_memory_working_set_bytes

The HPA was tested under generated load and reached up to five backend replicas before scaling back toward the minimum.

Grafana Probe Failures

Grafana entered CrashLoopBackOff during setup.

The investigation showed probe failures while Grafana sidecar components were still loading.

The relevant Grafana sidecar probes were disabled through Helm configuration. The replacement Grafana pod subsequently became healthy and the dashboard was verified.

Grafana persistence was later enabled with a 5Gi PVC.

MySQL Security Context Compatibility

Applying an aggressive application-style security context to the official MySQL image caused initialization to fail with:

setgid: Operation not permitted

The project therefore keeps the stronger security configuration on the application containers while leaving MySQL with a compatible configuration.

Minikube Restart and Context Recovery

A Minikube stop/restart caused the active kubectl context to become unavailable.

The recovery process involved restarting Minikube and restoring the minikube context.

Persistent claims remained intact after the restart.

Verification:

minikube status
kubectl config current-context
kubectl cluster-info
PVC Troubleshooting

Persistent storage was checked using:

kubectl get pvc -n ecommerce
kubectl describe pvc <pvc-name> -n ecommerce
kubectl get storageclass

Important checks included:

PVC status
StorageClass
access mode
provisioner
events
volume mounts

The MySQL data remained available after StatefulSet recreation.

Backup Troubleshooting

The backup CronJob initially produced some transient failed pods while later Jobs completed successfully.

The backup process was verified at the Job level rather than relying only on individual pod status.

The final backup implementation:

Uses mysqldump
Uses --single-transaction
Uses --routines
Uses --triggers
Uses --no-tablespaces
Writes to the persistent backup PVC
Verifies the output file is non-empty
Uses a temporary MySQL client option file instead of passing the database password through the command line

A manual test Job completed successfully and produced a 2.0K SQL backup file.

Helm Validation

The Helm chart was repeatedly checked using:

helm lint helm/ecommerce
helm template ecommerce helm/ecommerce

The final chart:

Helm lint: 0 failures
Helm render: successful

The final Helm release reached Revision 3 with status deployed.

Secret Cleanup

Before GitHub publication:

The plaintext Secret manifest was removed.
The Helm Secret template was removed.
A safe Secret example was added.
The backend password fallback was removed.
.gitignore rules were added.
The live Kubernetes Secret was preserved.
The Helm release was upgraded.
The final Helm manifest was confirmed to contain no Secret resource.
