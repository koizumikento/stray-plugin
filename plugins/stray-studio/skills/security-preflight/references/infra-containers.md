# Infrastructure, Cloud, And Container Checks

Use this reference for Terraform, CloudFormation, Bicep, ARM, Kubernetes, Helm, Kustomize, Dockerfiles, Compose files, IAM policies, cloud storage, and network exposure.

For repository-managed infrastructure, select security-relevant controls from the [shared IaC baseline](../../../references/iac-baseline.md), [IaC lifecycle](../../../references/iac-lifecycle.md), and [operations/runtime](../../../references/iac-operations.md). Retain this skill's review-only evidence contract; identify prohibited live checks as proof gaps. General performance and cost optimization stay outside a security-only review.

## Review Focus

1. IAM and least privilege.
   - Check wildcard actions/resources, broad managed roles, long-lived keys, missing conditions, cross-account/public principals, and service accounts with excessive privileges.
   - Repository evidence can show broad policy intent, but actual unused permissions and effective access require cloud telemetry.

2. Public exposure and storage.
   - Look for public buckets, anonymous blob/container access, `Principal: "*"`, public ACLs, missing public-access blocks, public IPs, and unqualified public sharing.
   - Distinguish intended public web assets from accidental public access by requiring explicit justification or allowlist context.

3. Network rules.
   - Flag `0.0.0.0/0` or `::/0` to SSH, RDP, databases, admin ports, Kubernetes APIs, and internal services.
   - Review egress and endpoint/firewall choices against required clients and isolation; missing private endpoints alone are not defects. Check overly broad ingress on load balancers against their intended public/private role.
   - Do not claim actual reachability from security group rules alone; route tables, firewalls, NAT, load balancers, and cloud posture are needed.

4. Secrets in infrastructure.
   - Check Terraform variables, state handling, Kubernetes Secrets, Compose env, Docker build args, cloud-init, and deployment manifests for plaintext secrets.
   - Treat Terraform plan/state and Kubernetes Secret manifests as sensitive even when values are base64 encoded.

5. Terraform and IaC hygiene.
   - Check provider and module pinning, remote state, state encryption/access control, destructive defaults, and CI policy-as-code.
   - Use `terraform validate`, `terraform plan -out`, checkov, tfsec, terrascan, tflint, or OPA only when safe and available.
   - Avoid printing plans or state when secrets may be present.

6. Dockerfile and image hardening.
   - Check base image pinning, `latest` tags, non-root `USER`, unnecessary packages, package manager cache cleanup, secret `COPY`, build args, `.dockerignore`, multi-stage builds, and image scan evidence.
   - Pair Dockerfile review with Compose/Kubernetes runtime settings when present.

7. Kubernetes and container runtime.
   - Check privileged pods, `hostPath`, `hostNetwork`, `hostPID`, root containers, added capabilities, writable root filesystem, service-account token auto-mounting, RBAC breadth, NetworkPolicy absence, and Pod Security Standard labels.
   - Repository manifests cannot prove cluster admission, namespace labels, managed defaults, or runtime drift.

8. Compliance baselines.
   - Use applicable CIS, NIST, OWASP, cloud provider benchmarks, or posture-service evidence as inputs. Distinguish recommendations, scanner results, and formally adopted requirements; verify target edition/profile and coverage before treating a control as mandatory.
   - Do not claim CIS or cloud-benchmark compliance from a static repo review.

## Common Evidence Searches

- Cloud public access: `Principal`, `public`, `acl`, `anonymous`, `0.0.0.0/0`, `::/0`
- IAM breadth: `"*"`, `Action`, `Resource`, `Owner`, `Contributor`, `Administrator`, `roles/owner`
- Terraform state/secrets: `terraform.tfstate`, `sensitive`, `secret`, `password`, `private_key`
- Docker: `FROM .*latest`, `USER root`, `COPY .`, `ARG .*TOKEN`, `ENV .*SECRET`
- Kubernetes: `privileged`, `hostPath`, `hostNetwork`, `runAsUser: 0`, `allowPrivilegeEscalation`, `automountServiceAccountToken`

## Guardrails

- Do not mutate cloud resources, IAM, security groups, branch deployments, or Kubernetes clusters during a review-only task.
- Do not run cloud CLI commands that require credentials unless the user asks and the scope is explicit.
- Do not expose Terraform state, plan secrets, Kubernetes Secret values, or cloud credential material.
- Mark real effective access, runtime drift, unused permissions, and reachability as requiring cloud/CSPM or runtime evidence.

## Useful Source Baselines

- AWS IAM best practices, IAM Access Analyzer, S3 Block Public Access, Security Hub controls, and AWS Config managed rules.
- Azure identity, storage, network, Key Vault, and Defender for Cloud guidance.
- Google Cloud IAM, role recommendations, Cloud Storage public access prevention, Secret Manager, firewall, and Security Command Center guidance.
- OWASP IaC Security and Docker Security Cheat Sheets.
- Dockerfile best practices and Docker Scout.
- Kubernetes Pod Security Standards and Pod Security Admission.
- NSA/CISA Kubernetes Hardening Guidance.
- CIS benchmarks for AWS, Azure, GCP, Docker, and Kubernetes.
- NIST SP 800-190 and NIST CSF.
