"""Core logic for the IAM Policy Simulator homelab.

This module deliberately contains no interactive input/output so it can be tested.
It is an educational RBAC prototype, not a production IAM service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class IAMError(ValueError):
    """Raised when an IAM operation uses invalid or unknown data."""


class IAMStore:
    """In-memory identities, roles, permissions, and audit events."""

    def __init__(self) -> None:
        self.users: dict[str, dict[str, Any]] = {}
        self.roles: dict[str, set[str]] = {}
        self.audit_log: list[dict[str, str]] = []

    @staticmethod
    def _required(value: str, field: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise IAMError(f"{field} cannot be empty")
        return cleaned

    def _audit(self, actor: str, action: str, target: str, result: str) -> None:
        self.audit_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "actor": actor,
            "action": action,
            "target": target,
            "result": result,
        })

    def create_user(self, username: str, actor: str = "system") -> None:
        username = self._required(username, "Username")
        if username in self.users:
            raise IAMError(f"User already exists: {username}")
        self.users[username] = {"roles": set(), "active": True}
        self._audit(actor, "create_user", username, "success")

    def set_user_active(self, username: str, active: bool, actor: str = "admin") -> None:
        username = self._required(username, "Username")
        if username not in self.users:
            raise IAMError(f"Unknown user: {username}")
        if not isinstance(active, bool):
            raise IAMError("Account status must be boolean")
        self.users[username]["active"] = active
        self._audit(actor, "set_user_active", username, "enabled" if active else "disabled")

    def create_role(self, role: str, actor: str = "admin") -> None:
        role = self._required(role, "Role")
        if role in self.roles:
            raise IAMError(f"Role already exists: {role}")
        self.roles[role] = set()
        self._audit(actor, "create_role", role, "success")

    def grant_permission(self, role: str, permission: str, actor: str = "admin") -> None:
        role = self._required(role, "Role")
        permission = self._required(permission, "Permission")
        if role not in self.roles:
            raise IAMError(f"Unknown role: {role}")
        self.roles[role].add(permission)
        self._audit(actor, "grant_permission", f"{role}:{permission}", "success")

    def revoke_permission(self, role: str, permission: str, actor: str = "admin") -> None:
        role = self._required(role, "Role")
        permission = self._required(permission, "Permission")
        if role not in self.roles or permission not in self.roles[role]:
            raise IAMError("Role or permission assignment not found")
        self.roles[role].remove(permission)
        self._audit(actor, "revoke_permission", f"{role}:{permission}", "success")

    def assign_role(self, username: str, role: str, actor: str = "admin") -> None:
        username = self._required(username, "Username")
        role = self._required(role, "Role")
        if username not in self.users:
            raise IAMError(f"Unknown user: {username}")
        if role not in self.roles:
            raise IAMError(f"Unknown role: {role}")
        self.users[username]["roles"].add(role)
        self._audit(actor, "assign_role", f"{username}:{role}", "success")

    def revoke_role(self, username: str, role: str, actor: str = "admin") -> None:
        username = self._required(username, "Username")
        role = self._required(role, "Role")
        if username not in self.users or role not in self.users[username]["roles"]:
            raise IAMError("User-role assignment not found")
        self.users[username]["roles"].remove(role)
        self._audit(actor, "revoke_role", f"{username}:{role}", "success")

    def check_access(self, username: str, permission: str, actor: str = "system") -> bool:
        username = self._required(username, "Username")
        permission = self._required(permission, "Permission")
        user = self.users.get(username)
        if user is None or not user["active"]:
            self._audit(actor, "access_check", f"{username}:{permission}", "denied")
            return False

        allowed = any(
            permission in self.roles.get(role, set())
            for role in user["roles"]
        )
        self._audit(actor, "access_check", f"{username}:{permission}",
                    "granted" if allowed else "denied")
        return allowed

    def review_user(self, username: str) -> dict[str, Any]:
        username = self._required(username, "Username")
        if username not in self.users:
            raise IAMError(f"Unknown user: {username}")
        assigned_roles = sorted(self.users[username]["roles"])
        permissions = sorted({
            permission
            for role in assigned_roles
            for permission in self.roles.get(role, set())
        })
        return {
            "username": username,
            "active": self.users[username]["active"],
            "roles": assigned_roles,
            "effective_permissions": permissions,
        }
