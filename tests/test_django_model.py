from io import StringIO
from textwrap import dedent

import pytest

from upcast.django_model import models
from upcast.django_model.core import Runner


@pytest.fixture
def context():
    return models.Context(root_dir="src")


@pytest.fixture
def runner(context):
    return Runner(context=context)


@pytest.fixture
def check(context, runner):
    def do(file_mapping: dict[str, str]):
        files: list[StringIO] = []

        for name, code in file_mapping.items():
            file = StringIO(dedent(code))
            file.name = name
            files.append(file)

        runner.run(files)

        return context.get_models()

    return do


class TestRunner:
    def test_analyze_django_models(self, check):
        results = check({
            "src/models/__init__.py": "from .author import *",
            "src/models/author.py": """
                from django.db import models
                from common import JsonField, SimpleManager, AdminManager, ModelMixin


                class Author(ModelMixin, models.Model):
                    first_name = models.CharField(max_length=100, db_index=True)
                    last_name = models.CharField(max_length=100, db_index=True)
                    sid = models.IntegerField(unique=True)
                    extra = JsonField()

                    objects = SimpleManager()
                    admin_objects = AdminManager()

                    def __str__(self):
                        return f"{self.first_name} {self.last_name}"

                    class Meta:
                        db_table = "authors"
                        unique_together = ["first_name", "last_name"]

                    @property
                    def full_name(self) -> str:
                        return self.get_full_name()

                    def do_something(self, action: str) -> str:
                        return f"{action} {self.full_name}"
                """,
            "src/tests.py": """
                from models import Author

                Model = Author

                author: Author = Author(first_name="YC", last_name="L", sid=1)
                author.save()

                assert isinstance(Author.objects.get(sid=1), Model)
                """,
        })

        assert len(results) == 1

        author = results[0]
        assert author.name == "Author"
        assert author.file == "src/models/author.py"
        assert "models.author.Author" in author.locations
        assert "models.Author" in author.locations
        assert author.manager == "common.SimpleManager"
        assert author.weight == 4
        assert author.lines > 0

        assert len(author.bases) == 2

        mixin = author.bases[0]
        assert mixin.name == "ModelMixin"
        assert mixin.class_path == "common.ModelMixin"

        base_model = author.bases[1]
        assert base_model.name == "Model"
        assert base_model.class_path == "django.db.models.Model"

        assert len(author.fields) == 4

        first_name = author.fields[0]
        assert first_name.name == "first_name"
        assert first_name.type == "CharField"
        assert first_name.class_path == "django.db.models.CharField"
        assert first_name.kwargs == {"max_length": 100, "db_index": True}

        sid = author.fields[2]
        assert sid.name == "sid"
        assert sid.type == "IntegerField"
        assert sid.class_path == "django.db.models.IntegerField"
        assert sid.kwargs == {"unique": True}

        extra = author.fields[3]
        assert extra.name == "extra"
        assert extra.type == "JsonField"
        assert extra.class_path == "common.JsonField"
        assert extra.kwargs == {}

        assert len(author.methods) == 3
        method_args = {
            "__str__": 1,
            "full_name": 1,
            "do_something": 2,
        }

        for method in author.methods:
            assert method.args == method_args.pop(method.name)
            assert method.lines > 0

        assert not method_args

        meta = author.meta
        assert meta.db_table == "authors"

        assert len(author.indexes) == 4

        unique_together = author.indexes[0]
        assert unique_together.fields == ["first_name", "last_name"]
        assert unique_together.kind == "unique"

        first_name_index = author.indexes[1]
        assert first_name_index.fields == ["first_name"]
        assert first_name_index.kind == "index"

        last_name_index = author.indexes[2]
        assert last_name_index.fields == ["last_name"]
        assert last_name_index.kind == "index"

        sid_index = author.indexes[3]
        assert sid_index.fields == ["sid"]
        assert sid_index.kind == "unique"

    def test_skip_pydantic_model(self, check):
        results = check({
            "src/models.py": """
                from pydantic import BaseModel, Field

                class Author(BaseModel):
                    first_name = Field()
                """,
        })

        assert len(results) == 0

    def test_model_field_challenge(self, check):
        results = check({
            "src/models.py": """
                from django.db import models
                from common import *
                from common import fields

                class Author(models.Model):
                    id = models.AutoField()
                    name_zh_hans = I18NField.zh_hans()
                    name_zh_hant = fields.I18NField.zh_hant()

                    callback = MyField().callback
                """,
        })

        assert len(results) == 1

        author = results[0]
        assert len(author.fields) == 3

        assert author.fields[0].name == "id"
        assert author.fields[1].name == "name_zh_hans"
        assert author.fields[2].name == "name_zh_hant"
