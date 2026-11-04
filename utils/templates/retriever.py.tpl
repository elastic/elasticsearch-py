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

import collections.abc
from copy import deepcopy
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    Protocol,
    Sequence,
    TypeVar,
    Union,
    cast,
    overload,
)

from elastic_transport.client_utils import DEFAULT

from .query import Query
from .utils import AttrDict, DslBase

if TYPE_CHECKING:
    from elastic_transport.client_utils import DefaultType
    from . import types
    from .document_base import InstrumentedField

_T = TypeVar("_T")
_M = TypeVar("_M", bound=Mapping[str, Any])


class RProxiedProtocol(Protocol[_T]):
    _proxied: _T


@overload
def R(
    name_or_retriever: MutableMapping[str, _M],
) -> Union["Retriever", "AttrDict[Any]"]: ...


@overload
def R(name_or_retriever: "Retriever") -> "Retriever": ...


@overload
def R(name_or_retriever: RProxiedProtocol[_T]) -> _T: ...


@overload
def R(name_or_retriever: str, **params: Any) -> "Retriever": ...


def R(
    name_or_retriever: Union[
        str,
        "Retriever",
        RProxiedProtocol[_T],
        MutableMapping[str, _M],
    ],
    **params: Any,
) -> Union["Retriever", "AttrDict[Any]", _T]:
    # types.RRFRetrieverComponent(retriever=..., weight=2.0)
    if isinstance(name_or_retriever, AttrDict):
        name_or_retriever = name_or_retriever.to_dict()

    # {"standard": {"query": {"match": {"title": "python"}}}}
    if isinstance(name_or_retriever, collections.abc.MutableMapping):
        if params:
            raise ValueError("R() cannot accept parameters when passing in a dict.")

        # RRF/Linear special case: {"retriever": {"standard": {...}}, "weight": 2.0}
        if "retriever" in name_or_retriever:
            component = RetrieverComponent(deepcopy(dict(name_or_retriever)))
            component.retriever = R(component.retriever)
            return component

        if len(name_or_retriever) != 1:
            raise ValueError(
                'R() can only accept dict with a single retriever '
                '({"standard": {...}}). '
                "Instead it got (%r)" % name_or_retriever
            )
        name, r_params = deepcopy(name_or_retriever).popitem()
        return Retriever.get_dsl_class(name)(_expand__to_dot=False, **r_params)

    # StandardRetriever()
    if isinstance(name_or_retriever, Retriever):
        if params:
            raise ValueError(
                "R() cannot accept parameters when passing in a Retriever object."
            )
        return name_or_retriever

    # s.retriever = R("standard", query=s.query)
    if hasattr(name_or_retriever, "_proxied"):
        return cast(RProxiedProtocol[_T], name_or_retriever)._proxied

    # "standard", query={"match": {"title": "python"}}
    return Retriever.get_dsl_class(name_or_retriever)(**params)


def _as_retriever(name_or_retriever: Union["Retriever", Dict[str, Any]]) -> "Retriever":
    """Coerce to a `Retriever`, for positions where a component is not valid.

    `R()` also returns a `RetrieverComponent` for dicts with a "retriever" key,
    which is only legitimate inside the `retrievers` list of `rrf` and `linear`.
    """
    r = R(name_or_retriever)
    if not isinstance(r, Retriever):
        raise ValueError(f"Expected a retriever, got {r!r}")
    return r


class Retriever(DslBase):
    _type_name = "retriever"
    _type_shortcut = staticmethod(R)
    name: ClassVar[Optional[str]] = None


class RetrieverComponent(AttrDict[Any]):
    """A retriever paired with a weight, as accepted by the `rrf` retriever.
    Also a retriever with a weight and/or normalizer as with `linear` retriever.

    Unlike a plain `AttrDict`, this serializes recursively so that the nested
    retriever is expanded rather than left as an object.
    """

    def to_dict(self, recursive: bool = True) -> Dict[str, Any]:
        return super().to_dict(recursive=recursive)


{% for k in classes %}
class {{ k.name }}({{ parent }}):
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
    name = "{{ k.property_name }}"
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
        {% if k.args and k.args[0].positional %}
        /,
        {% endif %}
        {% if k.args and not k.args[-1].positional %}
        *,
        {% endif %}
        {% for arg in k.args %}
            {% if not arg.positional %}
        {{ arg.name }}: {{ arg.type }} = DEFAULT,
            {% endif %}
        {% endfor %}
        **kwargs: Any
    ):
        {% if k.is_single_field %}
        if _field is not DEFAULT:
            kwargs[str(_field)] = _value
        {% elif k.is_multi_field %}
        if _fields is not DEFAULT:
            for field, value in _fields.items():
                kwargs[str(field)] = value
        {% endif %}
        super().__init__(
            {% for arg in k.args %}
                {% if not arg.positional %}
            {{ arg.name }}={{ arg.name }},
                {% endif %}
            {% endfor %}
            **kwargs
        )

{% endfor %}
