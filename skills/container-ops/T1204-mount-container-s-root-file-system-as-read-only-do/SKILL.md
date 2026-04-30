---
task_id: "T1204"
title: "Mount container's root file system as read-only (Docker)"
domain: "container-ops"
classification: "INFRA"
priority: 8
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T1204: Mount container's root file system as read-only (Docker)

## Context

**Domain:** container-ops  
**Classification:** INFRA  
**Priority:** P8  
**Phase:** Deployment  
**Primary Location:** `docker-compose.yml`

## Vulnerability

Container configuration includes excessive privileges or insecure settings.

## Fix Approach

Remove privileged mode and unnecessary capabilities; run as non-root user.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml`
2. Review the SD Elements countermeasure [T1204](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1204/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No `privileged: true` in docker-compose
- [ ] No unnecessary `cap_add` entries
- [ ] Container runs as non-root user

## References

- [SD Elements Countermeasure T1204](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T1204/)
- SDE Project: dvrag_20260430 (ID: 858)
