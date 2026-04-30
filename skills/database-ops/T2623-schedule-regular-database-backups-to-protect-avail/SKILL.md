---
task_id: "T2623"
title: "Schedule regular database backups to protect availability (PostgreSQL)"
domain: "database-ops"
classification: "INFRA"
priority: 6
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T2623: Schedule regular database backups to protect availability (PostgreSQL)

## Context

**Domain:** database-ops  
**Classification:** INFRA  
**Priority:** P6  
**Phase:** Deployment  
**Primary Location:** `docker-compose.yml`

## Vulnerability

Raw SQL string interpolation allows SQL injection attacks.

## Fix Approach

Use parameterized queries or SQLAlchemy ORM. Replace f-string SQL with bound parameters.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml`
2. Review the SD Elements countermeasure [T2623](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2623/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No raw SQL string formatting in query construction
- [ ] All queries use SQLAlchemy ORM or parameterized statements
- [ ] Automated SQL injection tests pass

## References

- [SD Elements Countermeasure T2623](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2623/)
- SDE Project: dvrag_20260430 (ID: 858)
