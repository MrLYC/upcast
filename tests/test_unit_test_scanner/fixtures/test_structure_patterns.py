import pytest

from myapp.service import build_payload


@pytest.fixture
def test_payload():
    payload = build_payload()
    assert payload
    return payload


@pytest.mark.slow
@pytest.mark.parametrize("value", [1, 2])
def test_marked_values(value, test_payload):
    result = build_payload()
    assert result
    assert value > 0


class TestFeature:
    def test_targeted(self, test_payload):
        assert build_payload()
