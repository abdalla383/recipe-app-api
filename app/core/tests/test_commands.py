"""
Test custom Django management commands.
"""

from unittest.mock import patch
# Used to temporarily replace real functions/objects during testing

# PostgreSQL-specific DB connection error
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
# Lets you run Django commands in Python

from django.db.utils import OperationalError
# Django's own DB error class

from django.test import SimpleTestCase
# Lightweight test class (no database setup)


# Patch the `check` method used in your custom command to simulate DB behavior
@patch(
    'core.management.commands.wait_for_db.Command.check'
)
class CommandTests(SimpleTestCase):
    """Tests for the wait_for_db management command."""

    def test_wait_for_db_ready(self, patched_check):
        """Test: should not wait if the database is ready immediately."""
        # Simulate the DB being ready on first check
        patched_check.return_value = True
        # Run the command
        call_command('wait_for_db')
        # Should call check once with this argument
        patched_check.assert_called_once_with(
            database=['default']
        )

    # Use another patch to fake time.sleep (so tests don't slow down)
    @patch(
        'time.sleep'
    )
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # Simulate 2 psycopg2 errors, 3 Django errors, then success
        patched_check.side_effect = (
            [Psycopg2Error] * 2 +
            [OperationalError] * 3 +
            [True]
        )

        # Run the command — it should retry 6 times
        call_command('wait_for_db')
        # Should call check 6 times
        self.assertEqual(patched_check.call_count, 6)
        # Final call should have this argument
        patched_check.assert_called_with(
            database=['default']
        )
