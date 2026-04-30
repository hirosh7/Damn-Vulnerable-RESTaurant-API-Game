---
task_id: "T1212"
title: "Confirm cgroup usage (Docker)"
domain: "container-ops"
classification: "INFRA"
priority: 7
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T1212: Confirm cgroup usage (Docker)

## Context

**Domain:** container-ops  
**Classification:** INFRA  
**Priority:** P7  
**Phase:** Deployment  
**Primary Location:** `docker-compose.yml`

## Vulnerability

Container operational settings may create security risks.

## Fix Approach

Apply container hardening: restrict capabilities, use read-only filesystems where possible, set resource limits.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml`
2. Review the SD Elements countermeasure [T1212](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1212/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Container security settings reviewed and hardened
- [ ] Resource limits configured
- [ ] Security scan passes

## References

- [SD Elements Countermeasure T1212](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1212/)
- SDE Project: dvrag_20260430 (ID: 858)
