from io import StringIO

import pytest

from p_ast.exporter import CollectionExporter
from p_ast.plugins.env_var import EnvVarHub


@pytest.fixture
def exporter():
    return CollectionExporter()


@pytest.fixture
def hub(exporter):
    return EnvVarHub(exporter=exporter)


@pytest.fixture
def check(exporter, hub):
    def do(code: str):
        file = StringIO(code)
        file.name = "anonymous.py"
        hub.run([file])
        return exporter.get_vars()

    return do


@pytest.fixture
def check_one(check):
    def do(code: str):
        exported = check(code)
        assert len(exported) == 1
        return exported[0]

    return do


class TestEnvVarHub:

    @pytest.mark.parametrize(
        "import_statement, statement_prefix",
        [
            ("import os", "os."),
            ("from os import *", ""),
            ("from other_module import *", "os."),
            ("from other_module import *", ""),
        ],
    )
    @pytest.mark.parametrize(
        "statement, name, expected_value1, expected_cast1",
        [
            ("getenv('KEY')", "KEY", "", ""),
            ("getenv('KEY', 'default')", "KEY", "'default'", ""),
            ("environ['KEY']", "KEY", "", ""),
            ("environ.get('KEY')", "KEY", "", ""),
            ("environ.get('KEY', 'default')", "KEY", "'default'", ""),
        ],
    )
    @pytest.mark.parametrize(
        "statement_template, expected_value2, expected_cast2",
        [
            ("{statement}", "", ""),
            ("[{statement}]", "", ""),
            ("VALUE = {statement}", "", ""),
            ("int({statement})", "", "int"),
            ("int({statement}) or 1", "1", "int"),
            ("int({statement} or 1)", "1", "int"),
        ],
    )
    def test_os_module_related(
        self,
        check_one,
        import_statement,
        statement_prefix,
        statement,
        name,
        expected_value1,
        expected_cast1,
        expected_value2,
        expected_cast2,
        statement_template,
    ):
        real_statement = f"{statement_prefix}{statement}"

        exported = check_one(
            "\n".join(
                [
                    import_statement,
                    statement_template.format(statement=real_statement),
                ]
            )
        )

        assert exported.name == name
        assert exported.value == expected_value1 or expected_value2
        assert exported.cast == expected_cast1 or expected_cast2
        assert exported.statement() == real_statement
