"""Locales the generated PDFs accept (issues #422, #441).

The download buttons send the viewer's UI language, so a PDF endpoint that
only validates ``es|en`` answers 422 in eight of the ten languages the app
ships — a dead button with no message. Every host locale is accepted
instead: labels fall back to English where a module has not translated
them, while amounts and dates still use the locale's own separators.

Both label sets and the Babel locale map live here rather than in one
module, because the list is a property of the host's ``i18n.locales``
(frontend/nuxt.config.ts) and every module that renders a PDF needs the
same one. A test guards the two against each other.
"""

from __future__ import annotations

from datetime import date, datetime

PDF_LOCALES: tuple[str, ...] = (
    "es",
    "en",
    "ta",
    "te",
    "hi",
    "fr",
    "pt",
    "pt-BR",
    "de",
    "hu",
    "pl",
    "it",
    "ar",
    "sr-Cyrl",
    "sr-Latn",
)
PDF_LOCALE_PATTERN = "^(" + "|".join(PDF_LOCALES) + ")$"

# UI language -> Babel locale for money and dates. Tamil and Telugu clinics are in
# India, so their amounts follow en_IN grouping.
LOCALE_BY_LANG: dict[str, str] = {
    "es": "es_ES",
    "en": "en_US",
    "ta": "en_IN",
    "te": "en_IN",
    "hi": "hi_IN",
    "fr": "fr_FR",
    "pt": "pt_PT",
    "pt-BR": "pt_BR",
    "de": "de_DE",
    "hu": "hu_HU",
    "pl": "pl_PL",
    "it": "it_IT",
    "ar": "ar",
    "sr-Cyrl": "sr_Cyrl_RS",
    "sr-Latn": "sr_Latn_RS",
}


# Date patterns printed on the PDFs. Day/month/year with slashes unless the
# language writes dates its own way; the time, where shown, is always HH:MM.
DEFAULT_DATE_FORMAT = "%d/%m/%Y"
DATE_FORMAT_BY_LANG: dict[str, str] = {
    "de": "%d.%m.%Y",
    "hu": "%Y. %m. %d.",
    "pl": "%d.%m.%Y",
    "sr-Cyrl": "%d.%m.%Y.",
    "sr-Latn": "%d.%m.%Y.",
}


def format_pdf_date(value: date, locale: str) -> str:
    return value.strftime(DATE_FORMAT_BY_LANG.get(locale, DEFAULT_DATE_FORMAT))


def format_pdf_datetime(value: datetime, locale: str) -> str:
    return f"{format_pdf_date(value, locale)} {value.strftime('%H:%M')}"
