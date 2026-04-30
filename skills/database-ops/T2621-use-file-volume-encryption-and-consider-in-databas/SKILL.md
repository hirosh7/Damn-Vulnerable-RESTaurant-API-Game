---
task_id: "T2621"
title: "Use file volume encryption and consider in-database encryption with pgcrypto (PostgreSQL)"
domain: "database-ops"
classification: "INFRA"
priority: 8
phase: "Deployment"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T2621: Use file volume encryption and consider in-database encryption with pgcrypto (PostgreSQL)

## Context

**Domain:** database-ops  
**Classification:** INFRA  
**Priority:** P8  
**Phase:** Deployment  
**Primary Location:** `docker-compose.yml`

## Vulnerability

Raw SQL string interpolation allows SQL injection attacks.

## Fix Approach

Use parameterized queries or SQLAlchemy ORM. Replace f-string SQL with bound parameters.

## Implementation Steps

1. Locate the relevant code at `docker-compose.yml`
2. Review the SD Elements countermeasure [T2621](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2621/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No raw SQL string formatting in query construction
- [ ] All queries use SQLAlchemy ORM or parameterized statements
- [ ] Automated SQL injection tests pass

## References

- [SD Elements Countermeasure T2621](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2621/)
- SDE Project: dvrag_20260430 (ID: 858)
