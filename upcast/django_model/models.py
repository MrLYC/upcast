from ast_grep_py import SgNode
from pydantic import BaseModel, Field


class ModelField(BaseModel):
    node: SgNode = Field(title="Node of the field", exclude=True)
    name: str = Field("", title="Name of the field")
    type: str = Field("", title="Type of the field")
    class_path: str = Field("", title="Class path of the field")
    kwargs: dict[str, str] = Field(default_factory=dict, title="Keyword arguments")

    class Config:
        arbitrary_types_allowed = True


class ModelIndex(BaseModel):
    node: SgNode = Field(title="Node of the index", exclude=True)
    fields: list[str] = Field(default_factory=list, title="Fields of the index")
    kind: str = Field("", title="Kind of the index")

    class Config:
        arbitrary_types_allowed = True


class ModelBase(BaseModel):
    node: SgNode = Field(title="Node of the model", exclude=True)
    name: str = Field("", title="Name of the model")
    class_path: str = Field("", title="Class path of the model")

    class Config:
        arbitrary_types_allowed = True


class Model(BaseModel):
    node: SgNode = Field(title="Node of the model", exclude=True)
    name: str = Field(title="Name of the model")
    file: str = Field(title="Path of the file")
    location: tuple[int, int] = Field(title="Path of the model")
    bases: list[ModelBase] = Field(default_factory=list, title="Base classes of the model")
    fields: list[ModelField] = Field(default_factory=list, title="Fields of the model")
    indexes: list[ModelIndex] = Field(default_factory=list, title="Indexes of the model")

    class Config:
        arbitrary_types_allowed = True


class ImportedModule(BaseModel):
    path: str = Field("", title="Path of the module")
    module: str = Field("", title="Module name")
    name: str = Field("", title="Name of the class")
    alias: str = Field("", title="Alias of the class")


class Context(BaseModel):
    resolved_models: dict[str, Model] = Field(default_factory=dict, title="Resolved models")
    unresolved_models: list[Model] = Field(default_factory=list, title="Unresolved models")
    current_file: str = Field("", title="Current file")
    imported_models: dict[str, ImportedModule] = Field(default_factory=dict, title="Imported models")

    class Config:
        arbitrary_types_allowed = True

    def switch_to_file(self, file: str):
        self.current_file = file
        self.imported_models = {}

    def reset(self):
        self.switch_to_file("")

    def add_imported_module(self, module: ImportedModule):
        self.imported_models[module.alias or module.name] = module
