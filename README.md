# DevSecOps Azure Pipeline

A small CI/CD security pipeline for the IUP CS midterm (data center deployment exploration, Azure free account).

GitHub Actions scans and builds the app, pushes the image to Azure Container Registry (ACR), Microsoft Defender
for Containers scans it for CVEs, and the pipeline deploys to a Staging VM, then waits for manual approval
before deploying to Production. A Telegram bot running on the Production VM polls GitHub for pipeline status
and can approve/rollback deployments from a phone.

## Repo setup (GitHub side)

Settings → Secrets and variables → Actions → **Variables** (not secrets — these aren't sensitive since auth is OIDC):

| Variable | Example | Notes |
|---|---|---|
| `AZURE_CLIENT_ID` | `00000000-...` | App registration (client) ID |
| `AZURE_TENANT_ID` | `00000000-...` | Entra ID tenant ID |
| `AZURE_SUBSCRIPTION_ID` | `00000000-...` | Azure subscription ID |
| `RESOURCE_GROUP` | `devsecops-rg` | resource group everything lives in |
| `ACR_NAME` | `devsecopsacr` | ACR registry name (no dots/dashes) |
| `IMAGE_NAME` | `devsecops-app` | image repository name inside ACR |
| `STAGING_VM_NAME` | `vm-staging` | Staging VM |
| `PRODUCTION_VM_NAME` | `vm-production` | Production VM |

Settings → Environments → create `staging` and `production`. On `production`, add a **required reviewer** —
that's the manual approval gate.

## Azure setup checklist

- [x] Resource group
- [x] VNet with 2 subnets (staging / production)
- [x] 2x Azure VMs (`Standard_B2ts_v2`), Docker installed, **system-assigned managed identity** with `AcrPull` role on the ACR
- [x] Azure Container Registry (Basic SKU)
- [x] Microsoft Defender for Cloud → Defender for Containers plan enabled on the subscription (scans images pushed to ACR)
- [x] Entra ID App Registration for GitHub Actions, with a **federated credential** trusting `token.actions.githubusercontent.com` for this repo, scoped via role assignment (`AcrPush` on the ACR, `Virtual Machine Contributor` on the resource group)
- [x] Azure Monitor: Log Analytics workspace (`devsecops-law`) + built-in VM availability monitoring + one alert rule (`vm-staging-high-cpu`, CPU > 80%)
- [x] Budget alert (done, $1 threshold)

**Cost note:** VMs are stopped (deallocated) between testing sessions to avoid compute charges — only
start them when actively demoing or capturing screenshots.

## Local dev

```bash
pip install -r requirements.txt
python app.py
```

## Deploy

Push to `main`. The pipeline runs automatically: scan → build → push to ACR → Defender for Containers scan
(automatic on push) → deploy staging → **manual approval** → deploy production.
