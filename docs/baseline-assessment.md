# Baseline Assessment

## Scope
A source-level review of the original Python CLI implementation in `IAM PS CODE`.

## Existing capabilities
- In-memory user and role dictionaries.
- Role-permission assignment.
- User-role assignment.
- Access checks based on permissions inherited from assigned roles.
- JSON save/load functionality.

## Findings from the initial review

| Area | Baseline observation | Security / engineering implication |
|---|---|---|
| Authorization | Access is allowed when any assigned role contains the requested permission | Basic RBAC model; no explicit deny rules or contextual conditions |
| Default behaviour | Unknown users are rejected; unmatched permissions are denied | A useful starting point for deny-by-default |
| Account lifecycle | No active/disabled account state | A user cannot be suspended without removing the identity |
| Revocation | No menu action to remove roles or permissions | Least-privilege changes are difficult to demonstrate |
| Auditability | No durable record of administrative changes or access decisions | Investigations cannot reconstruct who changed access or why |
| Input validation | Names and permissions are accepted with minimal validation | Empty or inconsistent values can enter the policy data |
| Persistence | JSON load assumes expected object shapes and catches only missing files | Malformed or unexpected data may cause runtime errors |
| Testing | No automated test suite was present in the reviewed baseline | Regressions and security properties are not verified automatically |
| Architecture | Business logic and interactive CLI are in one script | Harder to test and extend safely |

## Initial risk priorities
1. Add automated tests around authorization decisions.
2. Add permission and role revocation.
3. Add account disablement and ensure disabled users are denied.
4. Add audit events for security-relevant actions.
5. Validate persisted data before trusting it.

## Assessment limitations
This is a source-code review of the initial repository version, not a penetration test, formal audit, or assessment of a production deployment. Findings should be updated as implementation changes.
