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
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
    cast,
)

from typing_extensions import Self, dataclass_transform

from elasticsearch.exceptions import NotFoundError, RequestError
from elasticsearch.helpers import bulk

from .._sync.index import Index
from ..connections import get_connection
from ..document_base import DocumentBase, DocumentMeta, mapped_field
from ..exceptions import IllegalOperation
from ..utils import DOC_META_FIELDS, META_FIELDS, UsingType, merge
from .search import Search

if TYPE_CHECKING:
    from elasticsearch import Elasticsearch


class IndexMeta(DocumentMeta):
    _index: Index

    # global flag to guard us from associating an Index with the base Document
    # class, only user defined subclasses should have an _index attr
    _document_initialized = False

    def __new__(
        cls, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]
    ) -> "IndexMeta":
        new_cls = super().__new__(cls, name, bases, attrs)
        if cls._document_initialized:
            index_opts = attrs.pop("Index", None)
            index = cls.construct_index(index_opts, bases)
            new_cls._index = index
            index.document(new_cls)
        cls._document_initialized = True
        return cast(IndexMeta, new_cls)

    @classmethod
    def construct_index(cls, opts: Dict[str, Any], bases: Tuple[type, ...]) -> Index:
        if opts is None:
            for b in bases:
                if hasattr(b, "_index"):
                    return b._index

            # Set None as Index name so it will set _all while making the query
            return Index(name=None)

        i = Index(getattr(opts, "name", "*"), using=getattr(opts, "using", "default"))
        i.settings(**getattr(opts, "settings", {}))
        i.aliases(**getattr(opts, "aliases", {}))
        for a in getattr(opts, "analyzers", ()):
            i.analyzer(a)
        return i


@dataclass_transform(field_specifiers=(mapped_field,))
class Document(DocumentBase, metaclass=IndexMeta):
    """
    Model-like class for persisting documents in elasticsearch.
    """

    if TYPE_CHECKING:
        _index: Index

    @classmethod
    def _get_using(cls, using: Optional[UsingType] = None) -> UsingType:
        return cast(UsingType, using or cls._index._using)

    @classmethod
    def _get_connection(cls, using: Optional[UsingType] = None) -> "Elasticsearch":
        return get_connection(cls._get_using(using))

    @classmethod
    def init(
        cls, index: Optional[str] = None, using: Optional[UsingType] = None
    ) -> None:
        """
        Create the index and populate the mappings in elasticsearch.
        """
        i = cls._index
        if index:
            i = i.clone(name=index)
        i.save(using=using)

    @classmethod
    def search(
        cls, using: Optional[UsingType] = None, index: Optional[str] = None
    ) -> Search[Self]:
        """
        Create an :class:`~elasticsearch.dsl.Search` instance that will search
        over this ``Document``.
        """
        return Search(
            using=cls._get_using(using), index=cls._default_index(index), doc_type=[cls]
        )

    @classmethod
    def get(
        cls,
        id: str,
        using: Optional[UsingType] = None,
        index: Optional[str] = None,
        **kwargs: Any,
    ) -> Optional[Self]:
        """
        Retrieve a single document from elasticsearch using its ``id``.

        :arg id: ``id`` of the document to be retrieved
        :arg index: elasticsearch index to use, if the ``Document`` is
            associated with an index this can be omitted.
        :arg using: connection alias to use, defaults to ``'default'``

        Any additional keyword arguments will be passed to
        ``Elasticsearch.get`` unchanged.
        """
        es = cls._get_connection(using)
        doc = es.get(index=cls._default_index(index), id=id, **kwargs)
        if not doc.get("found", False):
            return None
        return cls.from_es(doc)

    @classmethod
    def exists(
        cls,
        id: str,
        using: Optional[UsingType] = None,
        index: Optional[str] = None,
        **kwargs: Any,
    ) -> bool:
        """
        check if exists a single document from elasticsearch using its ``id``.

        :arg id: ``id`` of the document to check if exists
        :arg index: elasticsearch index to use, if the ``Document`` is
            associated with an index this can be omitted.
        :arg using: connection alias to use, defaults to ``'default'``

        Any additional keyword arguments will be passed to
        ``Elasticsearch.exists`` unchanged.
        """
        es = cls._get_connection(using)
        return bool(es.exists(index=cls._default_index(index), id=id, **kwargs))

    @classmethod
    def mget(
        cls,
        docs: List[Dict[str, Any]],
        using: Optional[UsingType] = None,
        index: Optional[str] = None,
        raise_on_error: bool = True,
        missing: str = "none",
        **kwargs: Any,
    ) -> List[Optional[Self]]:
        r"""
        Retrieve multiple document by their ``id``\s. Returns a list of instances
        in the same order as requested.

        :arg docs: list of ``id``\s of the documents to be retrieved or a list
            of document specifications as per
            https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-multi-get.html
        :arg index: elasticsearch index to use, if the ``Document`` is
            associated with an index this can be omitted.
        :arg using: connection alias to use, defaults to ``'default'``
        :arg missing: what to do when one of the documents requested is not
            found. Valid options are ``'none'`` (use ``None``), ``'raise'`` (raise
            ``NotFoundError``) or ``'skip'`` (ignore the missing document).

        Any additional keyword arguments will be passed to
        ``Elasticsearch.mget`` unchanged.
        """
        if missing not in ("raise", "skip", "none"):
            raise ValueError("'missing' must be 'raise', 'skip', or 'none'.")
        es = cls._get_connection(using)
        body = {
            "docs": [
                doc if isinstance(doc, collections.abc.Mapping) else {"_id": doc}
                for doc in docs
            ]
        }
        results = es.mget(index=cls._default_index(index), body=body, **kwargs)

        objs: List[Optional[Self]] = []
        error_docs: List[Self] = []
        missing_docs: List[Self] = []
        for doc in results["docs"]:
            if doc.get("found"):
                if error_docs or missing_docs:
                    # We're going to raise an exception anyway, so avoid an
                    # expensive call to cls.from_es().
                    continue

                objs.append(cls.from_es(doc))

            elif doc.get("error"):
                if raise_on_error:
                    error_docs.append(doc)
                if missing == "none":
                    objs.append(None)

            # The doc didn't cause an error, but the doc also wasn't found.
            elif missing == "raise":
                missing_docs.append(doc)
            elif missing == "none":
                objs.append(None)

        if error_docs:
            error_ids = [doc["_id"] for doc in error_docs]
            message = "Required routing not provided for documents %s."
            message %= ", ".join(error_ids)
            raise RequestError(400, message, error_docs)  # type: ignore[arg-type]
        if missing_docs:
            missing_ids = [doc["_id"] for doc in missing_docs]
            message = f"Documents {', '.join(missing_ids)} not found."
            raise NotFoundError(404, message, {"docs": missing_docs})  # type: ignore[arg-type]
        return objs

    def delete(
        self,
        using: Optional[UsingType] = None,
        index: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Delete the instance in elasticsearch.

        :arg index: elasticsearch index to use, if the ``Document`` is
            associated with an index this can be omitted.
        :arg using: connection alias to use, defaults to ``'default'``

        Any additional keyword arguments will be passed to
        ``Elasticsearch.delete`` unchanged.
        """
        es = self._get_connection(using)
        # extract routing etc from meta
        doc_meta = {k: self.meta[k] for k in DOC_META_FIELDS if k in self.meta}

        # Optimistic concurrency control
        if "seq_no" in self.meta and "primary_term" in self.meta:
            doc_meta["if_seq_no"] = self.meta["seq_no"]
            doc_meta["if_primary_term"] = self.meta["primary_term"]

        doc_meta.update(kwargs)
        i = self._get_index(index)
        assert i is not None

        es.delete(index=i, **doc_meta)

    def update(
        self,
        using: Optional[UsingType] = None,
        index: Optional[str] = None,
        detect_noop: bool = True,
        doc_as_upsert: bool = False,
        refresh: bool = False,
        retry_on_conflict: Optional[int] = None,
        script: Optional[Union[str, Dict[str, Any]]] = None,
        script_id: Optional[str] = None,
        scripted_upsert: bool = False,
        upsert: Optional[Dict[str, Any]] = None,
        return_doc_meta: bool = False,
        **fields: Any,
    ) -> Any:
        """
        Partial update of the document, specify fields you wish to update and
        both the instance and the document in elasticsearch will be updated::

            doc = MyDocument(title='Document Title!')
            doc.save()
            doc.update(title='New Document Title!')

        :arg index: elasticsearch index to use, if the ``Document`` is
            associated with an index this can be omitted.
        :arg using: connection alias to use, defaults to ``'default'``
        :arg detect_noop: Set to ``False`` to disable noop detection.
        :arg refresh: Control when the changes made by this request are visible
            to search. Set to ``True`` for immediate effect.
        :arg retry_on_conflict: In between the get and indexing phases of the
            update, it is possible that another process might have already
            updated the same document. By default, the update will fail with a
            version conflict exception. The retry_on_conflict parameter
            controls how many times to retry the update before finally throwing
            an exception.
        :arg doc_as_upsert:  Instead of sending a partial doc plus an upsert
            doc, setting doc_as_upsert to true will use the contents of doc as
            the upsert value
        :arg script: the source code of the script as a string, or a dictionary
            with script attributes to update.
        :arg return_doc_meta: set to ``True`` to return all metadata from the
            index API call instead of only the operation result

        :return: operation result noop/updated
        """
        body: Dict[str, Any] = {
            "doc_as_upsert": doc_as_upsert,
            "detect_noop": detect_noop,
        }

        # scripted update
        if script or script_id:
            if upsert is not None:
                body["upsert"] = upsert

            if script:
                if isinstance(script, str):
                    script = {"source": script}
            else:
                script = {"id": script_id}

            if "params" not in script:
                script["params"] = fields
            else:
                script["params"].update(fields)

            body["script"] = script
            body["scripted_upsert"] = scripted_upsert

        # partial document update
        else:
            if not fields:
                raise IllegalOperation(
                    "You cannot call update() without updating individual fields or a script. "
                    "If you wish to update the entire object use save()."
                )

            # update given fields locally
            merge(self, fields)

            # prepare data for ES
            values = self.to_dict(skip_empty=False)

            # if fields were given: partial update
            body["doc"] = {k: values.get(k) for k in fields.keys()}

        # extract routing etc from meta
        doc_meta = {k: self.meta[k] for k in DOC_META_FIELDS if k in self.meta}

        if retry_on_conflict is not None:
            doc_meta["retry_on_conflict"] = retry_on_conflict

        # Optimistic concurrency control
        if (
            retry_on_conflict in (None, 0)
            and "seq_no" in self.meta
            and "primary_term" in self.meta
        ):
            doc_meta["if_seq_no"] = self.meta["seq_no"]
            doc_meta["if_primary_term"] = self.meta["primary_term"]

        i = self._get_index(index)
        assert i is not None

        meta = self._get_connection(using).update(
            index=i, body=body, refresh=refresh, **doc_meta
        )

        # update meta information from ES
        for k in META_FIELDS:
            if "_" + k in meta:
                setattr(self.meta, k, meta["_" + k])

        return meta if return_doc_meta else meta["result"]

    def save(
        self,
        using: Optional[UsingType] = None,
        index: Optional[str] = None,
        validate: bool = True,
        skip_empty: bool = True,
        return_doc_meta: bool = False,
        **kwargs: Any,
    ) -> Any:
        """
        Save the document into elasticsearch. If the document doesn't exist it
        is created, it is overwritten otherwise. Returns ``True`` if this
        operations resulted in new document being created.

        :arg index: elasticsearch index to use, if the ``Document`` is
            associated with an index this can be omitted.
        :arg using: connection alias to use, defaults to ``'default'``
        :arg validate: set to ``False`` to skip validating the document
        :arg skip_empty: if set to ``False`` will cause empty values (``None``,
            ``[]``, ``{}``) to be left on the document. Those values will be
            stripped out otherwise as they make no difference in elasticsearch.
        :arg return_doc_meta: set to ``True`` to return all metadata from the
            update API call instead of only the operation result

        Any additional keyword arguments will be passed to
        ``Elasticsearch.index`` unchanged.

        :return: operation result created/updated
        """
        if validate:
            self.full_clean()

        es = self._get_connection(using)
        # extract routing etc from meta
        doc_meta = {k: self.meta[k] for k in DOC_META_FIELDS if k in self.meta}

        # Optimistic concurrency control
        if "seq_no" in self.meta and "primary_term" in self.meta:
            doc_meta["if_seq_no"] = self.meta["seq_no"]
            doc_meta["if_primary_term"] = self.meta["primary_term"]

        doc_meta.update(kwargs)
        i = self._get_index(index)
        assert i is not None

        meta = es.index(
            index=i,
            body=self.to_dict(skip_empty=skip_empty),
            **doc_meta,
        )
        # update meta information from ES
        for k in META_FIELDS:
            if "_" + k in meta:
                setattr(self.meta, k, meta["_" + k])

        return meta if return_doc_meta else meta["result"]

    @classmethod
    def bulk(
        cls,
        actions: Iterable[Union[Self, Dict[str, Any]]],
        using: Optional[UsingType] = None,
        index: Optional[str] = None,
        validate: bool = True,
        skip_empty: bool = True,
        **kwargs: Any,
    ) -> Tuple[int, Union[int, List[Any]]]:
        """
        Allows to perform multiple indexing operations in a single request.

        :arg actions: a generator that returns document instances to be indexed,
            bulk operation dictionaries.
        :arg using: connection alias to use, defaults to ``'default'``
        :arg index: Elasticsearch index to use, if the ``Document`` is
            associated with an index this can be omitted.
        :arg validate: set to ``False`` to skip validating the documents
        :arg skip_empty: if set to ``False`` will cause empty values (``None``,
            ``[]``, ``{}``) to be left on the document. Those values will be
            stripped out otherwise as they make no difference in Elasticsearch.

        Any additional keyword arguments will be passed to
        ``Elasticsearch.bulk`` unchanged.

        :return: bulk operation results
        """
        es = cls._get_connection(using)

        i = cls._default_index(index)
        assert i is not None

        class Generate:
            def __init__(
                self,
                doc_iterator: Iterable[Union[Document, Dict[str, Any]]],
            ):
                self.doc_iterator = doc_iterator.__iter__()

            def __iter__(self) -> Self:
                return self

            def __next__(self) -> Dict[str, Any]:
                doc: Optional[Union[Document, Dict[str, Any]]] = (
                    self.doc_iterator.__next__()
                )

                if isinstance(doc, dict):
                    action = doc
                    doc = None
                    if "_source" in action and isinstance(action["_source"], Document):
                        doc = action["_source"]
                        if validate:  # pragma: no cover
                            doc.full_clean()
                        action["_source"] = doc.to_dict(
                            include_meta=False, skip_empty=skip_empty
                        )
                elif doc is not None:
                    if validate:  # pragma: no cover
                        doc.full_clean()
                    action = doc.to_dict(include_meta=True, skip_empty=skip_empty)
                if "_index" not in action:
                    action["_index"] = i
                return action

        return bulk(es, Generate(actions), **kwargs)
