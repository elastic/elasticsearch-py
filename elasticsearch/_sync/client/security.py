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

import typing as t

from elastic_transport import ObjectApiResponse

from ._base import NamespacedClient
from .utils import SKIP_IN_PATH, _quote, _rewrite_parameters


class SecurityClient(NamespacedClient):
    @_rewrite_parameters(
        body_fields=True,
    )
    def activate_user_profile(
        self,
        *,
        grant_type: t.Union["t.Literal['access_token', 'password']", str],
        access_token: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        password: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        username: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates or updates the user profile on behalf of another user.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-activate-user-profile.html>`_

        :param grant_type:
        :param access_token:
        :param password:
        :param username:
        """
        if grant_type is None:
            raise ValueError("Empty value passed for parameter 'grant_type'")
        __path = "/_security/profile/_activate"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if grant_type is not None:
            __body["grant_type"] = grant_type
        if access_token is not None:
            __body["access_token"] = access_token
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if password is not None:
            __body["password"] = password
        if pretty is not None:
            __query["pretty"] = pretty
        if username is not None:
            __body["username"] = username
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def authenticate(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Enables authentication as a user and retrieve information about the authenticated
        user.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-authenticate.html>`_
        """
        __path = "/_security/_authenticate"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def change_password(
        self,
        *,
        username: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        password: t.Optional[str] = None,
        password_hash: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Changes the passwords of users in the native realm and built-in users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-change-password.html>`_

        :param username: The user whose password you want to change. If you do not specify
            this parameter, the password is changed for the current user.
        :param password: The new password value. Passwords must be at least 6 characters
            long.
        :param password_hash: A hash of the new password value. This must be produced
            using the same hashing algorithm as has been configured for password storage.
            For more details, see the explanation of the `xpack.security.authc.password_hashing.algorithm`
            setting.
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if username not in SKIP_IN_PATH:
            __path = f"/_security/user/{_quote(username)}/_password"
        else:
            __path = "/_security/user/_password"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if password is not None:
            __body["password"] = password
        if password_hash is not None:
            __body["password_hash"] = password_hash
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def clear_api_key_cache(
        self,
        *,
        ids: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Clear a subset or all entries from the API key cache.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-clear-api-key-cache.html>`_

        :param ids: A comma-separated list of IDs of API keys to clear from the cache
        """
        if ids in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'ids'")
        __path = f"/_security/api_key/{_quote(ids)}/_clear_cache"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def clear_cached_privileges(
        self,
        *,
        application: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Evicts application privileges from the native application privileges cache.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-clear-privilege-cache.html>`_

        :param application: A comma-separated list of application names
        """
        if application in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'application'")
        __path = f"/_security/privilege/{_quote(application)}/_clear_cache"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def clear_cached_realms(
        self,
        *,
        realms: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        usernames: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Evicts users from the user cache. Can completely clear the cache or evict specific
        users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-clear-cache.html>`_

        :param realms: Comma-separated list of realms to clear
        :param usernames: Comma-separated list of usernames to clear from the cache
        """
        if realms in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'realms'")
        __path = f"/_security/realm/{_quote(realms)}/_clear_cache"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if usernames is not None:
            __query["usernames"] = usernames
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def clear_cached_roles(
        self,
        *,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Evicts roles from the native role cache.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-clear-role-cache.html>`_

        :param name: Role name
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/role/{_quote(name)}/_clear_cache"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def clear_cached_service_tokens(
        self,
        *,
        namespace: str,
        service: str,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Evicts tokens from the service account token caches.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-clear-service-token-caches.html>`_

        :param namespace: An identifier for the namespace
        :param service: An identifier for the service name
        :param name: A comma-separated list of service token names
        """
        if namespace in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'namespace'")
        if service in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'service'")
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/service/{_quote(namespace)}/{_quote(service)}/credential/token/{_quote(name)}/_clear_cache"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create_api_key(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        expiration: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        metadata: t.Optional[t.Mapping[str, t.Any]] = None,
        name: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
        role_descriptors: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates an API key for access without requiring basic authentication.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-create-api-key.html>`_

        :param expiration: Expiration time for the API key. By default, API keys never
            expire.
        :param metadata: Arbitrary metadata that you want to associate with the API key.
            It supports nested data structure. Within the metadata object, keys beginning
            with _ are reserved for system usage.
        :param name: Specifies the name for this API key.
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        :param role_descriptors: An array of role descriptors for this API key. This
            parameter is optional. When it is not specified or is an empty array, then
            the API key will have a point in time snapshot of permissions of the authenticated
            user. If you supply role descriptors then the resultant permissions would
            be an intersection of API keys permissions and authenticated user’s permissions
            thereby limiting the access scope for API keys. The structure of role descriptor
            is the same as the request for create role API. For more details, see create
            or update roles API.
        """
        __path = "/_security/api_key"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expiration is not None:
            __body["expiration"] = expiration
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if metadata is not None:
            __body["metadata"] = metadata
        if name is not None:
            __body["name"] = name
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        if role_descriptors is not None:
            __body["role_descriptors"] = role_descriptors
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def create_service_token(
        self,
        *,
        namespace: str,
        service: str,
        name: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a service account token for access without requiring basic authentication.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-create-service-token.html>`_

        :param namespace: An identifier for the namespace
        :param service: An identifier for the service name
        :param name: An identifier for the token name
        :param refresh: If `true` then refresh the affected shards to make this operation
            visible to search, if `wait_for` (the default) then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if namespace in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'namespace'")
        if service in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'service'")
        if (
            namespace not in SKIP_IN_PATH
            and service not in SKIP_IN_PATH
            and name not in SKIP_IN_PATH
        ):
            __path = f"/_security/service/{_quote(namespace)}/{_quote(service)}/credential/token/{_quote(name)}"
            __method = "PUT"
        elif namespace not in SKIP_IN_PATH and service not in SKIP_IN_PATH:
            __path = f"/_security/service/{_quote(namespace)}/{_quote(service)}/credential/token"
            __method = "POST"
        else:
            raise ValueError("Couldn't find a path for the given parameters")
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            __method, __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def delete_privileges(
        self,
        *,
        application: str,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Removes application privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-delete-privilege.html>`_

        :param application: Application name
        :param name: Privilege name
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if application in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'application'")
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/privilege/{_quote(application)}/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def delete_role(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Removes roles in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-delete-role.html>`_

        :param name: Role name
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/role/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def delete_role_mapping(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Removes role mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-delete-role-mapping.html>`_

        :param name: Role-mapping name
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/role_mapping/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def delete_service_token(
        self,
        *,
        namespace: str,
        service: str,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a service account token.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-delete-service-token.html>`_

        :param namespace: An identifier for the namespace
        :param service: An identifier for the service name
        :param name: An identifier for the token name
        :param refresh: If `true` then refresh the affected shards to make this operation
            visible to search, if `wait_for` (the default) then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if namespace in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'namespace'")
        if service in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'service'")
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/service/{_quote(namespace)}/{_quote(service)}/credential/token/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def delete_user(
        self,
        *,
        username: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes users from the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-delete-user.html>`_

        :param username: username
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'username'")
        __path = f"/_security/user/{_quote(username)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def disable_user(
        self,
        *,
        username: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Disables users in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-disable-user.html>`_

        :param username: The username of the user to disable
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'username'")
        __path = f"/_security/user/{_quote(username)}/_disable"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def disable_user_profile(
        self,
        *,
        uid: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Disables a user profile so it's not visible in user profile searches.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-disable-user-profile.html>`_

        :param uid: Unique identifier for the user profile.
        :param refresh: If 'true', Elasticsearch refreshes the affected shards to make
            this operation visible to search, if 'wait_for' then wait for a refresh to
            make this operation visible to search, if 'false' do nothing with refreshes.
        """
        if uid in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'uid'")
        __path = f"/_security/profile/{_quote(uid)}/_disable"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def enable_user(
        self,
        *,
        username: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Enables users in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-enable-user.html>`_

        :param username: The username of the user to enable
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'username'")
        __path = f"/_security/user/{_quote(username)}/_enable"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def enable_user_profile(
        self,
        *,
        uid: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Enables a user profile so it's visible in user profile searches.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-enable-user-profile.html>`_

        :param uid: Unique identifier for the user profile.
        :param refresh: If 'true', Elasticsearch refreshes the affected shards to make
            this operation visible to search, if 'wait_for' then wait for a refresh to
            make this operation visible to search, if 'false' do nothing with refreshes.
        """
        if uid in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'uid'")
        __path = f"/_security/profile/{_quote(uid)}/_enable"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def enroll_kibana(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Allows a kibana instance to configure itself to communicate with a secured elasticsearch
        cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-kibana-enrollment.html>`_
        """
        __path = "/_security/enroll/kibana"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def enroll_node(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Allows a new node to enroll to an existing cluster with security enabled.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-node-enrollment.html>`_
        """
        __path = "/_security/enroll/node"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_api_key(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        id: t.Optional[str] = None,
        name: t.Optional[str] = None,
        owner: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        realm_name: t.Optional[str] = None,
        username: t.Optional[str] = None,
        with_limited_by: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves information for one or more API keys.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-api-key.html>`_

        :param id: API key id of the API key to be retrieved
        :param name: API key name of the API key to be retrieved
        :param owner: flag to query API keys owned by the currently authenticated user
        :param realm_name: realm name of the user who created this API key to be retrieved
        :param username: user name of the user who created this API key to be retrieved
        :param with_limited_by: Return the snapshot of the owner user's role descriptors
            associated with the API key. An API key's actual permission is the intersection
            of its assigned role descriptors and the owner user's role descriptors.
        """
        __path = "/_security/api_key"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if id is not None:
            __query["id"] = id
        if name is not None:
            __query["name"] = name
        if owner is not None:
            __query["owner"] = owner
        if pretty is not None:
            __query["pretty"] = pretty
        if realm_name is not None:
            __query["realm_name"] = realm_name
        if username is not None:
            __query["username"] = username
        if with_limited_by is not None:
            __query["with_limited_by"] = with_limited_by
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_builtin_privileges(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves the list of cluster privileges and index privileges that are available
        in this version of Elasticsearch.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-builtin-privileges.html>`_
        """
        __path = "/_security/privilege/_builtin"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_privileges(
        self,
        *,
        application: t.Optional[str] = None,
        name: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves application privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-privileges.html>`_

        :param application: Application name
        :param name: Privilege name
        """
        if application not in SKIP_IN_PATH and name not in SKIP_IN_PATH:
            __path = f"/_security/privilege/{_quote(application)}/{_quote(name)}"
        elif application not in SKIP_IN_PATH:
            __path = f"/_security/privilege/{_quote(application)}"
        else:
            __path = "/_security/privilege"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_role(
        self,
        *,
        name: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves roles in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-role.html>`_

        :param name: The name of the role. You can specify multiple roles as a comma-separated
            list. If you do not specify this parameter, the API returns information about
            all roles.
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_security/role/{_quote(name)}"
        else:
            __path = "/_security/role"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_role_mapping(
        self,
        *,
        name: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves role mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-role-mapping.html>`_

        :param name: The distinct name that identifies the role mapping. The name is
            used solely as an identifier to facilitate interaction via the API; it does
            not affect the behavior of the mapping in any way. You can specify multiple
            mapping names as a comma-separated list. If you do not specify this parameter,
            the API returns information about all role mappings.
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_security/role_mapping/{_quote(name)}"
        else:
            __path = "/_security/role_mapping"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_service_accounts(
        self,
        *,
        namespace: t.Optional[str] = None,
        service: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves information about service accounts.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-service-accounts.html>`_

        :param namespace: Name of the namespace. Omit this parameter to retrieve information
            about all service accounts. If you omit this parameter, you must also omit
            the `service` parameter.
        :param service: Name of the service name. Omit this parameter to retrieve information
            about all service accounts that belong to the specified `namespace`.
        """
        if namespace not in SKIP_IN_PATH and service not in SKIP_IN_PATH:
            __path = f"/_security/service/{_quote(namespace)}/{_quote(service)}"
        elif namespace not in SKIP_IN_PATH:
            __path = f"/_security/service/{_quote(namespace)}"
        else:
            __path = "/_security/service"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_service_credentials(
        self,
        *,
        namespace: str,
        service: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves information of all service credentials for a service account.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-service-credentials.html>`_

        :param namespace: Name of the namespace.
        :param service: Name of the service name.
        """
        if namespace in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'namespace'")
        if service in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'service'")
        __path = f"/_security/service/{_quote(namespace)}/{_quote(service)}/credential"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def get_token(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        grant_type: t.Optional[
            t.Union[
                "t.Literal['_kerberos', 'client_credentials', 'password', 'refresh_token']",
                str,
            ]
        ] = None,
        human: t.Optional[bool] = None,
        kerberos_ticket: t.Optional[str] = None,
        password: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        refresh_token: t.Optional[str] = None,
        scope: t.Optional[str] = None,
        username: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a bearer token for access without requiring basic authentication.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-token.html>`_

        :param grant_type:
        :param kerberos_ticket:
        :param password:
        :param refresh_token:
        :param scope:
        :param username:
        """
        __path = "/_security/oauth2/token"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if grant_type is not None:
            __body["grant_type"] = grant_type
        if human is not None:
            __query["human"] = human
        if kerberos_ticket is not None:
            __body["kerberos_ticket"] = kerberos_ticket
        if password is not None:
            __body["password"] = password
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh_token is not None:
            __body["refresh_token"] = refresh_token
        if scope is not None:
            __body["scope"] = scope
        if username is not None:
            __body["username"] = username
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def get_user(
        self,
        *,
        username: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        with_profile_uid: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves information about users in the native realm and built-in users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-user.html>`_

        :param username: An identifier for the user. You can specify multiple usernames
            as a comma-separated list. If you omit this parameter, the API retrieves
            information about all users.
        :param with_profile_uid: If true will return the User Profile ID for a user,
            if any.
        """
        if username not in SKIP_IN_PATH:
            __path = f"/_security/user/{_quote(username)}"
        else:
            __path = "/_security/user"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if with_profile_uid is not None:
            __query["with_profile_uid"] = with_profile_uid
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_user_privileges(
        self,
        *,
        application: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        priviledge: t.Optional[str] = None,
        username: t.Optional[t.Union[None, str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves security privileges for the logged in user.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-user-privileges.html>`_

        :param application: The name of the application. Application privileges are always
            associated with exactly one application. If you do not specify this parameter,
            the API returns information about all privileges for all applications.
        :param priviledge: The name of the privilege. If you do not specify this parameter,
            the API returns information about all privileges for the requested application.
        :param username:
        """
        __path = "/_security/user/_privileges"
        __query: t.Dict[str, t.Any] = {}
        if application is not None:
            __query["application"] = application
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if priviledge is not None:
            __query["priviledge"] = priviledge
        if username is not None:
            __query["username"] = username
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_user_profile(
        self,
        *,
        uid: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        data: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves user profiles for the given unique ID(s).

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-get-user-profile.html>`_

        :param uid: A unique identifier for the user profile.
        :param data: List of filters for the `data` field of the profile document. To
            return all content use `data=*`. To return a subset of content use `data=<key>`
            to retrieve content nested under the specified `<key>`. By default returns
            no `data` content.
        """
        if uid in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'uid'")
        __path = f"/_security/profile/{_quote(uid)}"
        __query: t.Dict[str, t.Any] = {}
        if data is not None:
            __query["data"] = data
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
        ignore_deprecated_options={"api_key"},
    )
    def grant_api_key(
        self,
        *,
        api_key: t.Mapping[str, t.Any],
        grant_type: t.Union["t.Literal['access_token', 'password']", str],
        access_token: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        password: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        run_as: t.Optional[str] = None,
        username: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates an API key on behalf of another user.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-grant-api-key.html>`_

        :param api_key:
        :param grant_type:
        :param access_token:
        :param password:
        :param run_as:
        :param username:
        """
        if api_key is None:
            raise ValueError("Empty value passed for parameter 'api_key'")
        if grant_type is None:
            raise ValueError("Empty value passed for parameter 'grant_type'")
        __path = "/_security/api_key/grant"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if api_key is not None:
            __body["api_key"] = api_key
        if grant_type is not None:
            __body["grant_type"] = grant_type
        if access_token is not None:
            __body["access_token"] = access_token
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if password is not None:
            __body["password"] = password
        if pretty is not None:
            __query["pretty"] = pretty
        if run_as is not None:
            __body["run_as"] = run_as
        if username is not None:
            __body["username"] = username
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def has_privileges(
        self,
        *,
        user: t.Optional[str] = None,
        application: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        cluster: t.Optional[
            t.Union[
                t.List[
                    t.Union[
                        "t.Literal['all', 'cancel_task', 'create_snapshot', 'grant_api_key', 'manage', 'manage_api_key', 'manage_ccr', 'manage_enrich', 'manage_ilm', 'manage_index_templates', 'manage_ingest_pipelines', 'manage_logstash_pipelines', 'manage_ml', 'manage_oidc', 'manage_own_api_key', 'manage_pipeline', 'manage_rollup', 'manage_saml', 'manage_security', 'manage_service_account', 'manage_slm', 'manage_token', 'manage_transform', 'manage_user_profile', 'manage_watcher', 'monitor', 'monitor_ml', 'monitor_rollup', 'monitor_snapshot', 'monitor_text_structure', 'monitor_transform', 'monitor_watcher', 'read_ccr', 'read_ilm', 'read_pipeline', 'read_slm', 'transport_client']",
                        str,
                    ]
                ],
                t.Tuple[
                    t.Union[
                        "t.Literal['all', 'cancel_task', 'create_snapshot', 'grant_api_key', 'manage', 'manage_api_key', 'manage_ccr', 'manage_enrich', 'manage_ilm', 'manage_index_templates', 'manage_ingest_pipelines', 'manage_logstash_pipelines', 'manage_ml', 'manage_oidc', 'manage_own_api_key', 'manage_pipeline', 'manage_rollup', 'manage_saml', 'manage_security', 'manage_service_account', 'manage_slm', 'manage_token', 'manage_transform', 'manage_user_profile', 'manage_watcher', 'monitor', 'monitor_ml', 'monitor_rollup', 'monitor_snapshot', 'monitor_text_structure', 'monitor_transform', 'monitor_watcher', 'read_ccr', 'read_ilm', 'read_pipeline', 'read_slm', 'transport_client']",
                        str,
                    ],
                    ...,
                ],
            ]
        ] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        index: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Determines whether the specified user has a specified list of privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-has-privileges.html>`_

        :param user: Username
        :param application:
        :param cluster: A list of the cluster privileges that you want to check.
        :param index:
        """
        if user not in SKIP_IN_PATH:
            __path = f"/_security/user/{_quote(user)}/_has_privileges"
        else:
            __path = "/_security/user/_has_privileges"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if application is not None:
            __body["application"] = application
        if cluster is not None:
            __body["cluster"] = cluster
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if index is not None:
            __body["index"] = index
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def has_privileges_user_profile(
        self,
        *,
        privileges: t.Mapping[str, t.Any],
        uids: t.Union[t.List[str], t.Tuple[str, ...]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Determines whether the users associated with the specified profile IDs have all
        the requested privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-has-privileges-user-profile.html>`_

        :param privileges:
        :param uids: A list of profile IDs. The privileges are checked for associated
            users of the profiles.
        """
        if privileges is None:
            raise ValueError("Empty value passed for parameter 'privileges'")
        if uids is None:
            raise ValueError("Empty value passed for parameter 'uids'")
        __path = "/_security/profile/_has_privileges"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if privileges is not None:
            __body["privileges"] = privileges
        if uids is not None:
            __body["uids"] = uids
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def invalidate_api_key(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        id: t.Optional[str] = None,
        ids: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        name: t.Optional[str] = None,
        owner: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        realm_name: t.Optional[str] = None,
        username: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Invalidates one or more API keys.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-invalidate-api-key.html>`_

        :param id:
        :param ids:
        :param name:
        :param owner:
        :param realm_name:
        :param username:
        """
        __path = "/_security/api_key"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if id is not None:
            __body["id"] = id
        if ids is not None:
            __body["ids"] = ids
        if name is not None:
            __body["name"] = name
        if owner is not None:
            __body["owner"] = owner
        if pretty is not None:
            __query["pretty"] = pretty
        if realm_name is not None:
            __body["realm_name"] = realm_name
        if username is not None:
            __body["username"] = username
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def invalidate_token(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        realm_name: t.Optional[str] = None,
        refresh_token: t.Optional[str] = None,
        token: t.Optional[str] = None,
        username: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Invalidates one or more access tokens or refresh tokens.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-invalidate-token.html>`_

        :param realm_name:
        :param refresh_token:
        :param token:
        :param username:
        """
        __path = "/_security/oauth2/token"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if realm_name is not None:
            __body["realm_name"] = realm_name
        if refresh_token is not None:
            __body["refresh_token"] = refresh_token
        if token is not None:
            __body["token"] = token
        if username is not None:
            __body["username"] = username
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_name="privileges",
    )
    def put_privileges(
        self,
        *,
        privileges: t.Mapping[str, t.Mapping[str, t.Mapping[str, t.Any]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Adds or updates application privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-put-privileges.html>`_

        :param privileges:
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if privileges is None:
            raise ValueError("Empty value passed for parameter 'privileges'")
        __path = "/_security/privilege"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __body = privileges
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
        parameter_aliases={"global": "global_"},
    )
    def put_role(
        self,
        *,
        name: str,
        applications: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        cluster: t.Optional[
            t.Union[
                t.List[
                    t.Union[
                        "t.Literal['all', 'cancel_task', 'create_snapshot', 'grant_api_key', 'manage', 'manage_api_key', 'manage_ccr', 'manage_enrich', 'manage_ilm', 'manage_index_templates', 'manage_ingest_pipelines', 'manage_logstash_pipelines', 'manage_ml', 'manage_oidc', 'manage_own_api_key', 'manage_pipeline', 'manage_rollup', 'manage_saml', 'manage_security', 'manage_service_account', 'manage_slm', 'manage_token', 'manage_transform', 'manage_user_profile', 'manage_watcher', 'monitor', 'monitor_ml', 'monitor_rollup', 'monitor_snapshot', 'monitor_text_structure', 'monitor_transform', 'monitor_watcher', 'read_ccr', 'read_ilm', 'read_pipeline', 'read_slm', 'transport_client']",
                        str,
                    ]
                ],
                t.Tuple[
                    t.Union[
                        "t.Literal['all', 'cancel_task', 'create_snapshot', 'grant_api_key', 'manage', 'manage_api_key', 'manage_ccr', 'manage_enrich', 'manage_ilm', 'manage_index_templates', 'manage_ingest_pipelines', 'manage_logstash_pipelines', 'manage_ml', 'manage_oidc', 'manage_own_api_key', 'manage_pipeline', 'manage_rollup', 'manage_saml', 'manage_security', 'manage_service_account', 'manage_slm', 'manage_token', 'manage_transform', 'manage_user_profile', 'manage_watcher', 'monitor', 'monitor_ml', 'monitor_rollup', 'monitor_snapshot', 'monitor_text_structure', 'monitor_transform', 'monitor_watcher', 'read_ccr', 'read_ilm', 'read_pipeline', 'read_slm', 'transport_client']",
                        str,
                    ],
                    ...,
                ],
            ]
        ] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        global_: t.Optional[t.Mapping[str, t.Any]] = None,
        human: t.Optional[bool] = None,
        indices: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        metadata: t.Optional[t.Mapping[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
        run_as: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        transient_metadata: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Adds and updates roles in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-put-role.html>`_

        :param name: The name of the role.
        :param applications: A list of application privilege entries.
        :param cluster: A list of cluster privileges. These privileges define the cluster-level
            actions for users with this role.
        :param global_: An object defining global privileges. A global privilege is a
            form of cluster privilege that is request-aware. Support for global privileges
            is currently limited to the management of application privileges.
        :param indices: A list of indices permissions entries.
        :param metadata: Optional metadata. Within the metadata object, keys that begin
            with an underscore (`_`) are reserved for system use.
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        :param run_as: A list of users that the owners of this role can impersonate.
        :param transient_metadata: Indicates roles that might be incompatible with the
            current cluster license, specifically roles with document and field level
            security. When the cluster license doesn’t allow certain features for a given
            role, this parameter is updated dynamically to list the incompatible features.
            If `enabled` is `false`, the role is ignored, but is still listed in the
            response from the authenticate API.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/role/{_quote(name)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if applications is not None:
            __body["applications"] = applications
        if cluster is not None:
            __body["cluster"] = cluster
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if global_ is not None:
            __body["global"] = global_
        if human is not None:
            __query["human"] = human
        if indices is not None:
            __body["indices"] = indices
        if metadata is not None:
            __body["metadata"] = metadata
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        if run_as is not None:
            __body["run_as"] = run_as
        if transient_metadata is not None:
            __body["transient_metadata"] = transient_metadata
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_role_mapping(
        self,
        *,
        name: str,
        enabled: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        metadata: t.Optional[t.Mapping[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
        roles: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        rules: t.Optional[t.Mapping[str, t.Any]] = None,
        run_as: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates and updates role mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-put-role-mapping.html>`_

        :param name: Role-mapping name
        :param enabled:
        :param metadata:
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        :param roles:
        :param rules:
        :param run_as:
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/role_mapping/{_quote(name)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if enabled is not None:
            __body["enabled"] = enabled
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if metadata is not None:
            __body["metadata"] = metadata
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        if roles is not None:
            __body["roles"] = roles
        if rules is not None:
            __body["rules"] = rules
        if run_as is not None:
            __body["run_as"] = run_as
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_user(
        self,
        *,
        username: str,
        email: t.Optional[t.Union[None, str]] = None,
        enabled: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        full_name: t.Optional[t.Union[None, str]] = None,
        human: t.Optional[bool] = None,
        metadata: t.Optional[t.Mapping[str, t.Any]] = None,
        password: t.Optional[str] = None,
        password_hash: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
        roles: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Adds and updates users in the native realm. These users are commonly referred
        to as native users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-put-user.html>`_

        :param username: The username of the User
        :param email:
        :param enabled:
        :param full_name:
        :param metadata:
        :param password:
        :param password_hash:
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        :param roles:
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'username'")
        __path = f"/_security/user/{_quote(username)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if email is not None:
            __body["email"] = email
        if enabled is not None:
            __body["enabled"] = enabled
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if full_name is not None:
            __body["full_name"] = full_name
        if human is not None:
            __query["human"] = human
        if metadata is not None:
            __body["metadata"] = metadata
        if password is not None:
            __body["password"] = password
        if password_hash is not None:
            __body["password_hash"] = password_hash
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        if roles is not None:
            __body["roles"] = roles
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
        parameter_aliases={"from": "from_"},
    )
    def query_api_keys(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        from_: t.Optional[int] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        query: t.Optional[t.Mapping[str, t.Any]] = None,
        search_after: t.Optional[
            t.Union[
                t.List[t.Union[None, bool, float, int, str, t.Any]],
                t.Tuple[t.Union[None, bool, float, int, str, t.Any], ...],
            ]
        ] = None,
        size: t.Optional[int] = None,
        sort: t.Optional[
            t.Union[
                t.Union[str, t.Mapping[str, t.Any]],
                t.Union[
                    t.List[t.Union[str, t.Mapping[str, t.Any]]],
                    t.Tuple[t.Union[str, t.Mapping[str, t.Any]], ...],
                ],
            ]
        ] = None,
        with_limited_by: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves information for API keys using a subset of query DSL

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-query-api-key.html>`_

        :param from_: Starting document offset. By default, you cannot page through more
            than 10,000 hits using the from and size parameters. To page through more
            hits, use the search_after parameter.
        :param query: A query to filter which API keys to return. The query supports
            a subset of query types, including match_all, bool, term, terms, ids, prefix,
            wildcard, and range. You can query all public information associated with
            an API key
        :param search_after:
        :param size: The number of hits to return. By default, you cannot page through
            more than 10,000 hits using the from and size parameters. To page through
            more hits, use the search_after parameter.
        :param sort:
        :param with_limited_by: Return the snapshot of the owner user's role descriptors
            associated with the API key. An API key's actual permission is the intersection
            of its assigned role descriptors and the owner user's role descriptors.
        """
        __path = "/_security/_query/api_key"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        # The 'sort' parameter with a colon can't be encoded to the body.
        if sort is not None and (
            (isinstance(sort, str) and ":" in sort)
            or (
                isinstance(sort, (list, tuple))
                and all(isinstance(_x, str) for _x in sort)
                and any(":" in _x for _x in sort)
            )
        ):
            __query["sort"] = sort
            sort = None
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if from_ is not None:
            __body["from"] = from_
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if query is not None:
            __body["query"] = query
        if search_after is not None:
            __body["search_after"] = search_after
        if size is not None:
            __body["size"] = size
        if sort is not None:
            __body["sort"] = sort
        if with_limited_by is not None:
            __query["with_limited_by"] = with_limited_by
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def saml_authenticate(
        self,
        *,
        content: str,
        ids: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        realm: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Exchanges a SAML Response message for an Elasticsearch access token and refresh
        token pair

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-saml-authenticate.html>`_

        :param content: The SAML response as it was sent by the user’s browser, usually
            a Base64 encoded XML document.
        :param ids: A json array with all the valid SAML Request Ids that the caller
            of the API has for the current user.
        :param realm: The name of the realm that should authenticate the SAML response.
            Useful in cases where many SAML realms are defined.
        """
        if content is None:
            raise ValueError("Empty value passed for parameter 'content'")
        if ids is None:
            raise ValueError("Empty value passed for parameter 'ids'")
        __path = "/_security/saml/authenticate"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if content is not None:
            __body["content"] = content
        if ids is not None:
            __body["ids"] = ids
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if realm is not None:
            __body["realm"] = realm
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def saml_complete_logout(
        self,
        *,
        ids: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        realm: str,
        content: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        query_string: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Verifies the logout response sent from the SAML IdP

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-saml-complete-logout.html>`_

        :param ids: A json array with all the valid SAML Request Ids that the caller
            of the API has for the current user.
        :param realm: The name of the SAML realm in Elasticsearch for which the configuration
            is used to verify the logout response.
        :param content: If the SAML IdP sends the logout response with the HTTP-Post
            binding, this field must be set to the value of the SAMLResponse form parameter
            from the logout response.
        :param query_string: If the SAML IdP sends the logout response with the HTTP-Redirect
            binding, this field must be set to the query string of the redirect URI.
        """
        if ids is None:
            raise ValueError("Empty value passed for parameter 'ids'")
        if realm is None:
            raise ValueError("Empty value passed for parameter 'realm'")
        __path = "/_security/saml/complete_logout"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if ids is not None:
            __body["ids"] = ids
        if realm is not None:
            __body["realm"] = realm
        if content is not None:
            __body["content"] = content
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if query_string is not None:
            __body["query_string"] = query_string
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def saml_invalidate(
        self,
        *,
        query_string: str,
        acs: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        realm: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Consumes a SAML LogoutRequest

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-saml-invalidate.html>`_

        :param query_string: The query part of the URL that the user was redirected to
            by the SAML IdP to initiate the Single Logout. This query should include
            a single parameter named SAMLRequest that contains a SAML logout request
            that is deflated and Base64 encoded. If the SAML IdP has signed the logout
            request, the URL should include two extra parameters named SigAlg and Signature
            that contain the algorithm used for the signature and the signature value
            itself. In order for Elasticsearch to be able to verify the IdP’s signature,
            the value of the query_string field must be an exact match to the string
            provided by the browser. The client application must not attempt to parse
            or process the string in any way.
        :param acs: The Assertion Consumer Service URL that matches the one of the SAML
            realm in Elasticsearch that should be used. You must specify either this
            parameter or the realm parameter.
        :param realm: The name of the SAML realm in Elasticsearch the configuration.
            You must specify either this parameter or the acs parameter.
        """
        if query_string is None:
            raise ValueError("Empty value passed for parameter 'query_string'")
        __path = "/_security/saml/invalidate"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if query_string is not None:
            __body["query_string"] = query_string
        if acs is not None:
            __body["acs"] = acs
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if realm is not None:
            __body["realm"] = realm
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def saml_logout(
        self,
        *,
        token: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        refresh_token: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Invalidates an access token and a refresh token that were generated via the SAML
        Authenticate API

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-saml-logout.html>`_

        :param token: The access token that was returned as a response to calling the
            SAML authenticate API. Alternatively, the most recent token that was received
            after refreshing the original one by using a refresh_token.
        :param refresh_token: The refresh token that was returned as a response to calling
            the SAML authenticate API. Alternatively, the most recent refresh token that
            was received after refreshing the original access token.
        """
        if token is None:
            raise ValueError("Empty value passed for parameter 'token'")
        __path = "/_security/saml/logout"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if token is not None:
            __body["token"] = token
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh_token is not None:
            __body["refresh_token"] = refresh_token
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def saml_prepare_authentication(
        self,
        *,
        acs: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        realm: t.Optional[str] = None,
        relay_state: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a SAML authentication request

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-saml-prepare-authentication.html>`_

        :param acs: The Assertion Consumer Service URL that matches the one of the SAML
            realms in Elasticsearch. The realm is used to generate the authentication
            request. You must specify either this parameter or the realm parameter.
        :param realm: The name of the SAML realm in Elasticsearch for which the configuration
            is used to generate the authentication request. You must specify either this
            parameter or the acs parameter.
        :param relay_state: A string that will be included in the redirect URL that this
            API returns as the RelayState query parameter. If the Authentication Request
            is signed, this value is used as part of the signature computation.
        """
        __path = "/_security/saml/prepare"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if acs is not None:
            __body["acs"] = acs
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if realm is not None:
            __body["realm"] = realm
        if relay_state is not None:
            __body["relay_state"] = relay_state
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def saml_service_provider_metadata(
        self,
        *,
        realm_name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Generates SAML metadata for the Elastic stack SAML 2.0 Service Provider

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-saml-sp-metadata.html>`_

        :param realm_name: The name of the SAML realm in Elasticsearch.
        """
        if realm_name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'realm_name'")
        __path = f"/_security/saml/metadata/{_quote(realm_name)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def suggest_user_profiles(
        self,
        *,
        data: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        hint: t.Optional[t.Mapping[str, t.Any]] = None,
        human: t.Optional[bool] = None,
        name: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Get suggestions for user profiles that match specified search criteria.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-suggest-user-profile.html>`_

        :param data: List of filters for the `data` field of the profile document. To
            return all content use `data=*`. To return a subset of content use `data=<key>`
            to retrieve content nested under the specified `<key>`. By default returns
            no `data` content.
        :param hint: Extra search criteria to improve relevance of the suggestion result.
            Profiles matching the spcified hint are ranked higher in the response. Profiles
            not matching the hint don't exclude the profile from the response as long
            as the profile matches the `name` field query.
        :param name: Query string used to match name-related fields in user profile documents.
            Name-related fields are the user's `username`, `full_name`, and `email`.
        :param size: Number of profiles to return.
        """
        __path = "/_security/profile/_suggest"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if data is not None:
            __body["data"] = data
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if hint is not None:
            __body["hint"] = hint
        if human is not None:
            __query["human"] = human
        if name is not None:
            __body["name"] = name
        if pretty is not None:
            __query["pretty"] = pretty
        if size is not None:
            __body["size"] = size
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def update_api_key(
        self,
        *,
        id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        metadata: t.Optional[t.Mapping[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        role_descriptors: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates attributes of an existing API key.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-update-api-key.html>`_

        :param id: The ID of the API key to update.
        :param metadata: Arbitrary metadata that you want to associate with the API key.
            It supports nested data structure. Within the metadata object, keys beginning
            with _ are reserved for system usage.
        :param role_descriptors: An array of role descriptors for this API key. This
            parameter is optional. When it is not specified or is an empty array, then
            the API key will have a point in time snapshot of permissions of the authenticated
            user. If you supply role descriptors then the resultant permissions would
            be an intersection of API keys permissions and authenticated user’s permissions
            thereby limiting the access scope for API keys. The structure of role descriptor
            is the same as the request for create role API. For more details, see create
            or update roles API.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_security/api_key/{_quote(id)}"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if metadata is not None:
            __body["metadata"] = metadata
        if pretty is not None:
            __query["pretty"] = pretty
        if role_descriptors is not None:
            __body["role_descriptors"] = role_descriptors
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def update_user_profile_data(
        self,
        *,
        uid: str,
        data: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        if_primary_term: t.Optional[int] = None,
        if_seq_no: t.Optional[int] = None,
        labels: t.Optional[t.Mapping[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        refresh: t.Optional[
            t.Union["t.Literal['false', 'true', 'wait_for']", bool, str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Update application specific data for the user profile of the given unique ID.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/security-api-update-user-profile-data.html>`_

        :param uid: A unique identifier for the user profile.
        :param data: Non-searchable data that you want to associate with the user profile.
            This field supports a nested data structure.
        :param if_primary_term: Only perform the operation if the document has this primary
            term.
        :param if_seq_no: Only perform the operation if the document has this sequence
            number.
        :param labels: Searchable data that you want to associate with the user profile.
            This field supports a nested data structure.
        :param refresh: If 'true', Elasticsearch refreshes the affected shards to make
            this operation visible to search, if 'wait_for' then wait for a refresh to
            make this operation visible to search, if 'false' do nothing with refreshes.
        """
        if uid in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'uid'")
        __path = f"/_security/profile/{_quote(uid)}/_data"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if data is not None:
            __body["data"] = data
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if if_primary_term is not None:
            __query["if_primary_term"] = if_primary_term
        if if_seq_no is not None:
            __query["if_seq_no"] = if_seq_no
        if labels is not None:
            __body["labels"] = labels
        if pretty is not None:
            __query["pretty"] = pretty
        if refresh is not None:
            __query["refresh"] = refresh
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )
