---
task_id: "T61"
title: "Disable default accounts or change all default passwords"
domain: "container-config"
classification: "CODE_FIX"
priority: 9
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T61: Disable default accounts or change all default passwords

## Context

**Domain:** container-config  
**Classification:** CODE_FIX  
**Priority:** P9  
**Phase:** Deployment  
**Primary Location:** `docker-compose.yml:15`

## Vulnerability

Credentials or secrets may be hardcoded or insufficiently protected.

## Fix Approach

Remove hardcoded secrets; load all credentials from environment variables or a secrets manager.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml:15`
2. Review the SD Elements countermeasure [T61](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T61/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No hardcoded credentials in code or config files
- [ ] Secrets loaded from environment at runtime
- [ ] Secrets scanner finds no violations

## References

- [SD Elements Countermeasure T61](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T61/)
- SDE Project: dvrag_20260430 (ID: 858)
