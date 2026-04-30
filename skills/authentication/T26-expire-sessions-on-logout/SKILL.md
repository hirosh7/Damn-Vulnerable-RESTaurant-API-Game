---
task_id: "T26"
title: "Expire sessions on logout"
domain: "authentication"
classification: "CODE_FIX"
priority: 6
phase: "Requirements"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T26: Expire sessions on logout

## Context

**Domain:** authentication  
**Classification:** CODE_FIX  
**Priority:** P6  
**Phase:** Requirements  
**Primary Location:** `app/apis/auth/services/get_token_service.py`

## Vulnerability

Authentication controls may be insufficient or bypassable.

## Fix Approach

Enforce strong authentication requirements; validate tokens/credentials rigorously.

## Implementation Steps

1. Locate the relevant code at `app/apis/auth/services/get_token_service.py`
2. Review the SD Elements countermeasure [T26](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T26/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Authentication enforced on all protected endpoints
- [ ] Token validation tests pass
- [ ] No unauthenticated access to protected resources

## References

- [SD Elements Countermeasure T26](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T26/)
- SDE Project: dvrag_20260430 (ID: 858)
