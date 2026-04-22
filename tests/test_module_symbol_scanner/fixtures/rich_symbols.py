"""Rich symbol fixture for Task 7 module symbol enrichment tests."""


def build_payload(user_id: int, verbose=False, *extras, limit: int = 10, **options):
    """Build a payload for downstream processing."""
    return {
        "user_id": user_id,
        "verbose": verbose,
        "extras": extras,
        "limit": limit,
        "options": options,
    }


class Service:
    """Service with methods that should expose rich metadata."""

    @classmethod
    def from_config(cls, config, retries: int = 3):
        return cls()

    @decorator("audit")
    def run(self, payload, timeout: float = 1.5):
        return payload
