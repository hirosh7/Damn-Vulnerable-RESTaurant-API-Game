---
task_id: "T1162"
title: "Enable live restore (Docker)"
domain: "container-ops"
classification: "INFRA"
priority: 4
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T1162: Enable live restore (Docker)

## Context

**Domain:** container-ops  
**Classification:** INFRA  
**Priority:** P4  
**Phase:** Deployment  
**Primary Location:** `docker-compose.yml`

## Vulnerability

Container operational settings may create security risks.

## Fix Approach

Apply container hardening: restrict capabilities, use read-only filesystems where possible, set resource limits.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml`
2. Review the SD Elements countermeasure [T1162](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1162/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Container security settings reviewed and hardened
- [ ] Resource limits configured
- [ ] Security scan passes

## References

- [SD Elements Countermeasure T1162](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1162/)
- SDE Project: dvrag_20260430 (ID: 858)
