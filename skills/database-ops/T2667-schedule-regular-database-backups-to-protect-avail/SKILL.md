---
task_id: "T2667"
title: "Schedule regular database backups to protect availability (Database Server)"
domain: "database-ops"
classification: "INFRA"
priority: 6
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T2667: Schedule regular database backups to protect availability (Database Server)

## Context

**Domain:** database-ops  
**Classification:** INFRA  
**Priority:** P6  
**Phase:** Deployment  
**Primary Location:** `docker-compose.yml`

## Vulnerability

Database configuration may be insecure or allow excessive access.

## Fix Approach

Apply principle of least privilege to database accounts; enable encryption at rest.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml`
2. Review the SD Elements countermeasure [T2667](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2667/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Database user has minimal required permissions
- [ ] Encryption at rest configured
- [ ] Database access audited

## References

- [SD Elements Countermeasure T2667](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2667/)
- SDE Project: dvrag_20260430 (ID: 858)
