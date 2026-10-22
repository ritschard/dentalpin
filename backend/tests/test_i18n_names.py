"""Shared catalog-name resolver — priority chain + any-non-empty fallback."""

from app.core.i18n_names import CATALOG_NAME_PRIORITY, catalog_name


def test_prefers_priority_order():
    names = {"en": "Filling", "es": "Empaste", "ar": "حشوة"}
    assert catalog_name(names) == "Empaste"


def test_arabic_only_item_resolves():
    # Items created under a core-only locale must not degrade to None.
    assert catalog_name({"ar": "تبييض الأسنان"}) == "تبييض الأسنان"


def test_arabic_beats_catchall_when_present():
    names = {"de": "Bleaching", "ar": "تبييض"}
    assert catalog_name(names) == "Bleaching"
    names2 = {"nl": "Bleken", "ar": "تبييض"}
    # 'ar' is in the priority chain; 'nl' only via catch-all
    assert catalog_name(names2) == "تبييض"


def test_empty_strings_skipped():
    assert catalog_name({"es": "", "en": "  ", "fr": "Détartrage"}) == "Détartrage"
    assert catalog_name({"es": "", "en": ""}) is None


def test_none_and_non_dict_inputs():
    assert catalog_name(None) is None
    assert catalog_name({}) is None
    assert catalog_name("not-a-dict") is None


def test_priority_chain_covers_known_locales():
    """CATALOG_NAME_PRIORITY must list the core locales; future locales
    are added by appending to the tuple — this test pins the known set
    without breaking when a new locale is added."""
    for lang in ("es", "en", "fr", "pt", "ta", "te", "hi", "de", "hu", "it", "pl"):
        assert lang in CATALOG_NAME_PRIORITY, f"{lang} missing from CATALOG_NAME_PRIORITY"


def test_locale_wins_over_the_priority_order():
    names = {"es": "Empaste", "en": "Filling", "sr-Latn": "Plomba"}
    assert catalog_name(names, "sr-Latn") == "Plomba"
    assert catalog_name(names) == "Empaste"


def test_locale_falls_back_to_its_own_language_first():
    """A Cyrillic reader gets the Latin name before English or Spanish."""
    names = {"es": "Empaste", "en": "Filling", "sr-Latn": "Plomba"}
    assert catalog_name(names, "sr-Cyrl") == "Plomba"
    assert catalog_name({"es": "Empaste", "pt": "Obturação"}, "pt-BR") == "Obturação"


def test_untranslated_locale_falls_back_to_english_before_spanish():
    names = {"es": "Empaste", "en": "Filling"}
    assert catalog_name(names, "de") == "Filling"
    assert catalog_name({"es": "Empaste"}, "de") == "Empaste"
