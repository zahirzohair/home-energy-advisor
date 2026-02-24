from app.models.home import Home, HeatingType, InsulationLevel
from app.services.llm_service import MockLLMProvider, _parse_recommendations


def test_mock_provider_returns_list():
    provider = MockLLMProvider()
    home = Home(
        id=1,
        size_sqm=100,
        year_built=1990,
        heating_type=HeatingType.GAS,
        insulation=InsulationLevel.PARTIAL,
        notes=None,
    )
    result = provider.generate_advice(home)
    assert isinstance(result, list)
    assert len(result) >= 1
    assert all(isinstance(r, str) for r in result)


def test_parse_recommendations_numbered():
    text = "1. First tip\n2. Second tip\n3. Third tip"
    assert _parse_recommendations(text) == ["First tip", "Second tip", "Third tip"]


def test_parse_recommendations_bullets():
    text = "• One\n• Two"
    assert _parse_recommendations(text) == ["One", "Two"]
