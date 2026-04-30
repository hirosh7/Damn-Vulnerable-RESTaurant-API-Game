---
task_id: "T322"
title: "Include HTTP Strict-Transport-Security headers in HTTPS responses"
domain: "api-security"
classification: "CODE_FIX"
priority: 5
phase: "Requirements"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T322: Include HTTP Strict-Transport-Security headers in HTTPS responses

## Context

**Domain:** api-security  
**Classification:** CODE_FIX  
**Priority:** P5  
**Phase:** Requirements  
**Primary Location:** `app/init_app.py:36`

## Vulnerability

API may lack proper security controls against common attack patterns.

## Fix Approach

Apply API security best practices: rate limiting, request size limits, input validation, proper HTTP methods.

## Implementation Steps

1. Locate the relevant code at `app/init_app.py:36`
2. Review the SD Elements countermeasure [T322](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T322/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Rate limiting applied to sensitive endpoints
- [ ] Request size limits enforced
- [ ] API security scan passes

## References

- [SD Elements Countermeasure T322](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T322/)
- SDE Project: dvrag_20260430 (ID: 858)
