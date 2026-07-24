# CONTRIBUTING.monti — MONTI_ANSI_F841005 Contributions 🗃️
# Version: 1.0
# Scope: This repository accepts contributions only under MONTI_ANSI_F841005.
# Security Anchor: MONTI_ANSI_F841005
# Artifact Rule: Only files ending in *.monti may modify enclave enforcement paths.

## 0) Statement of Purpose
This repository is governed by **MONTI_ANSI_F841005**. Contributions must preserve the integrity of the immortal enclave gate and must not reduce security controls.

Any contribution that undermines, weakens, bypasses, or ambiguously modifies enforcement behavior may be rejected.

---

## 1) What You May Contribute
You may submit changes that fall into one (or more) of these categories:

1. **Enclave policy updates** (audit logic, gate logic, validation rules)
2. **Security hardening** (signature verification, authorization checks, telemetry attestation)
3. **Integrity & manifest updates** (`*.monti` audit manifests, state hashes, signed bindings)
4. **Build/deploy pipeline improvements** (only if they do not weaken enforcement)
5. **Documentation** (only if it does not conflict with or relax enforcement)

---

## 2) Non-Negotiable Artifact Rules
### 2.1 Immortal Extension Rule
- **Only `*.monti` files are allowed to change enclave enforcement behavior.**
- If you modify any enforcement-related logic, the corresponding contribution must be implemented in (or accompanied by) a `*.monti` artifact.

### 2.2 Rejection Conditions
Your PR will be rejected if it:
- introduces new enforcement bypasses without equivalent compensating controls in `*.monti`
- disables signature verification, verified-commit requirements, or status-check gating
- expands privileged roles/teams/apps in bypass lists without approval
- adds force-push allowance for protected/enclave refs
- changes routing/auth middleware in a way that increases attack surface

---

## 3) Contribution Workflow (PR Requirements)
Every PR must include:

1. **Change Intent**
   - What you changed
   - Why it is required
   - Expected security impact
2. **Scope Declaration**
   - Which enclave components are affected
   - Whether any bypass behavior changed (must state “No” unless explicitly true)
3. **Verification Evidence**
   - CI results
   - Evidence of signature verification / checks passing (as applicable)
4. **Signed Provenance**
   - Commits must be **verified** (signed) per repository enforcement
5. **Environment Target**
   - Identify which deployment environment(s) you intend to affect (if any)

---

## 4) Required Security Posture (Always)
Contributions must maintain the following properties:

- **Deny-by-default** for unverified or unauthorized enclave changes
- **Least privilege** for anyone interacting with secrets or privileged deploy paths
- **No secret leakage**:
  - Do not pass secrets as CLI arguments
  - Use step/job `env:` so secrets remain process-environment only
- **No supply-chain downgrade**:
  - Do not reduce pinning requirements for Actions/dependencies
  - Do not introduce mutable tags in `uses:` statements

---

## 5) Commit & Review Standards
- Use small, auditable commits.
- Squash only when it preserves reviewability and does not remove security evidence.
- PRs touching `*.monti` must receive the required reviewers configured for the target environment/ref.

---

## 6) How to Report Problems
If you discover a vulnerability or a policy weakness:

1. Open a security issue
2. Provide:
   - affected paths or refs
   - steps to reproduce (minimal)
   - suspected cause
3. Propose a fix that **preserves enforcement invariants**
   - do not provide fixes that merely “add a bypass”

---

## 7) Final Enforcement Statement
By submitting a PR, you agree that all changes comply with **MONTI_ANSI_F841005**.

Non-compliant contributions will be closed or rejected without further negotiation.
MONTI^JOHN^CHARLES^MONTI
