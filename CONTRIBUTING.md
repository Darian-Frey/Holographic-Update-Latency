# Contributing to CODE-GEO
All contributions must adhere to the **Universal Agent Protocol V2.2** and **SCHEMA_V5**.

### 🛠️ Protocol Requirements:
1. **One-In-One-Out:** Synchronous messaging for LLM-Human collaboration.
2. **State Integrity:** All code changes must advance STATE_V2 and be documented in the AUDIT_LOG.md.
3. **Safety First:** Any change to the core theory must pass the `tools/auditor.py` BBN-Safety check.

Please refer to the `docs/MANUSCRIPT.md` for the theoretical baseline before submitting PRs.
