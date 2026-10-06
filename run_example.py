from datetime import date

from property_forms import InfraiPdfClient, InspectionReminder, MaintenanceRequest, TenantDocument, due_reminders


def main() -> None:
    reminders = [InspectionReminder("3B", date(2026, 9, 10), "annual inspection")]
    request = MaintenanceRequest("Mina Chen", "3B", "Leaking kitchen tap", date.today())
    documents = [TenantDocument("Mina Chen", "lease", date.today())]
    print(f"due reminders: {len(due_reminders(reminders, date.today()))}")
    result = InfraiPdfClient().generate(request, documents, reminders)
    print(f"generated PDF response: {result}")


if __name__ == "__main__":
    main()

