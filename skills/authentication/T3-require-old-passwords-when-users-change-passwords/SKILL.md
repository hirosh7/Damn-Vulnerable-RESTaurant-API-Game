---
task_id: "T3"
title: "Require old passwords when users change passwords"
domain: "authentication"
classification: "CODE_FIX"
priority: 6
phase: "Requirements"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T3: Require old passwords when users change passwords

## Context

**Domain:** authentication  
**Classification:** CODE_FIX  
**Priority:** P6  
**Phase:** Requirements  
**Primary Location:** `app/apis/auth/services/update_profile_service.py`

## Vulnerability

Credentials or secrets may be hardcoded or insufficiently protected.

## Fix Approach

Remove hardcoded secrets; load all credentials from environment variables or a secrets manager.

## Implementation Steps

1. Locate the relevant code at `app/apis/auth/services/update_profile_service.py`
2. Review the SD Elements countermeasure [T3](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T3/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No hardcoded credentials in code or config files
- [ ] Secrets loaded from environment at runtime
- [ ] Secrets scanner finds no violations

## References

- [SD Elements Countermeasure T3](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T3/)
- SDE Project: dvrag_20260430 (ID: 858)
