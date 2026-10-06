from datetime import date

from property_forms import InspectionReminder, due_reminders


def test_due_reminders_selects_today_and_overdue_items():
    reminders = [
        InspectionReminder("1A", date(2026, 9, 6), "overdue"),
        InspectionReminder("2B", date(2026, 9, 7), "today"),
        InspectionReminder("3C", date(2026, 9, 8), "future"),
    ]
    assert [item.unit for item in due_reminders(reminders, date(2026, 9, 7))] == ["1A", "2B"]

