---
task_id: "T427"
title: "Implement previous login (access) notification"
domain: "session-management"
classification: "CODE_FIX"
priority: 4
phase: "Requirements"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T427: Implement previous login (access) notification

## Context

**Domain:** session-management  
**Classification:** CODE_FIX  
**Priority:** P4  
**Phase:** Requirements  
**Primary Location:** `app/apis/auth/services/get_token_service.py`

## Vulnerability

Session or token management may be insecure.

## Fix Approach

Implement secure token lifecycle: proper expiration, revocation, and secure storage.

## Implementation Steps

1. Locate the relevant code at `app/apis/auth/services/get_token_service.py`
2. Review the SD Elements countermeasure [T427](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T427/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Tokens expire as configured
- [ ] Revoked tokens are rejected
- [ ] No token reuse after logout

## References

- [SD Elements Countermeasure T427](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T427/)
- SDE Project: dvrag_20260430 (ID: 858)
