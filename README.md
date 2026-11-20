# IAM Policy Simulator — Security Homelab

An educational Identity and Access Management (IAM) project built to explore identity lifecycle, role-based access control (RBAC), least privilege, access decisions, and auditability.

This repository is a **local learning homelab**, not a production IAM platform or identity provider.

## Current capabilities

The new testable core in `src/iam_simulator/core.py` currently supports:

- Create users and roles.
- Grant and revoke role permissions.
- Assign and revoke roles from users.
- Enable or disable user accounts.
- Make deny-by-default RBAC access decisions.
- Record basic audit events for administrative actions and access checks.
- Review a user's effective permissions.

The original interactive script remains in `IAM PS CODE` as the starting point from which this project is evolving.

## Run the tests

Requires Python 3.10 or later.

From the repository root:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Example: use the IAM core

```python
from iam_simulator.core import IAMStore

iam = IAMStore()
iam.create_role("analyst")
iam.grant_permission("analyst", "read")
iam.create_user("alice")
iam.assign_role("alice", "analyst")

print(iam.check_access("alice", "read"))    # True
print(iam.check_access("alice", "delete"))  # False
```

## Project documentation

- [Three-day homelab roadmap](ROADMAP.md)
- [Baseline assessment](docs/baseline-assessment.md)
- [Initial threat model](docs/threat-model.md)

## Scope and limitations

- RBAC is currently the authorization model; ABAC and explicit deny policies are not implemented.
- The current core stores data in memory. Persistence and robust policy-file validation are planned.
- Audit events are held in memory and are not tamper-proof.
- Authentication, MFA, SSO, production PAM, multi-tenancy, and cloud deployment are not implemented.
- This prototype must not be used to control access to real organisational systems or sensitive data.

## Learning approach

Each feature should be accompanied by tests, evidence, and a short explanation of the security problem it addresses. Only verified, implemented capabilities will be presented as completed.

## License

See [LICENSE](LICENSE).
