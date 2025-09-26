#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from typing import Any, ClassVar, Dict, List, Optional, Tuple, Type

from pydantic import BaseModel, Field, PrivateAttr
from typing_extensions import Annotated, Self, dataclass_transform

from elasticsearch import dsl


class ESMeta(BaseModel):
    """Metadata items associated with Elasticsearch documents."""

    id: str = ""
    index: str = ""
    primary_term: int = 0
    seq_no: int = 0
    version: int = 0
    score: float = 0


class _BaseModel(BaseModel):
    meta: Annotated[ESMeta, dsl.mapped_field(exclude=True)] = Field(
        default=ESMeta(),
        init=False,
    )


class _BaseESModelMetaclass(type(BaseModel)):  # type: ignore[misc]
    """Generic metaclass methods for BaseEsModel and AsyncBaseESModel."""

    @staticmethod
    def process_annotations(
        metacls: Type["_BaseESModelMetaclass"], annotations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process Pydantic typing annotations and adapt them so that they can
        be used to create the Elasticsearch document.
        """
        updated_annotations = {}
        for var, ann in annotations.items():
            if isinstance(ann, type(BaseModel)):
                # an inner Pydantic model is transformed into an Object field
                updated_annotations[var] = metacls.make_dsl_class(
                    metacls, dsl.InnerDoc, ann
                )
            elif (
                hasattr(ann, "__origin__")
                and ann.__origin__ in [list, List]
                and isinstance(ann.__args__[0], type(BaseModel))
            ):
                # an inner list of Pydantic models is transformed into a Nested field
                updated_annotations[var] = List[  # type: ignore[assignment,misc]
                    metacls.make_dsl_class(metacls, dsl.InnerDoc, ann.__args__[0])
                ]
            else:
                updated_annotations[var] = ann
        return updated_annotations

    @staticmethod
    def make_dsl_class(
        metacls: Type["_BaseESModelMetaclass"],
        dsl_class: type,
        pydantic_model: type,
        pydantic_attrs: Optional[Dict[str, Any]] = None,
    ) -> type:
        """Create a DSL document class dynamically, using the structure of a
        Pydantic model."""
        dsl_attrs = {
            attr: value
            for attr, value in dsl_class.__dict__.items()
            if not attr.startswith("__")
        }
        pydantic_attrs = {
            **(pydantic_attrs or {}),
            "__annotations__": metacls.process_annotations(
                metacls, pydantic_model.__annotations__
            ),
        }
        return type(dsl_class)(
            f"_ES{pydantic_model.__name__}",
            (dsl_class,),
            {
                **pydantic_attrs,
                **dsl_attrs,
                "__qualname__": f"_ES{pydantic_model.__name__}",
            },
        )


class BaseESModelMetaclass(_BaseESModelMetaclass):
    """Metaclass for the BaseESModel class."""

    def __new__(cls, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]) -> Any:
        model = super().__new__(cls, name, bases, attrs)
        model._doc = cls.make_dsl_class(cls, dsl.Document, model, attrs)
        return model


class AsyncBaseESModelMetaclass(_BaseESModelMetaclass):
    """Metaclass for the AsyncBaseESModel class."""

    def __new__(cls, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]) -> Any:
        model = super().__new__(cls, name, bases, attrs)
        model._doc = cls.make_dsl_class(cls, dsl.AsyncDocument, model, attrs)
        return model


@dataclass_transform(kw_only_default=True, field_specifiers=(Field, PrivateAttr))
class BaseESModel(_BaseModel, metaclass=BaseESModelMetaclass):
    _doc: ClassVar[Type[dsl.Document]]

    def to_doc(self) -> dsl.Document:
        """Convert this model to an Elasticsearch document."""
        data = self.model_dump()
        meta = {f"_{k}": v for k, v in data.pop("meta", {}).items() if v}
        return self._doc(**meta, **data)

    @classmethod
    def from_doc(cls, dsl_obj: dsl.Document) -> Self:
        """Create a model from the given Elasticsearch document."""
        return cls(meta=ESMeta(**dsl_obj.meta.to_dict()), **dsl_obj.to_dict())


@dataclass_transform(kw_only_default=True, field_specifiers=(Field, PrivateAttr))
class AsyncBaseESModel(_BaseModel, metaclass=AsyncBaseESModelMetaclass):
    _doc: ClassVar[Type[dsl.AsyncDocument]]

    def to_doc(self) -> dsl.AsyncDocument:
        """Convert this model to an Elasticsearch document."""
        data = self.model_dump()
        meta = {f"_{k}": v for k, v in data.pop("meta", {}).items() if v}
        return self._doc(**meta, **data)

    @classmethod
    def from_doc(cls, dsl_obj: dsl.AsyncDocument) -> Self:
        """Create a model from the given Elasticsearch document."""
        return cls(meta=ESMeta(**dsl_obj.meta.to_dict()), **dsl_obj.to_dict())
