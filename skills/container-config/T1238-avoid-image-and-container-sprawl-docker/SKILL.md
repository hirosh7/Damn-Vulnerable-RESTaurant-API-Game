---
task_id: "T1238"
title: "Avoid image and container sprawl (Docker)"
domain: "container-config"
classification: "CODE_FIX"
priority: 5
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T1238: Avoid image and container sprawl (Docker)

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
2. Review the SD Elements countermeasure [T1238](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1238/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No `privileged: true` in docker-compose
- [ ] No unnecessary `cap_add` entries
- [ ] Container runs as non-root user

## References

- [SD Elements Countermeasure T1238](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1238/)
- SDE Project: dvrag_20260430 (ID: 858)
