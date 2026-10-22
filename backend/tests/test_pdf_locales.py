"""The PDF locale list must cover every language the app ships (#422, #441).

A locale the host offers but the PDF endpoints reject turns "Download PDF"
into a 422 with no message, which is how #422 and #441 were found in
production rather than in review.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

import pytest

from app.config import settings
from app.core.pdf_locales import (
    LOCALE_BY_LANG,
    PDF_LOCALE_PATTERN,
    PDF_LOCALES,
    format_pdf_date,
    format_pdf_datetime,
)


def _host_locales() -> set[str]:
    # CI checks out the whole repo; the dev container mounts the host
    # frontend at DENTALPIN_FRONTEND_ROOT instead.
    candidates = (
        Path(settings.DENTALPIN_FRONTEND_ROOT) / "nuxt.config.ts",
        Path(__file__).resolve().parents[2] / "frontend" / "nuxt.config.ts",
    )
    nuxt_config = next((c for c in candidates if c.is_file()), None)
    if nuxt_config is None:
        pytest.skip("host frontend not reachable from here")
    i18n_block = nuxt_config.read_text().split("i18n: {", 1)[1].split("defaultLocale", 1)[0]
    # Two-letter codes (`pt`), region overlays (`pt-BR`) and script
    # variants (`sr-Latn`). The script form was missed before, so Serbian
    # shipped in the UI while every "Download PDF" answered 422.
    return set(re.findall(r"code: '([a-z]{2}(?:-[A-Z]{2}|-[A-Z][a-z]{3})?)'", i18n_block))


def test_every_host_language_is_an_accepted_pdf_locale() -> None:
    ui_locales = _host_locales()
    assert ui_locales, "could not read the host locales from nuxt.config.ts"
    assert ui_locales <= set(PDF_LOCALES), ui_locales - set(PDF_LOCALES)


def test_every_accepted_locale_has_a_babel_locale_and_matches_the_pattern() -> None:
    for locale in PDF_LOCALES:
        assert re.match(PDF_LOCALE_PATTERN, locale), locale
        assert locale in LOCALE_BY_LANG, locale
    assert not re.match(PDF_LOCALE_PATTERN, "xx")


@pytest.mark.parametrize(
    ("locale", "expected"),
    [
        ("es", "22/10/2026"),
        ("en", "22/10/2026"),
        ("de", "22.10.2026"),
        ("pl", "22.10.2026"),
        ("hu", "2026. 10. 22."),
        ("sr-Cyrl", "22.10.2026."),
        ("sr-Latn", "22.10.2026."),
    ],
)
def test_pdf_dates_follow_the_locale(locale: str, expected: str) -> None:
    assert format_pdf_date(date(2026, 10, 22), locale) == expected


def test_pdf_datetimes_append_the_time() -> None:
    assert format_pdf_datetime(datetime(2026, 10, 22, 9, 5), "sr-Latn") == "22.10.2026. 09:05"
