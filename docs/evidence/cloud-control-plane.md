# Google Cloud Control-Plane Evidence

Read-only verification captured on 29 Aug 2026 from project `ai-malaysia` with Google Cloud CLI. No credentials or secret values are included.

## Cloud Run

```yaml
service: canibiz-careloop-agent
region: asia-southeast1
latest_ready_revision: canibiz-careloop-agent-00009-vvz
traffic_percent: 100
service_account: careloop-runtime@ai-malaysia.iam.gserviceaccount.com
max_instances: 3
url: https://canibiz-careloop-agent-kep7hzbbeq-as.a.run.app
```

## Firestore

```yaml
database: projects/ai-malaysia/databases/(default)
location: asia-southeast1
type: FIRESTORE_NATIVE
concurrency_mode: PESSIMISTIC
```

## Reproduce

```powershell
gcloud run services describe canibiz-careloop-agent `
  --project ai-malaysia `
  --region asia-southeast1

gcloud firestore databases describe `
  --project ai-malaysia `
  --database="(default)"
```
