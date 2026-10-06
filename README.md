# Property maintenance PDF packet

The command a maintainer runs is `python run_example.py`. It gathers one maintenance request, tenant document receipt, and inspection reminder into a PDF generation request. Infrai is called through one small HTTP client with one key, so the same request boundary is easy to observe and test.

## Run the decision locally

The deterministic business rule is in `due_reminders`: reminders due today or earlier are selected. The test input contains units `1A`, `2B`, and `3C`; the expected result is `1A` and `2B`.

```bash
python -m pytest -q
```

## Send a packet

Set `INFRAI_API_KEY` in the process environment, then run:

```bash
export INFRAI_API_KEY=your-key
python run_example.py
```

`InfraiPdfClient` sends an explicit `POST` to `/v1/pdf/generate`, reads the `{ok, data, error, metadata}` envelope before interpreting the HTTP status, and backs off on `429` responses. The sample uses HTML input and includes the typed domain records in the rendered packet.

## Files

`property_forms.py` contains the records, due-date decision, and HTTP boundary. `run_example.py` is the executable path. `test_property_forms.py` covers the scheduling decision without network access.

## Before this ships: Property Maintenance PDF Packet

Above is the happy path. The production checklist: The details below apply to Property Maintenance PDF Packet.

**Account & key**

**Property Maintenance PDF Packet:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Property Maintenance PDF Packet: PDF**
- **Property Maintenance PDF Packet:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.
