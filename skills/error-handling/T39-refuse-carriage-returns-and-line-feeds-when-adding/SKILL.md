---
task_id: "T39"
title: "Refuse carriage returns and line feeds when adding data to HTTP response headers"
domain: "error-handling"
classification: "CODE_FIX"
priority: 4
phase: "Development"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T39: Refuse carriage returns and line feeds when adding data to HTTP response headers

## Context

**Domain:** error-handling  
**Classification:** CODE_FIX  
**Priority:** P4  
**Phase:** Development  
**Primary Location:** `app/apis/`

## Vulnerability

Error responses may leak sensitive implementation details.

## Fix Approach

Return generic error messages to clients; log full details server-side only.

## Implementation Steps

1. Locate the relevant code at `app/apis/`
2. Review the SD Elements countermeasure [T39](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T39/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No stack traces or internal paths in API error responses
- [ ] Errors logged with full context server-side
- [ ] Error response tests pass

## References

- [SD Elements Countermeasure T39](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T39/)
- SDE Project: dvrag_20260430 (ID: 858)
