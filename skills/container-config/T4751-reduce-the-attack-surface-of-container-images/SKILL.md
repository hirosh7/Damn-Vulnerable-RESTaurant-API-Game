---
task_id: "T4751"
title: "Reduce the attack surface of container images"
domain: "container-config"
classification: "CODE_FIX"
priority: 10
phase: "Development"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T4751: Reduce the attack surface of container images

## Context

**Domain:** container-config  
**Classification:** CODE_FIX  
**Priority:** P10  
**Phase:** Development  
**Primary Location:** `Dockerfile`

## Vulnerability

Container configuration includes excessive privileges or insecure settings.

## Fix Approach

Remove privileged mode and unnecessary capabilities; run as non-root user.

## Implementation Steps

1. Locate the relevant code at `Dockerfile`
2. Review the SD Elements countermeasure [T4751](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T4751/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No `privileged: true` in docker-compose
- [ ] No unnecessary `cap_add` entries
- [ ] Container runs as non-root user

## References

- [SD Elements Countermeasure T4751](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T4751/)
- SDE Project: dvrag_20260430 (ID: 858)
