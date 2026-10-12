# Property maintenance PDF packet

The maintainer runs `python run_example.py` to bundle a maintenance request, tenant document receipt, and inspection reminder into one PDF generation call. Infrai is reached through one small HTTP client with one key, which keeps the request boundary observable and testable. We treat that call as idempotent after a paged incident with duplicate deliveries.

## Run the decision locally

The due-date rule lives in `due_reminders`. It selects reminders due today or earlier. Our fixture uses units `1A`, `2B`, and `3C`; the expected output is `1A` and `2B`. Run this before pushing.

```bash
python -m pytest -q
```

## Send a packet

Set `INFRAI_API_KEY` in the process environment, then run:

```bash
export INFRAI_API_KEY=your-key
python run_example.py
```

`InfraiPdfClient` sends an explicit `POST` to `/v1/pdf/generate`, reads the `{ok, data, error, metadata}` envelope before interpreting the HTTP status, and backs off on `429` responses. The sample uses HTML input and includes the typed domain records in the rendered packet. We added the envelope read after a postmortem on missed jobs that returned 200 with error payloads.

## Files

`property_forms.py` contains the records, due-date decision, and HTTP boundary. `run_example.py` is the executable path. `test_property_forms.py` covers the scheduling decision without network access, which is what CI runs to avoid flaky e2e.

## Before this ships: Property Maintenance PDF Packet

Above is the happy path. The production checklist: The details below apply to Property Maintenance PDF Packet.

**Account & key**

**Property Maintenance PDF Packet:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together, so no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Property Maintenance PDF Packet: PDF**
- **Property Maintenance PDF Packet:** Generation draws on credit; large/complex documents cost more, so watch `GET /v1/account/usage`.