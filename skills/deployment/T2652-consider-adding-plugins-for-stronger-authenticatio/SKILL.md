---
task_id: "T2652"
title: "Consider adding plugins for stronger authentication protocols and stricter password complexity rules (MariaDB)"
domain: "deployment"
classification: "INFRA"
priority: 9
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T2652: Consider adding plugins for stronger authentication protocols and stricter password complexity rules (MariaDB)

## Context

**Domain:** deployment  
**Classification:** INFRA  
**Priority:** P9  
**Phase:** Deployment  
**Primary Location:** `external`

## Vulnerability

Credentials or secrets may be hardcoded or insufficiently protected.

## Fix Approach

Remove hardcoded secrets; load all credentials from environment variables or a secrets manager.

## Implementation Steps

1. Locate the relevant code at `external`
2. Review the SD Elements countermeasure [T2652](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2652/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No hardcoded credentials in code or config files
- [ ] Secrets loaded from environment at runtime
- [ ] Secrets scanner finds no violations

## References

- [SD Elements Countermeasure T2652](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2652/)
- SDE Project: dvrag_20260430 (ID: 858)
