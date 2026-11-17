"""Demonstrate bugs only within intentionally vulnerable in-memory lab code."""
import unittest

from labs.idor_demo import vulnerable_get_document, secure_get_document
from labs.sql_injection_demo import (
    make_lab_database,
    vulnerable_user_lookup,
    secure_user_lookup,
)


class TrainingLabsTests(unittest.TestCase):
    def test_idor_demonstrates_missing_owner_check(self):
        exposed = vulnerable_get_document("doc-200", "alice")
        self.assertEqual(exposed["owner"], "bob")
        self.assertIsNone(secure_get_document("doc-200", "alice"))
        self.assertEqual(secure_get_document("doc-100", "alice")["owner"], "alice")

    def test_sql_injection_and_prepared_statement(self):
        connection = make_lab_database()
        try:
            lab_payload = "' OR '1'='1"
            self.assertEqual(
                vulnerable_user_lookup(connection, lab_payload),
                ["alice", "bob"],
            )
            self.assertEqual(secure_user_lookup(connection, lab_payload), [])
            self.assertEqual(secure_user_lookup(connection, "alice"), ["alice"])
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
