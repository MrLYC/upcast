"""Test file with real multi-line signatures."""


def implement_rewrite_decision(intention, query, contexts_moderately_relevant, qa_results):
    """实施重写决策"""
    # Some code with complexity
    if intention:
        if query:
            if contexts_moderately_relevant:
                if qa_results:
                    for item in qa_results:
                        if item:
                            return True
    return False


def another_long_signature(
    param1: str, param2: int, param3: dict, param4: list, optional1: bool = True, optional2: str = "default"
) -> dict:
    """Another function with long signature."""
    if param2 > 0:
        if param3:
            if param4:
                return {"result": param1}
    return {}
