---
task_id: "T1178"
title: "Do not install unnecessary packages in the container (Docker)"
domain: "container-config"
classification: "CODE_FIX"
priority: 5
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T1178: Do not install unnecessary packages in the container (Docker)

## Context

**Domain:** container-config  
**Classification:** CODE_FIX  
**Priority:** P5  
**Phase:** Deployment  
**Primary Location:** `Dockerfile:11`

## Vulnerability

Container configuration includes excessive privileges or insecure settings.

## Fix Approach

Remove privileged mode and unnecessary capabilities; run as non-root user.

## Implementation Steps

1. Locate the relevant code at `Dockerfile:11`
2. Review the SD Elements countermeasure [T1178](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1178/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No `privileged: true` in docker-compose
- [ ] No unnecessary `cap_add` entries
- [ ] Container runs as non-root user

## References

- [SD Elements Countermeasure T1178](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1178/)
- SDE Project: dvrag_20260430 (ID: 858)
