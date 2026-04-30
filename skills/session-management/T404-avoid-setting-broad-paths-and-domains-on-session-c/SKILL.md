---
task_id: "T404"
title: "Avoid setting broad paths and domains on session cookies"
domain: "session-management"
classification: "CODE_FIX"
priority: 4
phase: "Development"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T404: Avoid setting broad paths and domains on session cookies

## Context

**Domain:** session-management  
**Classification:** CODE_FIX  
**Priority:** P4  
**Phase:** Development  
**Primary Location:** `app/init_app.py`

## Vulnerability

Session or token management may be insecure.

## Fix Approach

Implement secure token lifecycle: proper expiration, revocation, and secure storage.

## Implementation Steps

1. Locate the relevant code at `app/init_app.py`
2. Review the SD Elements countermeasure [T404](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T404/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Tokens expire as configured
- [ ] Revoked tokens are rejected
- [ ] No token reuse after logout

## References

- [SD Elements Countermeasure T404](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T404/)
- SDE Project: dvrag_20260430 (ID: 858)
