---
task_id: "T184"
title: "Perform authorization checks on RESTful web services"
domain: "authorization"
classification: "CODE_FIX"
priority: 9
phase: "Development"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T184: Perform authorization checks on RESTful web services

## Context

**Domain:** authorization  
**Classification:** CODE_FIX  
**Priority:** P9  
**Phase:** Development  
**Primary Location:** `app/apis/orders/services/`

## Vulnerability

Authorization controls may be missing or insufficiently granular.

## Fix Approach

Apply role-based access control checks; verify user has required permissions before granting access.

## Implementation Steps

1. Locate the relevant code at `app/apis/orders/services/`
2. Review the SD Elements countermeasure [T184](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T184/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] All sensitive endpoints require appropriate role checks
- [ ] Authorization tests pass
- [ ] Privilege escalation tests fail

## References

- [SD Elements Countermeasure T184](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T184/)
- SDE Project: dvrag_20260430 (ID: 858)
