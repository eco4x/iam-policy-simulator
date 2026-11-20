# IAM Policy Simulator — Homelab Roadmap

## Project purpose
An educational Identity and Access Management (IAM) security prototype for a single organisation. It demonstrates how identities, roles, permissions, access decisions, and audit evidence fit together.

This is a learning homelab, not a production identity provider or enterprise IAM service.

## Three-day showcase target

### Day 1 — Core access control
- Establish a documented baseline.
- Separate core IAM logic from terminal input/output.
- Implement user and role creation, role assignment, permission grant/revoke, and access checks.
- Enforce deny-by-default and reject unknown identities or roles.
- Add automated tests for the core access-control paths.

### Day 2 — Security visibility
- Record identity, role, permission, and access-decision events.
- Add basic least-privilege review findings.
- Add inactive-account and excessive-access checks.
- Test both permitted and denied scenarios.

### Day 3 — Evidence and communication
- Run the test suite and record actual results.
- Document the threat model and limitations.
- Capture terminal screenshots and a short walkthrough.
- Update the README with setup, capabilities, and evidence.
- Publish a LinkedIn post linking to the repository.

## Later milestones
1. Persistent storage with schema validation and safe file handling.
2. Authentication demonstrations using secure password hashing.
3. Attribute-based access control (ABAC) policies.
4. Privileged access workflows and time-limited elevation.
5. Access certification and joiner-mover-leaver workflows.
6. API and dashboard, only after the core security model is stable.
7. Optional SIEM export and identity-event detection.

## Showcase rule
Only describe capabilities that exist in the repository and have been tested. Clearly label simulated controls and planned features.
