---
task_id: "T36"
title: "Escape untrusted data in HTML, HTML attributes, CSS, and JavaScript"
domain: "input-validation"
classification: "CODE_FIX"
priority: 8
phase: "Development"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T36: Escape untrusted data in HTML, HTML attributes, CSS, and JavaScript

## Context

**Domain:** input-validation  
**Classification:** CODE_FIX  
**Priority:** P8  
**Phase:** Development  
**Primary Location:** `app/apis/`

## Vulnerability

User input is not sufficiently validated, enabling injection or malformed data attacks.

## Fix Approach

Validate and sanitize all input at the API boundary using strict schemas and allowlists.

## Implementation Steps

1. Locate the relevant code at `app/apis/`
2. Review the SD Elements countermeasure [T36](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T36/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] All API inputs validated against strict schemas
- [ ] Malformed input returns 422 with clear error
- [ ] Injection payloads rejected

## References

- [SD Elements Countermeasure T36](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T36/)
- SDE Project: dvrag_20260430 (ID: 858)
