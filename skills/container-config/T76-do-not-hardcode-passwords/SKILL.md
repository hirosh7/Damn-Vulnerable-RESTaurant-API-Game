---
task_id: "T76"
title: "Do not hardcode passwords"
domain: "container-config"
classification: "CODE_FIX"
priority: 10
phase: "Development"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T76: Do not hardcode passwords

## Context

**Domain:** container-config  
**Classification:** CODE_FIX  
**Priority:** P10  
**Phase:** Development  
**Primary Location:** `docker-compose.yml:15`

## Vulnerability

Credentials or secrets may be hardcoded or insufficiently protected.

## Fix Approach

Remove hardcoded secrets; load all credentials from environment variables or a secrets manager.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml:15`
2. Review the SD Elements countermeasure [T76](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T76/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No hardcoded credentials in code or config files
- [ ] Secrets loaded from environment at runtime
- [ ] Secrets scanner finds no violations

## References

- [SD Elements Countermeasure T76](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T76/)
- SDE Project: dvrag_20260430 (ID: 858)
