"""Test decorators are skipped in signatures."""


class MyClass:
    @classmethod
    def get_query_instance(
        cls,
        query=None,
        search=None,
        exclude_search=None,
        time_field="alarm_time",
        start_time=None,
        end_time=None,
        or_query=None,
        exclude_query=None,
        global_search=None,
        sort=None,
        query_fields=None,
        from_dict=None,
        from_dsl=None,
        permission_request=None,
        using: str | None = None,
        index: str | None = None,
        **kwargs,
    ):
        """Get query instance."""
        if query:
            if search:
                if exclude_search:
                    return None
        return query

    @staticmethod
    def static_method(x, y):
        """Static method."""
        if x > 0:
            return y
        return 0

    @property
    def prop(self):
        """Property."""
        return bool(self)
