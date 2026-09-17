
Deployment
Prerequisites

The project was developed and tested locally using:

Docker
Minikube
kubectl
Helm

The cluster also requires the storage, ingress, and metrics capabilities used by the project.

Project Namespace

Application resources use:

ecommerce
Build Application Images

Backend:

minikube image build -t ecommerce-backend:1.3 ./backend

The frontend image used by the current project is:

ecommerce-frontend:1.3
Validate Helm
helm lint helm/ecommerce

Render the chart:

helm template ecommerce helm/ecommerce
Install or Upgrade
helm upgrade --install ecommerce helm/ecommerce \
  -n ecommerce \
  --create-namespace \
  --take-ownership \
  --wait \
  --timeout 10m
Verify the Release
helm status ecommerce -n ecommerce
helm history ecommerce -n ecommerce
Verify Workloads
kubectl get pods -n ecommerce
kubectl get svc -n ecommerce
kubectl get deployments -n ecommerce
kubectl get statefulsets -n ecommerce
kubectl get hpa -n ecommerce
kubectl get pvc -n ecommerce
kubectl get ingress -n ecommerce
kubectl get cronjobs -n ecommerce
kubectl get servicemonitor -n ecommerce
Application Verification

Backend health:

kubectl run backend-health-test \
  -n ecommerce \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl:8.10.1 \
  -- curl -sS http://backend/health

Backend products:

kubectl run backend-products-test \
  -n ecommerce \
  --rm -it \
  --restart=Never \
  --image=curlimages/curl:8.10.1 \
  -- curl -sS http://backend/api/products
Persistent Storage

Do not delete these existing claims during normal project upgrades:

mysql-pvc
mysql-backup-pvc
Secrets

Real database credentials are intentionally excluded from the repository.

Create a local Secret using values appropriate for the local environment instead of committing credentials.

The repository includes:

config/db-secret.example.yaml

with placeholders only.

Current Helm Release

The documented local environment reached:

Release: ecommerce
Namespace: ecommerce
Revision: 3
Status: deployed
