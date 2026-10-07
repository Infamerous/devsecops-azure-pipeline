# Azure resources (actual values)

Created under subscription **Azure for Students** (`f2e48da5-dde8-4a85-b575-0293004c2a9b`), region **Southeast Asia**.

| Resource | Name | Notes |
|---|---|---|
| Resource group | `devsecops-rg` | |
| VNet | `devsecops-vnet` | 10.0.0.0/16 |
| Subnet (staging) | `staging` | 10.0.1.0/24, default outbound enabled |
| Subnet (production) | `production` | 10.0.2.0/24, default outbound enabled |
| Container registry | `devsecopspipelineacr` | Basic SKU — `devsecopspipelineacr.azurecr.io` |
| VM (staging) | _pending_ | |
| VM (production) | _pending_ | |
| Entra ID app registration | _pending_ | |

Fill these into the GitHub repo's Actions variables per [README.md](README.md) once everything is created.
