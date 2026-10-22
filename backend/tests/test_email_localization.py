"""The shared email layout and subject follow the recipient's locale.

base.html's footer used to fall back to Spanish for every locale (nothing
set ``footer_sent_by``), and a template send without a subject went out as
``Notificación: <template_key>``. The footer now comes from
``app/core/email/strings.py`` and the subject from the template's own
localized ``title`` block.
"""

from __future__ import annotations

import pytest

from app.core.email.providers.base import EmailResult, EmailStatus
from app.core.email.service import EmailService

CONTEXT = {
    "clinic_name": "Dental Smile",
    "patient_name": "Ana",
    "appointment_date": "21.10.2026.",
    "appointment_time": "10:30",
}


def _service() -> EmailService:
    service = EmailService()
    service._initialize()
    return service


@pytest.mark.parametrize(
    ("locale", "footer"),
    [
        ("sr-Cyrl", "Ову поруку Вам шаље Dental Smile"),
        ("sr-Latn", "Ovu poruku Vam šalje Dental Smile"),
        ("de", "Diese E-Mail wurde von Dental Smile gesendet"),
        ("es", "Este email fue enviado por Dental Smile"),
        # Overlay falls back to its base language, unknown to English.
        ("pt-BR", "Este e-mail foi enviado por Dental Smile"),
        ("xx", "This email was sent by Dental Smile"),
    ],
)
def test_footer_follows_the_locale(locale: str, footer: str) -> None:
    body = _service()._render_template("appointment_reminder", locale, CONTEXT)
    assert body is not None
    assert footer in body
    if locale != "es":
        assert "Este email fue enviado" not in body


def test_explicit_footer_in_context_wins() -> None:
    body = _service()._render_template(
        "appointment_reminder", "en", {**CONTEXT, "footer_sent_by": "Custom footer"}
    )
    assert body is not None
    assert "Custom footer" in body


async def _sent_subject(monkeypatch, **kwargs) -> str:
    from app.config import settings as app_settings

    monkeypatch.setattr(app_settings, "EMAIL_ENABLED", True)
    service = _service()
    captured = {}

    async def fake_send(message, db=None, clinic_id=None):
        captured["subject"] = message.subject
        return EmailResult(status=EmailStatus.SUCCESS, provider="test")

    monkeypatch.setattr(service, "send", fake_send)
    await service.send_templated(to_email="ana@example.com", **kwargs)
    return captured["subject"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("locale", "subject"),
    [
        ("sr-Cyrl", "Подсетник за термин - Dental Smile"),
        ("sr-Latn", "Podsetnik za termin - Dental Smile"),
        ("en", "Appointment reminder - Dental Smile"),
    ],
)
async def test_missing_subject_uses_the_localized_title(monkeypatch, locale, subject) -> None:
    sent = await _sent_subject(
        monkeypatch, template_key="appointment_reminder", context=CONTEXT, locale=locale
    )
    assert sent == subject


@pytest.mark.asyncio
async def test_title_subject_is_plain_text(monkeypatch) -> None:
    sent = await _sent_subject(
        monkeypatch,
        template_key="appointment_reminder",
        context={**CONTEXT, "clinic_name": "Smith & Co"},
        locale="en",
    )
    assert sent == "Appointment reminder - Smith & Co"


@pytest.mark.asyncio
async def test_explicit_subject_wins(monkeypatch) -> None:
    sent = await _sent_subject(
        monkeypatch,
        template_key="appointment_reminder",
        context=CONTEXT,
        subject="Hola {{ patient_name }}",
        locale="sr-Cyrl",
    )
    assert sent == "Hola Ana"


@pytest.mark.asyncio
async def test_template_without_title_falls_back_to_clinic_name(monkeypatch) -> None:
    sent = await _sent_subject(
        monkeypatch,
        template_key="custom",
        context=CONTEXT,
        template_html="<p>{{ patient_name }}</p>",
        locale="en",
    )
    assert sent == "Dental Smile"
