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
| VM (staging) | _pending_ | Central India | |
| VM (production) | _pending_ | Central India | |
| Entra ID app registration | _pending_ | — | |

Fill these into the GitHub repo's Actions variables per [README.md](README.md) once everything is created.
