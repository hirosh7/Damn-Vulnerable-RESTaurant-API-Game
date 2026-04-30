---
task_id: "T1184"
title: "Use COPY instead of ADD in Dockerfile (Docker)"
domain: "container-config"
classification: "CODE_FIX"
priority: 5
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T1184: Use COPY instead of ADD in Dockerfile (Docker)

## Context

**Domain:** container-config  
**Classification:** CODE_FIX  
**Priority:** P5  
**Phase:** Deployment  
**Primary Location:** `Dockerfile`

## Vulnerability

Container configuration includes excessive privileges or insecure settings.

## Fix Approach

Remove privileged mode and unnecessary capabilities; run as non-root user.

## Implementation Steps

1. Locate the relevant code at `Dockerfile`
2. Review the SD Elements countermeasure [T1184](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1184/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No `privileged: true` in docker-compose
- [ ] No unnecessary `cap_add` entries
- [ ] Container runs as non-root user

## References

- [SD Elements Countermeasure T1184](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1184/)
- SDE Project: dvrag_20260430 (ID: 858)
