# Azure resources (actual values)

Created under subscription **Azure for Students** (`f2e48da5-dde8-4a85-b575-0293004c2a9b`).

Note: this subscription has a Microsoft-managed "Allowed resource deployment regions" policy that
restricts where resources can be created, and a separate VM-capacity restriction on top of that.
The only region that satisfied both for VM creation was **Central India** — see README for why
ACR didn't need to move with it.

| Resource | Name | Region | Notes |
|---|---|---|---|
| Resource group | `devsecops-rg` | Central India | (created before region constraint was known; region itself doesn't matter for a resource group) |
| VNet | `devsecops-vnet` | Central India | 10.0.0.0/16 |
| Subnet (staging) | `staging` | — | 10.0.2.0/24, default outbound enabled |
| Subnet (production) | `production` | — | 10.0.1.0/24, default outbound enabled |
| Container registry | `devsecopspipelineacr` | Southeast Asia | Basic SKU — `devsecopspipelineacr.azurecr.io` (region mismatch is fine, no VNet dependency) |
| VM (staging) | `vm-staging` | Central India | Standard_B2ts_v2 (2 vcpu, 1 GiB) — US$8.18/mo if left running, SSH key `vm-staging_key.pem` |
| VM (production) | `vm-production` | Central India | Standard_B2ts_v2 (2 vcpu, 1 GiB) — US$8.18/mo if left running, SSH key `vm-production_key.pem` |
| Entra ID app registration | `github-actions-devsecops-pipeline` | — | 3 federated credentials (branch `main`, env `staging`, env `production`); AcrPush + Virtual Machine Contributor role assignments |
| Log Analytics workspace | `devsecops-law` | Southeast Asia | free tier (5 GB/day, 31-day retention) |
| Action group | `devsecops-alerts` | Global | email notification to account owner |
| Alert rule | `vm-staging-high-cpu` | — | Percentage CPU > 80, severity Warning, $0.10/month |
| Defender for Containers | — | — | enabled on the subscription, scans images pushed to ACR, $6.87/vcore/month (negligible without AKS) |

**B-series note:** classic B1s/B1ls and A1_v2 are blocked on this subscription (capacity, not region) —
`Standard_B2ts_v2` is the cheapest size that's actually deployable here.

**Action group region note:** action groups hit the same "Allowed resource deployment regions" policy as
VMs. Selecting region **Global** (not a specific Azure region) sidesteps it since action groups are a
non-regional resource.

**Resource provider gotcha:** alert rule creation failed with "service principal for the Alerts resource
provider has been revoked" even though `microsoft.insights` showed as Registered. Fix: Subscriptions →
(subscription) → Resource providers → select `microsoft.insights` → Re-register.

**Cost discipline:** stop (deallocate) both VMs between work sessions — compute only bills while running.

Fill these into the GitHub repo's Actions variables per [README.md](README.md) once everything is created.

## First real pipeline run: three bugs, three fixes

Pushing a real commit to `main` surfaced three genuine issues that only show up with a live run
(the architecture was sound, but these details weren't visible until things actually ran):

1. **OIDC subject broke on repo rename.** Renaming the GitHub repo (`devsecops-aws-pipeline` →
   `devsecops-azure-pipeline`) changed the subject claim GitHub's OIDC token presents
   (`repo:<org>/<org-id>/<repo-name>@<repo-id>:ref:...`), so all three federated credentials in
   Entra ID stopped matching and `azure/login` failed with `AADSTS70021`. Fix: edit each federated
   credential's Repository field to the new name (Azure recomputes the subject identifier; the
   credential itself doesn't need deleting/recreating).
2. **`az acr build` needs more than `AcrPush`.** `AcrPush` only grants the ACR *data-plane*
   pull/push actions — not the ARM *control-plane* `registries/read` needed to resolve the
   registry, nor `listBuildSourceUploadUrl`/`scheduleRun` needed by ACR Tasks. Adding `Reader` and
   then `Contributor` (both scoped to just the ACR resource) got past each error in turn.
3. **ACR Tasks isn't permitted on Azure for Students at all.** Even with full `Contributor`, the
   build failed with `TasksOperationsNotAllowed` — this subscription tier blocks the managed-build
   feature outright, independent of RBAC. The real fix was to stop using `az acr build` and instead
   `docker build` on the GitHub Actions runner itself, then `docker push` after `az acr login`.
   This is arguably the more standard pattern for a CI runner anyway.

After these three fixes, the pipeline ran clean end-to-end: scan → build/push → deploy staging →
manual approval → deploy production, total ~4m30s.
