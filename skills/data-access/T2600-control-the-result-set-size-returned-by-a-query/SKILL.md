---
task_id: "T2600"
title: "Control the result set size returned by a query"
domain: "data-access"
classification: "CODE_FIX"
priority: 7
phase: "Development"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T2600: Control the result set size returned by a query

## Context

**Domain:** data-access  
**Classification:** CODE_FIX  
**Priority:** P7  
**Phase:** Development  
**Primary Location:** `app/apis/orders/services/get_orders_for_delivery_service.py`

## Vulnerability

Raw SQL string interpolation allows SQL injection attacks.

## Fix Approach

Use parameterized queries or SQLAlchemy ORM. Replace f-string SQL with bound parameters.

## Implementation Steps

1. Locate the relevant code at `app/apis/orders/services/get_orders_for_delivery_service.py`
2. Review the SD Elements countermeasure [T2600](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2600/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] No raw SQL string formatting in query construction
- [ ] All queries use SQLAlchemy ORM or parameterized statements
- [ ] Automated SQL injection tests pass

## References

- [SD Elements Countermeasure T2600](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T2600/)
- SDE Project: dvrag_20260430 (ID: 858)
