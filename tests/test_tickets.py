import os
import unittest
from tickets import TicketService


class TestTicketService(unittest.TestCase):
    def setUp(self):
        self.test_csv = "test_run_tickets.csv"
        self.service = TicketService(self.test_csv)

    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_01_create_valid_ticket(self):
        t = self.service.create_ticket("TCK-1", "Server crash", "HIGH", "NEW", "ops")
        self.assertEqual(t["priority"], "HIGH")

    def test_02_invalid_priority_is_rejected(self):
        """Тест требования варианта 3: недопустимый приоритет вызывает ValueError."""
        with self.assertRaises(ValueError):
            self.service.create_ticket("TCK-2", "Glitch", "UNKNOWN_PRIORITY")

    def test_03_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            self.service.create_ticket("TCK-3", "   ", "LOW")

    def test_04_empty_id_rejected(self):
        with self.assertRaises(ValueError):
            self.service.create_ticket("", "Some issue", "NORMAL")

    def test_05_duplicate_id_rejected(self):
        self.service.create_ticket("TCK-5", "Task 1", "NORMAL")
        with self.assertRaises(ValueError):
            self.service.create_ticket("TCK-5", "Task 2", "HIGH")

    def test_06_get_existing_ticket(self):
        self.service.create_ticket("TCK-6", "Check memory", "LOW")
        found = self.service.get_ticket("TCK-6")
        self.assertIsNotNone(found)
        self.assertEqual(found["title"], "Check memory")

    def test_07_get_nonexistent_ticket_returns_none(self):
        self.assertIsNone(self.service.get_ticket("TCK-9999"))

    def test_08_update_status_success(self):
        self.service.create_ticket("TCK-8", "Deploy bug", "CRITICAL", "NEW")
        self.service.update_status("TCK-8", "RESOLVED")
        t = self.service.get_ticket("TCK-8")
        self.assertEqual(t["status"], "RESOLVED")

    def test_09_update_invalid_status_rejected(self):
        self.service.create_ticket("TCK-9", "Bug", "LOW")
        with self.assertRaises(ValueError):
            self.service.update_status("TCK-9", "EXPLODED")

    def test_10_list_tickets_with_filter(self):
        self.service.create_ticket("TCK-10A", "A", "LOW", "NEW")
        self.service.create_ticket("TCK-10B", "B", "HIGH", "CLOSED")
        closed = self.service.list_tickets(status_filter="CLOSED")
        self.assertEqual(len(closed), 1)
        self.assertEqual(closed[0]["ticket_id"], "TCK-10B")

    def test_11_case_insensitivity_priority(self):
        t = self.service.create_ticket("TCK-11", "Network lag", "critical")
        self.assertEqual(t["priority"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()