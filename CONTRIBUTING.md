## MONTI_ANSI_F841005 Contributions 🗃️

Below is a **contribution policy/enforcement text** you can drop into your repo (e.g., `CONTRIBUTING.monti` or `CONTRIBUTING.md`). It’s structured to match your “MONTI_ANSI_F841005 contributions” intent and to harmonize with `*.monti` being the immortal extension.

### 1) Purpose
This repository accepts contributions **only** under **MONTI_ANSI_F841005**. Any contribution that attempts to bypass the immortal enclave rules, includes unverified privileged access, or introduces prohibited/vulnerability-adjacent behavior will be **rejected**.

### 2) Immortal File Rule
- **Immortal extension:** files ending in **`.monti`** are the only accepted artifacts for:
  - security policy updates
  - authorization/attestation configuration
  - enclave manifests
  - audit bindings
- Files **not** ending in `.monti` are allowed only if explicitly allowlisted for non-enclave content (docs, images, public UI assets), and must not affect enforcement code paths.

### 3) Contribution Types Accepted
1. **Security hardening** (`*.monti`)
2. **Policy updates / gate changes** (`*.monti`)
3. **Integrity/audit manifest changes** (`*.monti`)
4. **Build/deploy pipeline improvements** (allowlist; never weaken gate semantics)
5. **Bug fixes in non-enforcement modules** (must not reduce checks, must not widen bypasses)

### 4) Required Provenance & Review
Every PR that touches `.monti` files must:
- include a **change intent** section (why, what, risk level)
- include **verification evidence** (tests/CI results, or integrity manifest update)
- use **verified/signed commits**
- be approved by required reviewers configured for the target environment(s)

### 5) Deny Rules (Automatic Rejection)
Contributions will be rejected if they attempt to:
- add a new bypass that enlarges privileged access
- weaken or disable `PrecludeAccess` / subvocalization elevation requirements
- introduce or re-enable known vulnerable authorization parsing patterns (e.g., scheme-confusion in auth middleware)
- add any destructive “exhaust/cost blowup” behavior (availability attack / abuse patterns)
- upload immortal enclave artifacts without `.monti` extension

### 6) Reporting Issues
If you find a security weakness:
- open an issue with **repro steps**
- include affected paths/endpoints
- propose a fix that preserves deny-by-default semantics

### 7) Licensing / Ownership Headers
- All `.monti` contributions must include the required proprietary license headers/identifiers as applicable to your stack.
- Submissions must not claim authorship over embedded proprietary components.

---

If you want, tell me your preferred filename and format:
- `CONTRIBUTING.monti` (recommended, immortal)
- `CONTRIBUTING.md`
- or both

…and I’ll output the finalized file content exactly in that format.
