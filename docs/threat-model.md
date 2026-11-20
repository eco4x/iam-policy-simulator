# Initial Threat Model

## System boundary
A local, single-organisation Python IAM simulator operated through a command-line interface. The first iteration uses local data files and is intended for controlled learning and demonstration.

## Assets
- User identities and account status.
- Role definitions and permission assignments.
- Policy/configuration data.
- Audit records showing administrative actions and access decisions.

## Trust boundaries
- Human operator to CLI input.
- Application logic to persisted JSON data.
- Authorization decision point to the caller requesting access.

## Threat scenarios

| Threat | Example | Initial mitigation / test |
|---|---|---|
| Excessive privilege | A user receives an unnecessary administrative role | Review assigned roles and flag broad permissions |
| Stale account | A former employee remains enabled | Disable account and verify access is denied |
| Unauthorized access | User requests a permission they do not hold | Deny by default and test negative cases |
| Privilege persistence | A role or permission is not removed after a change | Provide explicit revoke operations and test them |
| Tampered or malformed policy file | Invalid JSON or unexpected data is loaded | Validate data before accepting it; fail safely |
| Weak accountability | An administrator changes a role without a trace | Record actor, action, target, result, and timestamp |

## Security assumptions
- The homelab runs on a trusted local machine.
- The operator controls access to the project directory.
- No real employee credentials or production identity data are used.
- Audit logs and JSON files are not tamper-proof in this prototype.

## Out of scope for the three-day showcase
- Production authentication or SSO.
- Real MFA delivery.
- Multi-tenant isolation.
- High availability, distributed deployment, and regulatory certification.
- Protection against a local administrator who can modify application files.

## Review status
Initial design threat model. Update it when the storage model, interfaces, or trust boundaries change.
