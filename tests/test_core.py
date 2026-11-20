import unittest

from iam_simulator.core import IAMError, IAMStore


class IAMStoreTests(unittest.TestCase):
    def setUp(self):
        self.iam = IAMStore()
        self.iam.create_role("analyst")
        self.iam.grant_permission("analyst", "read")
        self.iam.create_user("alice")
        self.iam.assign_role("alice", "analyst")

    def test_assigned_permission_is_granted(self):
        self.assertTrue(self.iam.check_access("alice", "read"))

    def test_unassigned_permission_is_denied(self):
        self.assertFalse(self.iam.check_access("alice", "delete"))

    def test_unknown_user_is_denied(self):
        self.assertFalse(self.iam.check_access("ghost", "read"))

    def test_disabled_user_is_denied(self):
        self.iam.set_user_active("alice", False)
        self.assertFalse(self.iam.check_access("alice", "read"))

    def test_permission_revocation_takes_effect(self):
        self.iam.revoke_permission("analyst", "read")
        self.assertFalse(self.iam.check_access("alice", "read"))

    def test_role_revocation_takes_effect(self):
        self.iam.revoke_role("alice", "analyst")
        self.assertFalse(self.iam.check_access("alice", "read"))

    def test_empty_username_is_rejected(self):
        with self.assertRaises(IAMError):
            self.iam.create_user("   ")

    def test_audit_events_are_recorded(self):
        self.iam.check_access("alice", "read")
        self.assertTrue(any(event["action"] == "access_check"
                            for event in self.iam.audit_log))


if __name__ == "__main__":
    unittest.main()
