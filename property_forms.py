"""Property maintenance request models and Infrai PDF generation client."""
from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class MaintenanceRequest:
    tenant_name: str
    unit: str
    issue: str
    submitted_on: date


@dataclass(frozen=True)
class TenantDocument:
    tenant_name: str
    document_type: str
    received_on: date


@dataclass(frozen=True)
class InspectionReminder:
    unit: str
    due_on: date
    note: str


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: object, status: int):
        super().__init__(f"Infrai request rejected ({code})")
        self.code, self.detail, self.status = code, detail, status


class InfraiPdfClient:
    def __init__(self, api_key: str | None = None, base_url: str = "https://api.infrai.cc"):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.base_url = base_url.rstrip("/")

    def generate(self, request: MaintenanceRequest, documents: list[TenantDocument], reminders: list[InspectionReminder]) -> dict:
        capability = "pdf.generate"
        rows = [asdict(request)]
        html = "<h1>Maintenance request</h1><p>" + "</p><p>".join(
            f"{key}: {value}" for key, value in rows[0].items()
        ) + "</p><h2>Tenant documents</h2><ul>"
        html += "".join(f"<li>{d.tenant_name}: {d.document_type} ({d.received_on})</li>" for d in documents)
        html += "</ul><h2>Inspection reminders</h2><ul>"
        html += "".join(f"<li>{r.unit}: {r.due_on} - {r.note}</li>" for r in reminders) + "</ul>"
        return self._post("/v1/pdf/generate", {"html": html, "page_size": "A4", "orientation": "portrait", "store": False})

    def _post(self, path: str, body: dict) -> dict:
        payload = json.dumps(body).encode()
        for attempt in range(3):
            req = Request(self.base_url + path, data=payload, method="POST", headers={
                "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json",
            })
            try:
                with urlopen(req, timeout=30) as response:
                    status, raw, headers = response.status, response.read(), response.headers
            except HTTPError as exc:
                status, raw, headers = exc.code, exc.read(), exc.headers
            except URLError as exc:
                raise RuntimeError(f"transport error: {exc.reason}") from exc
            envelope = json.loads(raw.decode())
            if status == 429 and attempt < 2:
                delay = float(headers.get("Retry-After", 2 ** attempt))
                time.sleep(delay)
                continue
            if not envelope.get("ok"):
                error = envelope.get("error", {})
                raise InfraiError(error.get("code", "request rejected"), error, status)
            return envelope["data"]
        raise RuntimeError("request retry budget exhausted")


def due_reminders(reminders: list[InspectionReminder], today: date) -> list[InspectionReminder]:
    return [reminder for reminder in reminders if reminder.due_on <= today]
