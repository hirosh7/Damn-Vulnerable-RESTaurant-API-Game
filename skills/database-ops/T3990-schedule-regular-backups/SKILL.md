---
task_id: "T3990"
title: "Schedule regular backups"
domain: "database-ops"
classification: "INFRA"
priority: 6
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T3990: Schedule regular backups

## Context

**Domain:** database-ops  
**Classification:** INFRA  
**Priority:** P6  
**Phase:** Deployment  
**Primary Location:** `external`

## Vulnerability

Database configuration may be insecure or allow excessive access.

## Fix Approach

Apply principle of least privilege to database accounts; enable encryption at rest.

## Implementation Steps

1. Locate the relevant code at `external`
2. Review the SD Elements countermeasure [T3990](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T3990/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Database user has minimal required permissions
- [ ] Encryption at rest configured
- [ ] Database access audited

## References

- [SD Elements Countermeasure T3990](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T3990/)
- SDE Project: dvrag_20260430 (ID: 858)
