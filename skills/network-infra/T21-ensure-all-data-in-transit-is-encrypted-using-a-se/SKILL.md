---
task_id: "T21"
title: "Ensure all data in transit is encrypted using a secure TLS channel"
domain: "network-infra"
classification: "INFRA"
priority: 8
phase: "Requirements"
sde_project_id: 858
sde_project_name: "dvrag_20260430"
---

# T21: Ensure all data in transit is encrypted using a secure TLS channel

## Context

**Domain:** network-infra  
**Classification:** INFRA  
**Priority:** P8  
**Phase:** Requirements  
**Primary Location:** `external`

## Vulnerability

Network configuration may expose services insecurely or allow unnecessary traffic.

## Fix Approach

Restrict network exposure; use TLS for all communications; apply network policies.

## Implementation Steps

1. Locate the relevant code at `external`
2. Review the SD Elements countermeasure [T21](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T21/) for specific guidance
3. Implement the required security control
4. Write or update tests to verify the fix
5. Confirm no regression in existing functionality

## Success Criteria

- [ ] Only required ports exposed
- [ ] TLS configured for external traffic
- [ ] Network policies applied

## References

- [SD Elements Countermeasure T21](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag_20260430/task/T21/)
- SDE Project: dvrag_20260430 (ID: 858)
