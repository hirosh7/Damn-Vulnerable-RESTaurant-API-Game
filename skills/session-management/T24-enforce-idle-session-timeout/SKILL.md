---
task_id: "T24"
title: "Enforce idle session timeout"
domain: "session-management"
classification: "CODE_FIX"
priority: 3
phase: "Requirements"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T24: Enforce idle session timeout

## Context

**Domain:** session-management  
**Classification:** CODE_FIX  
**Priority:** P3  
**Phase:** Requirements  
**Primary Location:** `app/apis/auth/utils/jwt_auth.py`

## Vulnerability

Session or token management may be insecure.

## Fix Approach

Implement secure token lifecycle: proper expiration, revocation, and secure storage.

## Implementation Steps

1. Locate the relevant code at `app/apis/auth/utils/jwt_auth.py`
2. Review the SD Elements countermeasure [T24](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T24/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Tokens expire as configured
- [ ] Revoked tokens are rejected
- [ ] No token reuse after logout

## References

- [SD Elements Countermeasure T24](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T24/)
- SDE Project: dvrag_20260430 (ID: 858)
