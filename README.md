![Build and Push](https://github.com/bagewadiarti-hub/k8s-myapp/actions/workflows/deploy.yaml/badge.svg)

# Kubernetes Multi-Tier Application

A production-ready multi-tier application deployed on Kubernetes, demonstrating
core DevOps and cloud-native engineering concepts.

## Architecture
```
Internet → Ingress (nginx) → Frontend (nginx)
                           → Backend (Python/Flask) → PostgreSQL
```

## Tech stack

- **Kubernetes** — container orchestration (Docker Desktop)
- **Helm** — package manager, multi-environment deployments
- **GitHub Actions** — CI/CD pipeline, automated Docker builds
- **Docker Hub** — container image registry
- **Python/Flask** — backend API
- **PostgreSQL** — persistent database with PVC
- **nginx** — frontend web server + Ingress controller

## Kubernetes concepts demonstrated

- Deployments + ReplicaSets with rolling updates
- StatefulSets with PersistentVolumes for database
- Services — ClusterIP, NodePort, LoadBalancer
- Ingress with path-based routing
- ConfigMaps + Secrets for configuration management
- RBAC — ServiceAccounts with least privilege
- Resource limits and health checks (liveness/readiness probes)

## Project structure
```
k8s-myapp/
  app.py                        # Flask backend application
  Dockerfile                    # Container image definition
  myapp/                        # Helm chart
    Chart.yaml                  # Chart metadata
    values.yaml                 # Default configuration values
    templates/                  # Kubernetes manifests
      backend.yaml              # Backend deployment + service
      frontend.yaml             # Frontend deployment + service + configmap
      postgres.yaml             # Database deployment + service
      secret.yaml               # Database credentials
      ingress.yaml              # Ingress routing rules
  .github/workflows/
    deploy.yaml                 # CI/CD pipeline
  docs/
    architecture.md             # Detailed architecture notes
```

## CI/CD pipeline

Every push to `main` automatically:
1. Builds a Docker image from `Dockerfile`
2. Pushes to Docker Hub with two tags — `latest` and the git SHA
3. Image is versioned and reproducible from any commit
```
git push → GitHub Actions → docker build → artibagewadi/myapp-backend:latest
```

## How to run locally

### Prerequisites
- Docker Desktop with Kubernetes enabled
- Helm v3
- kubectl

### Deploy with Helm
```bash
# Clone the repo
git clone https://github.com/bagewadiarti-hub/k8s-myapp.git
cd k8s-myapp

# Install nginx ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml

# Deploy the app
helm install myapp ./myapp

# Add to hosts file (Windows)
# Add: 127.0.0.1 myapp.local to C:\Windows\System32\drivers\etc\hosts

# Port-forward ingress
kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80

# Test
curl -H "Host: myapp.local" http://localhost:8080/
curl -H "Host: myapp.local" http://localhost:8080/api
```

### Deploy staging environment
```bash
helm install myapp-staging ./myapp \
  --set backend.message="hello from staging" \
  --set frontend.replicas=1 \
  --set ingress.host=staging.local
```

## Key learnings

- Stateful apps require StatefulSets + PVCs — not regular Deployments
- Services use label selectors, not pod names — labels are everything
- Helm templates with `{{ .Release.Name }}` prefix prevent multi-release conflicts
- RBAC least privilege — ServiceAccounts should only have the permissions they need
- ClusterIP addresses are not reachable from outside the cluster — use port-forward for local testing