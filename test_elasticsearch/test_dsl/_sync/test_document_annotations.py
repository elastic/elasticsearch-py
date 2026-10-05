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

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Annotated, ClassVar, List, Optional

import pydantic
import pytest

from elasticsearch.dsl import (
    Date,
    Document,
    InnerDoc,
    Keyword,
    M,
    Object,
    Text,
    mapped_field,
)
from elasticsearch.dsl.exceptions import ValidationException
from elasticsearch.dsl.pydantic import BaseESModel

if TYPE_CHECKING:
    from datetime import datetime


class Author(InnerDoc):
    name = Keyword()


def test_optional_field_is_not_required() -> None:
    class Article(Document):
        name: str = mapped_field(Keyword(required=True))
        note: str | None = mapped_field(Keyword())

    assert Article._doc_type.mapping["name"]._required is True
    assert Article._doc_type.mapping["note"]._required is False
    Article(name="test").full_clean()


def test_future_annotations_have_same_mapping_as_plain_annotations() -> None:
    class PlainArticle(Document):
        __annotations__ = {
            "text": str,
            "created": date,
            "author": Author,
            "authors": List[Author],
            "note": Optional[str],
        }

    class Article(Document):
        text: str
        created: date
        author: Author
        authors: List[Author]
        note: Optional[str]

    assert (
        Article._doc_type.mapping.to_dict() == PlainArticle._doc_type.mapping.to_dict()
    )
    for name in ("text", "created", "author", "authors", "note"):
        field = Article._doc_type.mapping[name]
        plain_field = PlainArticle._doc_type.mapping[name]
        assert (field._required, field._multi) == (
            plain_field._required,
            plain_field._multi,
        )


@pytest.mark.parametrize(
    "annotation",
    [
        "str | None",
        "None | str",
        "Optional[str]",
        "M[Optional[str]]",
        'Optional["str"]',
    ],
)
def test_optional_annotations(annotation: str) -> None:
    class Article(Document):
        __annotations__ = {"note": annotation}
        note = mapped_field(Keyword(required=True))

    assert Article._doc_type.mapping["note"]._required is False
    Article().full_clean()


def test_none_first_optional_without_field() -> None:
    class Article(Document):
        note: None | str

    assert Article._doc_type.mapping.to_dict() == {
        "properties": {"note": {"type": "text"}}
    }
    assert Article._doc_type.mapping["note"]._required is False


def test_mapped_list_annotation() -> None:
    class Article(Document):
        tags: M[List[str]] = mapped_field(Keyword(required=True))

    assert Article().tags == []
    Article().full_clean()


def test_annotated_field() -> None:
    class Article(Document):
        metadata: Annotated[Optional[str], Keyword(required=True)]

    assert Article._doc_type.mapping.to_dict() == {
        "properties": {"metadata": {"type": "keyword"}}
    }
    Article().full_clean()


def test_annotated_field_takes_precedence_over_right_hand_field() -> None:
    class Article(Document):
        title: Annotated[str, Keyword()] = Text()

    assert Article._doc_type.mapping.to_dict() == {
        "properties": {"title": {"type": "keyword"}}
    }


def test_classvar_annotation() -> None:
    class Article(Document):
        ignored: ClassVar[str] = "not a field"

    assert Article._doc_type.mapping.to_dict() == {}


def test_annotation_uses_class_namespace() -> None:
    class Article(Document):
        Alias: ClassVar = Optional[str]
        note: Alias = Keyword(required=True)

    Article().full_clean()


@pytest.mark.parametrize("wrapped", [False, True])
def test_field_named_after_its_type(wrapped: bool) -> None:
    explicit = Date(format="yyyy-MM-dd")

    class Event(Document):
        date: date = mapped_field(explicit) if wrapped else explicit

    assert Event._doc_type.mapping["date"]._required is True
    Event(date=date(2026, 1, 2)).full_clean()


@pytest.mark.parametrize(
    "member_kind", ["method", "property", "classmethod", "staticmethod"]
)
def test_class_members_do_not_shadow_annotation_types(member_kind: str) -> None:
    class Event(Document):
        day: date

        def date(self) -> None:
            pass

        if member_kind == "property":
            date = property(date)
        elif member_kind == "classmethod":
            date = classmethod(date)
        elif member_kind == "staticmethod":
            date = staticmethod(date)

    assert Event._doc_type.mapping.to_dict() == {
        "properties": {"day": {"type": "date", "format": "yyyy-MM-dd"}}
    }


def test_pydantic_model_with_future_annotations() -> None:
    class Article(BaseESModel):
        name: Annotated[str, Keyword()] = pydantic.Field(default="draft")
        note: Optional[str] = None

    document = Article().to_doc()
    assert document._doc_type.mapping.to_dict() == {
        "properties": {"name": {"type": "keyword"}, "note": {"type": "text"}}
    }
    document.full_clean()


@pytest.mark.parametrize("required", [False, True])
def test_type_checking_only_annotation_uses_field_as_given(required: bool) -> None:
    explicit = Date(required=required)

    class Article(Document):
        created: datetime = explicit

    assert Article._doc_type.mapping["created"] is explicit
    assert explicit._required is required
    if required:
        with pytest.raises(ValidationException):
            Article().full_clean()
    else:
        Article().full_clean()


@pytest.mark.parametrize(
    "annotation",
    [
        "Missing",
        "Optional[Missing]",
        'List["Missing"]',
        "str | int",
        "List",
        "List[Annotated[str, 'doc']]",
        "List[int, str]",
        "[str]",
    ],
)
@pytest.mark.parametrize("required, multi", [(True, True), (False, False)])
def test_unusable_annotation_uses_field_as_given(
    annotation: str, required: bool, multi: bool
) -> None:
    explicit = Keyword(required=required, multi=multi)

    class Article(Document):
        __annotations__ = {"value": annotation}
        value = explicit

    assert Article._doc_type.mapping["value"] is explicit
    assert (explicit._required, explicit._multi) == (required, multi)


@pytest.mark.parametrize(
    "annotation, cause",
    [
        ("Optional[Missing]", NameError),
        ("str | int", TypeError),
        ("[str]", TypeError),
    ],
)
def test_unusable_annotation_without_field_raises(
    annotation: str, cause: type[Exception]
) -> None:
    with pytest.raises(TypeError, match="Cannot map field value") as exc:

        class Article(Document):
            __annotations__ = {"value": annotation}

    assert isinstance(exc.value.__cause__, cause)


def test_unresolved_annotation_keeps_mapped_field_options() -> None:
    class Article(Document):
        note: Missing = mapped_field(  # noqa: F821
            Keyword(multi=True), default=["draft"], es_name="note_text"
        )

    assert Article._doc_type.mapping.to_dict() == {
        "properties": {"note_text": {"type": "keyword"}}
    }
    assert Article().to_dict() == {"note_text": ["draft"]}


def test_unresolved_excluded_annotation() -> None:
    class Article(Document):
        ignored: Missing = mapped_field(exclude=True)  # noqa: F821

    assert "ignored" not in Article._doc_type.mapping


def test_function_local_type_uses_field_as_given() -> None:
    class Tag(InnerDoc):
        label: Optional[str] = Keyword()

    explicit = Object(Tag)

    class Article(Document):
        tag: Optional[Tag] = explicit

    assert Article._doc_type.mapping["tag"] is explicit


CircularAlias = "CircularAlias"
RecursiveAlias = List["RecursiveAlias"]


@pytest.mark.parametrize("annotation", ["CircularAlias", "RecursiveAlias"])
def test_circular_alias_uses_field_as_given(annotation: str) -> None:
    class Article(Document):
        __annotations__ = {"value": annotation}
        value = Keyword(multi=True)

    assert Article().value == []
