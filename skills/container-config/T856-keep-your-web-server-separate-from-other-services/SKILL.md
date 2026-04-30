---
task_id: "T856"
title: "Keep your web server separate from other services"
domain: "container-config"
classification: "CODE_FIX"
priority: 5
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T856: Keep your web server separate from other services

## Context

**Domain:** container-config  
**Classification:** CODE_FIX  
**Priority:** P5  
**Phase:** Deployment  
**Primary Location:** `docker-compose.yml`

## Vulnerability

Container configuration includes excessive privileges or insecure settings.

## Fix Approach

Remove privileged mode and unnecessary capabilities; run as non-root user.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml`
2. Review the SD Elements countermeasure [T856](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T856/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No `privileged: true` in docker-compose
- [ ] No unnecessary `cap_add` entries
- [ ] Container runs as non-root user

## References

- [SD Elements Countermeasure T856](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T856/)
- SDE Project: dvrag_20260430 (ID: 858)
