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

        return exporter.get_merged_vars()

    return do


@pytest.fixture
def check_one(check):
    def do(code: str):
        exported = check(code)
        values = list(exported.values())
        assert len(values) == 1
        return values[0]

    return do


class TestEnvVarHub:
    def test_example(self, check):
        exported = check(
            """
            import os
            from environ import Env

            VALUE1 = os.getenv('KEY1')
            VALUE2 = os.getenv('KEY2', 'default')
            VALUE3 = os.getenv('KEY3') or 'default'
            VALUE4 = str(os.getenv('KEY4') or 'default')
            VALUE5 = os.environ['KEY5']
            VALUE6 = int(os.environ['KEY6'])
            VALUE7 = os.environ.get('KEY7')
            VALUE8 = os.environ.get('KEY8', 'default')
            VALUE9 = os.environ.get('KEY9') or 'default'
            VALUE10 = int(os.environ.get('KEY10')) or 1

            env = Env(
                KEY11=(bool, False)
            )
            VALUE11 = env('KEY11')
            VALUE12 = env('KEY12')
            VALUE13 = env.str('KEY13')
            VALUE14 = env.str('KEY14', 'default')
            VALUE15 = env.str('KEY15', default='default')
            """
        )

        for i in [
            {"name": "KEY1", "value": "", "cast": "", "required": False},
            {"name": "KEY2", "value": "'default'", "cast": "str", "required": False},
            {"name": "KEY3", "value": "'default'", "cast": "str", "required": False},
            {"name": "KEY4", "value": "'default'", "cast": "str", "required": False},
            {"name": "KEY5", "value": "", "cast": "", "required": True},
            {"name": "KEY6", "value": "", "cast": "int", "required": True},
            {"name": "KEY7", "value": "", "cast": "", "required": False},
            {"name": "KEY8", "value": "'default'", "cast": "str", "required": False},
            {"name": "KEY9", "value": "'default'", "cast": "str", "required": False},
            {"name": "KEY10", "value": "1", "cast": "int", "required": False},
            {"name": "KEY11", "value": "False", "cast": "bool", "required": False},
            {"name": "KEY12", "value": "", "cast": "", "required": True},
            {"name": "KEY13", "value": "", "cast": "str", "required": True},
            {"name": "KEY14", "value": "'default'", "cast": "str", "required": False},
            {"name": "KEY15", "value": "'default'", "cast": "str", "required": False},
        ]:
            v = exported[i["name"]]
            assert v.name == i["name"]
            assert v.value == i["value"]
            assert v.cast == i["cast"]
            assert v.required == i["required"]

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
        "statement, name, expected_value1, expected_cast1, required",
        [
            ("getenv('KEY')", "KEY", "", "", False),
            ("getenv('KEY', 'default')", "KEY", "'default'", "str", False),
            ("environ['KEY']", "KEY", "", "", True),
            ("environ.get('KEY')", "KEY", "", "", False),
            ("environ.get('KEY', 'default')", "KEY", "'default'", "str", False),
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
        required,
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
        assert exported.required == required
        assert exported.statement() == real_statement
