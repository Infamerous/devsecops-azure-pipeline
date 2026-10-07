# DevSecOps AWS Pipeline

A small CI/CD security pipeline for the IUP CS midterm (data center deployment exploration, AWS free tier).

GitHub Actions scans and builds the app, pushes the image to ECR, Amazon Inspector scans it for CVEs, and the
pipeline deploys to a Staging EC2 instance, then waits for manual approval before deploying to Production.
A Telegram bot running on the Production instance polls GitHub for pipeline status and can approve/rollback
deployments from a phone.

## Repo setup (GitHub side)

Settings → Secrets and variables → Actions → **Variables** (not secrets — these aren't sensitive since auth is OIDC):

| Variable | Example | Notes |
|---|---|---|
| `AWS_REGION` | `us-east-1` | region everything is deployed in |
| `ECR_REPOSITORY` | `devsecops-aws-pipeline` | ECR repo name |
| `AWS_ROLE_ARN` | `arn:aws:iam::<account-id>:role/github-actions-deploy` | the OIDC-trusted role |
| `STAGING_INSTANCE_ID` | `i-0abc...` | Staging EC2 instance |
| `PRODUCTION_INSTANCE_ID` | `i-0def...` | Production EC2 instance |

Settings → Environments → create `staging` and `production`. On `production`, add a **required reviewer** —
that's the manual approval gate.

## AWS setup checklist

- [ ] VPC with 2 subnets (staging / production)
- [ ] 2x EC2 instances (t2/t3.micro), SSM agent enabled, Docker installed, instance role with `AmazonSSMManagedInstanceCore` + ECR pull permissions
- [ ] ECR repository with enhanced scanning (Amazon Inspector) turned on
- [ ] IAM OIDC identity provider for `token.actions.githubusercontent.com`
- [ ] IAM role trusted by that provider, scoped to this repo, with ECR push + SSM send-command permissions
- [ ] CloudWatch dashboard + one alarm
- [ ] Budget alarm (done)

## Local dev

```bash
pip install -r requirements.txt
python app.py
```

## Deploy

Push to `main`. The pipeline runs automatically: scan → build → push → Inspector scan (automatic on ECR push) →
deploy staging → **manual approval** → deploy production.
