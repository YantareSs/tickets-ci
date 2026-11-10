import csv
import os
import sys

ALLOWED_PRIORITIES = {"LOW", "NORMAL", "HIGH", "CRITICAL"}
ALLOWED_STATUSES = {"NEW", "IN_PROGRESS", "RESOLVED", "CLOSED"}


class TicketService:
    def __init__(self, storage_path="tickets.csv"):
        self.storage_path = storage_path
        self._init_storage()

    def _init_storage(self):
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ticket_id", "title", "priority", "status", "author"])

    def create_ticket(self, ticket_id, title, priority, status="NEW", author="system"):
        if not ticket_id or not str(ticket_id).strip():
            raise ValueError("Ticket ID cannot be empty.")
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")

        priority_norm = priority.upper().strip() if priority else ""
        if priority_norm not in ALLOWED_PRIORITIES:
            raise ValueError(f"Invalid priority '{priority}'. Allowed: {ALLOWED_PRIORITIES}")

        status_norm = status.upper().strip() if status else "NEW"
        if status_norm not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Allowed: {ALLOWED_STATUSES}")

        if self.get_ticket(ticket_id) is not None:
            raise ValueError(f"Ticket with ID '{ticket_id}' already exists.")

        with open(self.storage_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([str(ticket_id).strip(), title.strip(), priority_norm, status_norm, author.strip()])

        return {
            "ticket_id": str(ticket_id).strip(),
            "title": title.strip(),
            "priority": priority_norm,
            "status": status_norm,
            "author": author.strip(),
        }

    def get_ticket(self, ticket_id):
        if not os.path.exists(self.storage_path):
            return None
        with open(self.storage_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["ticket_id"] == str(ticket_id).strip():
                    return row
        return None

    def list_tickets(self, status_filter=None):
        results = []
        if not os.path.exists(self.storage_path):
            return results
        with open(self.storage_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if status_filter is None or row["status"] == status_filter.upper().strip():
                    results.append(row)
        return results

    def update_status(self, ticket_id, new_status):
        status_norm = new_status.upper().strip()
        if status_norm not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'.")
        tickets = []
        found = False
        with open(self.storage_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames
            for row in reader:
                if row["ticket_id"] == str(ticket_id).strip():
                    row["status"] = status_norm
                    found = True
                tickets.append(row)
        if not found:
            raise KeyError(f"Ticket '{ticket_id}' not found.")
        with open(self.storage_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(tickets)
        return True


def main():
    print("Tickets Service CLI v1.0.0")


if __name__ == "__main__":
    main()