---
task_id: "T2597"
title: "Implement RBAC instead of individual accounts"
domain: "deployment"
classification: "INFRA"
priority: 10
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T2597: Implement RBAC instead of individual accounts

## Context

**Domain:** deployment  
**Classification:** INFRA  
**Priority:** P10  
**Phase:** Deployment  
**Primary Location:** `external`

## Vulnerability

Deployment configuration or process may lack security controls.

## Fix Approach

Harden deployment pipeline and runtime configuration following security best practices.

## Implementation Steps

1. Locate the relevant code at `external`
2. Review the SD Elements countermeasure [T2597](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2597/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Deployment follows security checklist
- [ ] Configuration hardened per guidelines
- [ ] Deployment security review passed

## References

- [SD Elements Countermeasure T2597](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2597/)
- SDE Project: dvrag_20260430 (ID: 858)
