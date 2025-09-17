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

import base64
import collections.abc
import ipaddress
from copy import deepcopy
from datetime import date, datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Iterator,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from dateutil import parser, tz
from elastic_transport.client_utils import DEFAULT, DefaultType

from .exceptions import ValidationException
from .query import Q
from .utils import AttrDict, AttrList, DslBase
from .wrappers import Range

if TYPE_CHECKING:
    from datetime import tzinfo
    from ipaddress import IPv4Address, IPv6Address

    from _operator import _SupportsComparison

    from .document import InnerDoc
    from .document_base import InstrumentedField
    from .mapping_base import MappingBase
    from .query import Query
    from . import types

unicode = str


def construct_field(
    name_or_field: Union[
        str,
        "Field",
        Dict[str, Any],
    ],
    **params: Any,
) -> "Field":
    # {"type": "text", "analyzer": "snowball"}
    if isinstance(name_or_field, collections.abc.Mapping):
        if params:
            raise ValueError(
                "construct_field() cannot accept parameters when passing in a dict."
            )
        params = deepcopy(name_or_field)
        if "type" not in params:
            # inner object can be implicitly defined
            if "properties" in params:
                name = "object"
            else:
                raise ValueError('construct_field() needs to have a "type" key.')
        else:
            name = params.pop("type")
        return Field.get_dsl_class(name)(**params)

    # Text()
    if isinstance(name_or_field, Field):
        if params:
            raise ValueError(
                "construct_field() cannot accept parameters "
                "when passing in a construct_field object."
            )
        return name_or_field

    # "text", analyzer="snowball"
    return Field.get_dsl_class(name_or_field)(**params)


class Field(DslBase):
    _type_name = "field"
    _type_shortcut = staticmethod(construct_field)
    # all fields can be multifields
    _param_defs = {"fields": {"type": "field", "hash": True}}
    name = ""
    _coerce = False

    def __init__(
        self, multi: bool = False, required: bool = False, *args: Any, **kwargs: Any
    ):
        """
        :arg bool multi: specifies whether field can contain array of values
        :arg bool required: specifies whether field is required
        """
        self._multi = multi
        self._required = required
        super().__init__(*args, **kwargs)

    def __getitem__(self, subfield: str) -> "Field":
        return cast(Field, self._params.get("fields", {})[subfield])

    def _serialize(self, data: Any, skip_empty: bool) -> Any:
        return data

    def _safe_serialize(self, data: Any, skip_empty: bool) -> Any:
        try:
            return self._serialize(data, skip_empty)
        except TypeError:
            # older method signature, without skip_empty
            return self._serialize(data)  # type: ignore[call-arg]

    def _deserialize(self, data: Any) -> Any:
        return data

    def _empty(self) -> Optional[Any]:
        return None

    def empty(self) -> Optional[Any]:
        if self._multi:
            return AttrList([])
        return self._empty()

    def serialize(self, data: Any, skip_empty: bool = True) -> Any:
        if isinstance(data, (list, AttrList, tuple)):
            return list(map(self._safe_serialize, cast(Iterable[Any], data), [skip_empty] * len(data)))
        return self._safe_serialize(data, skip_empty)

    def deserialize(self, data: Any) -> Any:
        if isinstance(data, (list, AttrList, tuple)):
            data = [
                None if d is None else self._deserialize(d)
                for d in cast(Iterable[Any], data)
            ]
            return data
        if data is None:
            return None
        return self._deserialize(data)

    def clean(self, data: Any) -> Any:
        if data is not None:
            data = self.deserialize(data)
        if data in (None, [], {}) and self._required:
            raise ValidationException("Value required for this field.")
        return data

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        name, value = cast(Tuple[str, Dict[str, Any]], d.popitem())
        value["type"] = name
        return value


class CustomField(Field):
    name = "custom"
    _coerce = True

    def to_dict(self) -> Dict[str, Any]:
        if isinstance(self.builtin_type, Field):
            return self.builtin_type.to_dict()

        d = super().to_dict()
        d["type"] = self.builtin_type
        return d


class RangeField(Field):
    _coerce = True
    _core_field: Optional[Field] = None

    def _deserialize(self, data: Any) -> Range["_SupportsComparison"]:
        if isinstance(data, Range):
            return data
        data = {k: self._core_field.deserialize(v) for k, v in data.items()}  # type: ignore[union-attr]
        return Range(data)

    def _serialize(self, data: Any, skip_empty: bool) -> Optional[Dict[str, Any]]:
        if data is None:
            return None
        if isinstance(data, AttrDict) or not isinstance(data, collections.abc.Mapping):
            data = data.to_dict()
        return {k: self._core_field.serialize(v) for k, v in data.items()}  # type: ignore[union-attr]


{% for k in classes %}
class {{ k.name }}({{ k.parent }}):
    """
    {% for line in k.docstring %}
    {{ line }}
    {% endfor %}
    {% if k.args %}
        {% if k.docstring %}

        {% endif %}
        {% for kwarg in k.args %}
            {% for line in kwarg.doc %}
    {{ line }}
            {% endfor %}
        {% endfor %}
    {% endif %}
    """
    name = "{{ k.field }}"
    {% if k.coerced %}
    _coerce = True
    {% endif %}
    {% if k.name.endswith('Range') %}
    _core_field = {{ k.name[:-5] }}()
    {% endif %}
    {% if k.params %}
    _param_defs = {
    {% for param in k.params %}
        "{{ param.name }}": {{ param.param }},
    {% endfor %}
    }
    {% endif %}

    def __init__(
        self,
        {% for arg in k.args %}
            {% if arg.positional %}
        {{ arg.name }}: {{ arg.type }} = DEFAULT,
            {% endif %}
        {% endfor %}
        *args: Any,
        {% for arg in k.args %}
            {% if not arg.positional %}
        {{ arg.name }}: {{ arg.type }} = DEFAULT,
            {% endif %}
        {% endfor %}
        **kwargs: Any
    ):
        {% for arg in k.args %}
            {% if not arg.positional %}
        if {{ arg.name }} is not DEFAULT:
                {% if "InstrumentedField" in arg.type %}
                    {% if "Sequence" in arg.type %}
            if isinstance({{ arg.name }}, list):
                kwargs["{{ arg.name }}"] = [str(field) for field in {{ arg.name }}]
            else:
                kwargs["{{ arg.name }}"] = str({{ arg.name }})
                    {% else %}
            kwargs["{{ arg.name }}"] = str({{ arg.name }})
                    {% endif %}
                {% else %}
            kwargs["{{ arg.name }}"] = {{ arg.name }}
                {% endif %}
            {% endif %}
        {% endfor %}
        {% if k.field == 'object' %}

        if doc_class is not DEFAULT and (properties is not DEFAULT or dynamic is not DEFAULT):
            raise ValidationException(
                "doc_class and properties/dynamic should not be provided together"
            )
        if doc_class is not DEFAULT:
            self._doc_class: Type["InnerDoc"] = doc_class
        else:
            # FIXME import
            from .document import InnerDoc

            # no InnerDoc subclass, creating one instead...
            self._doc_class = type("InnerDoc", (InnerDoc,), {})
            for name, field in (properties if properties is not DEFAULT else {}).items():
                self._doc_class._doc_type.mapping.field(name, field)
            if "properties" in kwargs:
                del kwargs["properties"]
            if dynamic is not DEFAULT:
                self._doc_class._doc_type.mapping.meta("dynamic", dynamic)

        self._mapping: "MappingBase" = deepcopy(self._doc_class._doc_type.mapping)
        super().__init__(**kwargs)

    def __getitem__(self, name: str) -> Field:
        return self._mapping[name]

    def __contains__(self, name: str) -> bool:
        return name in self._mapping

    def _empty(self) -> "InnerDoc":
        return self._wrap({})

    def _wrap(self, data: Dict[str, Any]) -> "InnerDoc":
        return self._doc_class.from_es(data, data_only=True)

    def empty(self) -> Union["InnerDoc", AttrList[Any]]:
        if self._multi:
            return AttrList[Any]([], self._wrap)
        return self._empty()

    def to_dict(self) -> Dict[str, Any]:
        d = self._mapping.to_dict()
        d.update(super().to_dict())
        return d

    def _collect_fields(self) -> Iterator[Field]:
        return self._mapping.properties._collect_fields()

    def _deserialize(self, data: Any) -> "InnerDoc":
        # don't wrap already wrapped data
        if isinstance(data, self._doc_class):
            return data

        if isinstance(data, AttrDict):
            data = data._d_

        return self._wrap(data)

    def _serialize(
        self, data: Optional[Union[Dict[str, Any], "InnerDoc"]], skip_empty: bool
    ) -> Optional[Dict[str, Any]]:
        from .document import InnerDoc

        if data is None:
            return None

        if isinstance(data, InnerDoc):
            return data.to_dict(skip_empty=skip_empty)
        elif isinstance(data, AttrDict):
            return data.to_dict()
        # somebody assigned raw dict to the field, we should tolerate that
        elif isinstance(data, collections.abc.Mapping):
            return data

    def clean(self, data: Any) -> Any:
        data = super().clean(data)
        if data is None:
            return None
        if isinstance(data, (list, AttrList)):
            for d in cast(Iterator["InnerDoc"], data):
                d.full_clean()
        else:
            data.full_clean()
        return data

    def update(self, other: Any, update_only: bool = False) -> None:
        if not isinstance(other, Object):
            # not an inner/nested object, no merge possible
            return

        self._mapping.update(other._mapping, update_only)
        {% elif k.field == "nested" %}
        kwargs.setdefault("multi", True)
        super().__init__(*args, **kwargs)
        {% elif k.field == "date" %}

        if default_timezone is DEFAULT:
            self._default_timezone = None
        elif isinstance(default_timezone, str):
            self._default_timezone = tz.gettz(default_timezone)
        else:
            self._default_timezone = default_timezone
        super().__init__(*args, **kwargs)

    def _deserialize(self, data: Any) -> Union[datetime, date]:
        if isinstance(data, str):
            try:
                data = parser.parse(data)
            except Exception as e:
                raise ValidationException(
                    f"Could not parse date from the value ({data!r})", e
                )
            # we treat the yyyy-MM-dd format as a special case
            if hasattr(self, "format") and self.format == "yyyy-MM-dd":
                data = data.date()

        if isinstance(data, datetime):
            if self._default_timezone and data.tzinfo is None:
                data = data.replace(tzinfo=self._default_timezone)
            return cast(datetime, data)
        if isinstance(data, date):
            return data
        if isinstance(data, int):
            # Divide by a float to preserve milliseconds on the datetime.
            return datetime.utcfromtimestamp(data / 1000.0)

        raise ValidationException(f"Could not parse date from the value ({data!r})")
        {% elif k.field == "boolean" %}
        super().__init__(*args, **kwargs)

    def _deserialize(self, data: Any) -> bool:
        if data == "false":
            return False
        return bool(data)

    def clean(self, data: Any) -> Optional[bool]:
        if data is not None:
            data = self.deserialize(data)
        if data is None and self._required:
            raise ValidationException("Value required for this field.")
        return data  # type: ignore[no-any-return]
        {% elif k.field == "float" %}
        super().__init__(*args, **kwargs)

    def _deserialize(self, data: Any) -> float:
        return float(data)
        {% elif k.field == "dense_vector" %}
        self._element_type = kwargs.get("element_type", "float")
        if self._element_type in ["float", "byte"]:
            kwargs["multi"] = True
        super().__init__(*args, **kwargs)

    def _deserialize(self, data: Any) -> Any:
        if self._element_type == "float":
            return float(data)
        elif self._element_type == "byte":
            return int(data)
        return data
        {% elif k.field == "scaled_float" %}
        if 'scaling_factor' not in kwargs:
            if len(args) > 0:
                kwargs['scaling_factor'] = args[0]
                args = args[1:]
            else:
                raise TypeError("missing required argument: 'scaling_factor'")
        super().__init__(*args, **kwargs)
        {% elif k.field == "integer" %}
        super().__init__(*args, **kwargs)

    def _deserialize(self, data: Any) -> int:
        return int(data)
        {% elif k.field == "ip" %}
        super().__init__(*args, **kwargs)

    def _deserialize(self, data: Any) -> Union["IPv4Address", "IPv6Address"]:
        # the ipaddress library for pypy only accepts unicode.
        return ipaddress.ip_address(unicode(data))

    def _serialize(self, data: Any, skip_empty: bool) -> Optional[str]:
        if data is None:
            return None
        return str(data)
        {% elif k.field == "binary" %}
        super().__init__(*args, **kwargs)

    def clean(self, data: str) -> str:
        # Binary fields are opaque, so there's not much cleaning
        # that can be done.
        return data

    def _deserialize(self, data: Any) -> bytes:
        return base64.b64decode(data)

    def _serialize(self, data: Any, skip_empty: bool) -> Optional[str]:
        if data is None:
            return None
        return base64.b64encode(data).decode()
        {% elif k.field == "percolator" %}
        super().__init__(*args, **kwargs)

    def _deserialize(self, data: Any) -> "Query":
        return Q(data)  # type: ignore[no-any-return]

    def _serialize(self, data: Any, skip_empty: bool) -> Optional[Dict[str, Any]]:
        if data is None:
            return None
        return data.to_dict()  # type: ignore[no-any-return]
        {% else %}
        super().__init__(*args, **kwargs)
        {% endif %}


{% endfor %}
