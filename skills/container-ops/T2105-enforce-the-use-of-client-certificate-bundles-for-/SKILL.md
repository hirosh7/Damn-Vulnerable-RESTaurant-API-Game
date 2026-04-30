---
task_id: "T2105"
title: "Enforce the use of client certificate bundles for unprivileged users to access UCP (Docker)"
domain: "container-ops"
classification: "INFRA"
priority: 7
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T2105: Enforce the use of client certificate bundles for unprivileged users to access UCP (Docker)

## Context

**Domain:** container-ops  
**Classification:** INFRA  
**Priority:** P7  
**Phase:** Deployment  
**Primary Location:** `docker-compose.yml`

## Vulnerability

Container configuration includes excessive privileges or insecure settings.

## Fix Approach

Remove privileged mode and unnecessary capabilities; run as non-root user.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml`
2. Review the SD Elements countermeasure [T2105](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2105/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No `privileged: true` in docker-compose
- [ ] No unnecessary `cap_add` entries
- [ ] Container runs as non-root user

## References

- [SD Elements Countermeasure T2105](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2105/)
- SDE Project: dvrag_20260430 (ID: 858)
