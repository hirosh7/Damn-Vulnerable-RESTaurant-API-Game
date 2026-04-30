---
task_id: "T17"
title: "Do not only rely on client-side authorization"
domain: "authorization"
classification: "CODE_FIX"
priority: 8
phase: "Development"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T17: Do not only rely on client-side authorization

## Context

**Domain:** authorization  
**Classification:** CODE_FIX  
**Priority:** P8  
**Phase:** Development  
**Primary Location:** `app/apis/orders/services/get_order_status.py`

## Vulnerability

Authorization controls may be missing or insufficiently granular.

## Fix Approach

Apply role-based access control checks; verify user has required permissions before granting access.

## Implementation Steps

1. Locate the relevant code at `app/apis/orders/services/get_order_status.py`
2. Review the SD Elements countermeasure [T17](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T17/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] All sensitive endpoints require appropriate role checks
- [ ] Authorization tests pass
- [ ] Privilege escalation tests fail

## References

- [SD Elements Countermeasure T17](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T17/)
- SDE Project: dvrag_20260430 (ID: 858)
