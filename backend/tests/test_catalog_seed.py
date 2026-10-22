"""Tests for the catalog seeder.

Verifies that the seeded catalog includes globally-scoped treatments (cleaning,
whitening, whole-arch prosthesis, etc.) and that every seeded item uses one of
the four valid `treatment_scope` values.
"""

from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.auth.models import Clinic
from app.modules.catalog.models import TreatmentCatalogItem
from app.modules.catalog.seed import TREATMENTS, convert_reference_price, seed_catalog

VALID_SCOPES = {"tooth", "multi_tooth", "global_mouth", "global_arch"}


@pytest.fixture
async def seeded_clinic(db_session: AsyncSession) -> Clinic:
    clinic = Clinic(
        id=uuid4(),
        name="Seed Clinic",
        tax_id="B44444444",
        address={"street": "x", "city": "y"},
        settings={"slot_duration_min": 15},
    )
    db_session.add(clinic)
    await db_session.flush()
    await seed_catalog(db_session, clinic.id)
    await db_session.commit()
    return clinic


@pytest.mark.asyncio
async def test_seed_creates_global_mouth_items(
    db_session: AsyncSession, seeded_clinic: Clinic
) -> None:
    result = await db_session.execute(
        select(TreatmentCatalogItem).where(
            TreatmentCatalogItem.clinic_id == seeded_clinic.id,
            TreatmentCatalogItem.treatment_scope == "global_mouth",
        )
    )
    items = list(result.scalars().all())
    codes = {i.internal_code for i in items}

    # Essential globals that should always be seeded.
    assert "PREV-CLEAN" in codes
    assert "PREV-FLUOR" in codes
    assert "PREV-CHECKUP" in codes
    assert any(c.startswith("EST-BLAN") for c in codes), (
        "At least one whitening item should be global_mouth"
    )


@pytest.mark.asyncio
async def test_seed_creates_global_arch_items(
    db_session: AsyncSession, seeded_clinic: Clinic
) -> None:
    result = await db_session.execute(
        select(TreatmentCatalogItem).where(
            TreatmentCatalogItem.clinic_id == seeded_clinic.id,
            TreatmentCatalogItem.treatment_scope == "global_arch",
        )
    )
    items = list(result.scalars().all())
    codes = {i.internal_code for i in items}

    assert "REST-SPLINT-OCC" in codes
    assert "PROT-FULL-SUP" in codes
    assert "PROT-FULL-INF" in codes


@pytest.mark.asyncio
async def test_seed_creates_multi_tooth_items(
    db_session: AsyncSession, seeded_clinic: Clinic
) -> None:
    result = await db_session.execute(
        select(TreatmentCatalogItem).where(
            TreatmentCatalogItem.clinic_id == seeded_clinic.id,
            TreatmentCatalogItem.treatment_scope == "multi_tooth",
        )
    )
    items = list(result.scalars().all())
    codes = {i.internal_code for i in items}

    # All bridges must be multi_tooth.
    assert "REST-BRIDGE-MC" in codes
    assert "REST-BRIDGE-ZIR" in codes


@pytest.mark.asyncio
async def test_seed_items_have_valid_scope(db_session: AsyncSession, seeded_clinic: Clinic) -> None:
    result = await db_session.execute(
        select(TreatmentCatalogItem).where(
            TreatmentCatalogItem.clinic_id == seeded_clinic.id,
        )
    )
    items = list(result.scalars().all())
    assert items, "Seeder should create items"
    for item in items:
        assert item.treatment_scope in VALID_SCOPES, (
            f"{item.internal_code} has invalid scope {item.treatment_scope}"
        )


@pytest.mark.asyncio
async def test_seed_endpoint_is_idempotent_repair_path(
    client, auth_headers: dict, test_clinic: Clinic, db_session: AsyncSession
) -> None:
    """``POST /catalog/seed`` fills an empty clinic and is a no-op afterwards."""
    from app.modules.catalog.models import TreatmentCategory

    r = await client.post("/api/v1/catalog/seed", headers=auth_headers)
    assert r.status_code == 200, r.text
    first = r.json()["data"]
    assert first["categories"] > 0 and first["items"] > 100 and first["vat_types"] >= 1
    assert first["vat_types"] == 1  # test_clinic has no country → generic preset (exempt only)

    cats = await db_session.scalar(
        select(func.count())
        .select_from(TreatmentCategory)
        .where(TreatmentCategory.clinic_id == test_clinic.id)
    )
    assert cats == first["categories"]

    r = await client.post("/api/v1/catalog/seed", headers=auth_headers)
    assert r.status_code == 200
    second = r.json()["data"]
    assert second == {"categories": 0, "items": 0, "vat_types": 0}


async def _fresh_clinic(db_session: AsyncSession) -> Clinic:
    clinic = Clinic(
        id=uuid4(),
        name="Price Clinic",
        tax_id="B55555555",
        address={"street": "x", "city": "y"},
        settings={"slot_duration_min": 15},
    )
    db_session.add(clinic)
    await db_session.flush()
    return clinic


def _reference_items() -> dict[str, dict]:
    return {t["internal_code"]: t for items in TREATMENTS.values() for t in items}


async def _seeded_items(db_session: AsyncSession, clinic: Clinic) -> list[TreatmentCatalogItem]:
    result = await db_session.execute(
        select(TreatmentCatalogItem)
        .options(selectinload(TreatmentCatalogItem.sessions))
        .where(TreatmentCatalogItem.clinic_id == clinic.id)
    )
    return list(result.scalars().all())


@pytest.mark.asyncio
async def test_price_rate_converts_every_reference_price(db_session: AsyncSession) -> None:
    """A dinar demo clinic gets the EUR reference prices converted, not 60 RSD fillings."""
    rate = Decimal("117")
    clinic = await _fresh_clinic(db_session)
    await seed_catalog(db_session, clinic.id, price_rate=rate)
    reference = _reference_items()

    items = await _seeded_items(db_session, clinic)
    assert items
    for item in items:
        ref = reference[item.internal_code]
        assert item.default_price == convert_reference_price(ref["default_price"], rate)
        for surface, price in (ref.get("surface_prices") or {}).items():
            assert item.surface_prices[surface] == f"{convert_reference_price(price, rate):.2f}"
        for key, price in (ref.get("pricing_config") or {}).items():
            if isinstance(price, int | float | Decimal) and not isinstance(price, bool):
                assert item.pricing_config[key] == int(convert_reference_price(price, rate))
        ref_sessions = ref.get("sessions") or []
        for session, ref_session in zip(
            sorted(item.sessions, key=lambda s: s.sequence), ref_sessions, strict=True
        ):
            assert session.default_price == convert_reference_price(
                ref_session["default_price"], rate
            )


@pytest.mark.asyncio
async def test_without_prices_every_price_is_zero(db_session: AsyncSession) -> None:
    clinic = await _fresh_clinic(db_session)
    await seed_catalog(db_session, clinic.id, with_prices=False)

    for item in await _seeded_items(db_session, clinic):
        assert item.default_price == 0
        assert all(Decimal(v) == 0 for v in (item.surface_prices or {}).values())
        assert all(s.default_price == 0 for s in item.sessions)


def test_reference_price_rounds_to_hundreds() -> None:
    rate = Decimal("117")
    assert convert_reference_price(Decimal("30.00"), rate) == Decimal("3500")
    assert convert_reference_price("15.00", rate) == Decimal("1800")
    assert convert_reference_price(400, rate) == Decimal("46800")
    assert convert_reference_price("0.00", rate) == 0
