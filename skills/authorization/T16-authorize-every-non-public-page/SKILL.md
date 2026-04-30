---
task_id: "T16"
title: "Authorize every non-public page"
domain: "authorization"
classification: "CODE_FIX"
priority: 6
phase: "Development"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T16: Authorize every non-public page

## Context

**Domain:** authorization  
**Classification:** CODE_FIX  
**Priority:** P6  
**Phase:** Development  
**Primary Location:** `app/apis/orders/services/`

## Vulnerability

Authorization controls may be missing or insufficiently granular.

## Fix Approach

Apply role-based access control checks; verify user has required permissions before granting access.

## Implementation Steps

1. Locate the relevant code at `app/apis/orders/services/`
2. Review the SD Elements countermeasure [T16](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T16/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] All sensitive endpoints require appropriate role checks
- [ ] Authorization tests pass
- [ ] Privilege escalation tests fail

## References

- [SD Elements Countermeasure T16](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T16/)
- SDE Project: dvrag_20260430 (ID: 858)
