"""Serbian (Latin) demo seed: a Belgrade clinic that prices in dinars.

``--lang sr-Latn`` seeds Serbian people, clinic and clinical text, and
converts the catalog's EUR reference prices to RSD. The source guard at the
bottom keeps the seed translations complete: every language dict that
carries French must carry Serbian too, or ``t()`` silently falls back to
English in a Serbian demo.
"""

from __future__ import annotations

import ast
from decimal import Decimal
from pathlib import Path

import pytest

from app.seeds.demo_data import (
    get_catalog_price_rate,
    get_clinic_data,
    get_patients_data,
    get_users_data,
    localized_catalog_name,
    set_language,
)

BACKEND = Path(__file__).resolve().parents[1]
SEED_FILES = [
    BACKEND / "app/seeds/demo_data.py",
    BACKEND / "app/seeds/patient_timeline_demo.py",
    BACKEND / "app/modules/catalog/seed.py",
    BACKEND / "app/modules/clinical_notes/seed.py",
    BACKEND / "app/modules/recalls/seed.py",
]


@pytest.fixture
def serbian():
    set_language("sr-Latn")
    try:
        yield
    finally:
        set_language("en")


def test_serbian_demo_is_a_belgrade_clinic_in_dinars(serbian) -> None:
    clinic = get_clinic_data()
    assert clinic["address"]["city"] == "Beograd"
    assert clinic["address"]["country"] == "Srbija"
    assert clinic["currency"] == "RSD"
    assert clinic["timezone"] == "Europe/Belgrade"
    assert clinic["phone"].startswith("+381")
    assert get_catalog_price_rate() == Decimal("117")


@pytest.mark.parametrize("lang", ["en", "es"])
def test_other_demos_keep_the_reference_prices(lang: str) -> None:
    set_language(lang)
    try:
        assert get_catalog_price_rate() is None
    finally:
        set_language("en")


def test_serbian_demo_people_are_serbian(serbian) -> None:
    patients = get_patients_data()
    set_language("en")
    english = {(p["first_name"], p["last_name"]) for p in get_patients_data()}
    set_language("sr-Latn")

    assert len(patients) == 15
    assert not english & {(p["first_name"], p["last_name"]) for p in patients}
    for patient in patients:
        assert patient["phone"].startswith("+381")
        if patient["email"]:
            assert patient["email"].endswith(".rs")
        contact = patient["emergency_contact"]
        if contact:
            assert contact["phone"].startswith("+381")
    assert {u["first_name"] for u in get_users_data()} >= {"Jelena", "Nenad", "Tijana"}


def test_catalog_names_follow_the_demo_language(serbian) -> None:
    assert localized_catalog_name({"es": "Empaste", "sr-Latn": "Plomba"}) == "Plomba"
    # Not translated → English before the Spanish-first priority order.
    assert localized_catalog_name({"es": "Empaste", "en": "Filling"}) == "Filling"
    assert localized_catalog_name(None) is None


def _language_dicts(path: Path):
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Dict):
            keys = {k.value for k in node.keys if isinstance(k, ast.Constant)}
            if {"en", "fr"} <= keys:
                yield node.lineno, keys


@pytest.mark.parametrize("path", SEED_FILES, ids=lambda p: p.name)
def test_every_seed_translation_has_serbian(path: Path) -> None:
    missing = [line for line, keys in _language_dicts(path) if "sr-Latn" not in keys]
    assert not missing, f"{path.name}: language dicts without sr-Latn at lines {missing}"
