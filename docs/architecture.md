# Architecture notes

## Traffic flow

1. Request hits nginx Ingress controller on port 80
2. Ingress matches Host header `myapp.local`
3. Path `/api` routes to backend-service (ClusterIP)
4. Path `/` routes to frontend-service (ClusterIP)
5. Backend connects to postgres-service via K8s DNS

## DNS resolution inside cluster

Services are reachable by name inside the cluster:
- `postgres-service` resolves to the postgres ClusterIP
- `backend-service` resolves to the backend ClusterIP
- Full DNS: `service-name.namespace.svc.cluster.local`

## Storage

- PostgreSQL uses emptyDir for local development
- In production, replace with a cloud PVC (AWS EBS, Azure Disk)
- PVC lifecycle is independent of pod lifecycle

## Security

- Database credentials stored in Kubernetes Secret
- Backend uses a dedicated ServiceAccount with read-only ClusterRole
- Secrets are base64 encoded — use Sealed Secrets or Vault in production

## Multi-environment strategy

Same Helm chart, different values:
- Production: `helm install myapp ./myapp`
- Staging: `helm install myapp-staging ./myapp --set ingress.host=staging.local`