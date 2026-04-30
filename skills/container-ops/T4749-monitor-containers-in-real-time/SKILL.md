---
task_id: "T4749"
title: "Monitor containers in real-time"
domain: "container-ops"
classification: "INFRA"
priority: 10
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T4749: Monitor containers in real-time

## Context

**Domain:** container-ops  
**Classification:** INFRA  
**Priority:** P10  
**Phase:** Deployment  
**Primary Location:** `docker-compose.yml`

## Vulnerability

Container operational settings may create security risks.

## Fix Approach

Apply container hardening: restrict capabilities, use read-only filesystems where possible, set resource limits.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml`
2. Review the SD Elements countermeasure [T4749](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T4749/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Container security settings reviewed and hardened
- [ ] Resource limits configured
- [ ] Security scan passes

## References

- [SD Elements Countermeasure T4749](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T4749/)
- SDE Project: dvrag_20260430 (ID: 858)
