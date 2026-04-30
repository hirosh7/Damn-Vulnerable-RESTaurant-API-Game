---
task_id: "T7"
title: "Salt and hash stored passwords"
domain: "authentication"
classification: "CODE_FIX"
priority: 6
phase: "Requirements"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T7: Salt and hash stored passwords

## Context

**Domain:** authentication  
**Classification:** CODE_FIX  
**Priority:** P6  
**Phase:** Requirements  
**Primary Location:** `app/apis/auth/utils/utils.py:21`

## Vulnerability

Credentials or secrets may be hardcoded or insufficiently protected.

## Fix Approach

Remove hardcoded secrets; load all credentials from environment variables or a secrets manager.

## Implementation Steps

1. Locate the relevant code at `app/apis/auth/utils/utils.py:21`
2. Review the SD Elements countermeasure [T7](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T7/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No hardcoded credentials in code or config files
- [ ] Secrets loaded from environment at runtime
- [ ] Secrets scanner finds no violations

## References

- [SD Elements Countermeasure T7](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T7/)
- SDE Project: dvrag_20260430 (ID: 858)
