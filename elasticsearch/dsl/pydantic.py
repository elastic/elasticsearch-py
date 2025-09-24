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

from typing import Any, ClassVar, Dict, Tuple, Type

from pydantic import BaseModel, Field, PrivateAttr
from typing_extensions import Annotated, Self, dataclass_transform

from elasticsearch import dsl


class _BaseModel(BaseModel):
    meta: Annotated[Dict[str, Any], dsl.mapped_field(exclude=True)] = Field(default={})


class BaseESModelMetaclass(type(BaseModel)):  # type: ignore[misc]
    def __new__(cls, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]) -> Any:
        model = super().__new__(cls, name, bases, attrs)
        dsl_attrs = {
            attr: value
            for attr, value in dsl.AsyncDocument.__dict__.items()
            if not attr.startswith("__")
        }
        model._doc = type(dsl.AsyncDocument)(  # type: ignore[misc]
            f"_ES{name}",
            dsl.AsyncDocument.__bases__,
            {**attrs, **dsl_attrs, "__qualname__": f"_ES{name}"},
        )
        return model


@dataclass_transform(kw_only_default=True, field_specifiers=(Field, PrivateAttr))
class BaseESModel(_BaseModel, metaclass=BaseESModelMetaclass):
    _doc: ClassVar[Type[dsl.AsyncDocument]]

    def to_doc(self) -> dsl.AsyncDocument:
        data = self.model_dump()
        meta = {f"_{k}": v for k, v in data.pop("meta", {}).items()}
        return self._doc(**meta, **data)

    @classmethod
    def from_doc(cls, dsl_obj: dsl.AsyncDocument) -> Self:
        return cls(meta=dsl_obj.meta.to_dict(), **dsl_obj.to_dict())
