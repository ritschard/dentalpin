"""Localized strings the shared email layout (``templates/email/base.html``) needs.

Per-template copy lives in each locale's template files; only the text the
base layout itself renders belongs here. Every communication locale must have
an entry (guarded by ``tests/test_email_template_parity.py``); an unknown
locale falls back to its base language, then to English.
"""

from __future__ import annotations

FOOTER_SENT_BY: dict[str, str] = {
    "es": "Este email fue enviado por {clinic_name}",
    "en": "This email was sent by {clinic_name}",
    "fr": "Cet e-mail vous a été envoyé par {clinic_name}",
    "pt": "Este e-mail foi enviado por {clinic_name}",
    "de": "Diese E-Mail wurde von {clinic_name} gesendet",
    "hu": "Ezt az e-mailt a(z) {clinic_name} küldte",
    "pl": "Ten e-mail został wysłany przez {clinic_name}",
    "it": "Questa email è stata inviata da {clinic_name}",
    "ta": "இந்த மின்னஞ்சல் {clinic_name} மூலம் அனுப்பப்பட்டது",
    "te": "ఈ ఇమెయిల్ {clinic_name} ద్వారా పంపబడింది",
    "hi": "यह ईमेल {clinic_name} द्वारा भेजा गया है",
    "ar": "أُرسلت هذه الرسالة من {clinic_name}",
    "sr-Cyrl": "Ову поруку Вам шаље {clinic_name}",
    "sr-Latn": "Ovu poruku Vam šalje {clinic_name}",
}


def footer_sent_by(locale: str, clinic_name: str | None) -> str:
    template = (
        FOOTER_SENT_BY.get(locale)
        or FOOTER_SENT_BY.get(locale.split("-")[0])
        or FOOTER_SENT_BY["en"]
    )
    return template.format(clinic_name=clinic_name or "DentalPin")
