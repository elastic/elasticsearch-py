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

from typing import Any, Dict, List, Optional, Union

from elastic_transport import ObjectApiResponse

from ._base import NamespacedClient
from .utils import SKIP_IN_PATH, _quote, _quote_query, _rewrite_parameters


class SecurityClient(NamespacedClient):
    @_rewrite_parameters()
    async def authenticate(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Enables authentication as a user and retrieve information about the authenticated
        user.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-authenticate.html>`_
        """
        __path = "/_security/_authenticate"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def change_password(
        self,
        *,
        username: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        password: Optional[Any] = None,
        password_hash: Optional[str] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Changes the passwords of users in the native realm and built-in users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-change-password.html>`_

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
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def clear_api_key_cache(
        self,
        *,
        ids: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Clear a subset or all entries from the API key cache.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-clear-api-key-cache.html>`_

        :param ids: A comma-separated list of IDs of API keys to clear from the cache
        """
        if ids in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'ids'")
        __path = f"/_security/api_key/{_quote(ids)}/_clear_cache"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def clear_cached_privileges(
        self,
        *,
        application: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Evicts application privileges from the native application privileges cache.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-clear-privilege-cache.html>`_

        :param application: A comma-separated list of application names
        """
        if application in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'application'")
        __path = f"/_security/privilege/{_quote(application)}/_clear_cache"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def clear_cached_realms(
        self,
        *,
        realms: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        usernames: Optional[List[str]] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Evicts users from the user cache. Can completely clear the cache or evict specific
        users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-clear-cache.html>`_

        :param realms: Comma-separated list of realms to clear
        :param usernames: Comma-separated list of usernames to clear from the cache
        """
        if realms in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'realms'")
        __path = f"/_security/realm/{_quote(realms)}/_clear_cache"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def clear_cached_roles(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Evicts roles from the native role cache.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-clear-role-cache.html>`_

        :param name: Role name
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/role/{_quote(name)}/_clear_cache"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def clear_cached_service_tokens(
        self,
        *,
        namespace: Any,
        service: Any,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Evicts tokens from the service account token caches.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-clear-service-token-caches.html>`_

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
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def create_api_key(
        self,
        *,
        error_trace: Optional[bool] = None,
        expiration: Optional[Any] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        metadata: Optional[Any] = None,
        name: Optional[Any] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
        role_descriptors: Optional[Dict[str, Any]] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates an API key for access without requiring basic authentication.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html>`_

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
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def create_service_token(
        self,
        *,
        namespace: Any,
        service: Any,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a service account token for access without requiring basic authentication.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-service-token.html>`_

        :param namespace: An identifier for the namespace
        :param service: An identifier for the service name
        :param name: An identifier for the token name
        """
        if namespace in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'namespace'")
        if service in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'service'")
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
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
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request(__method, __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def delete_privileges(
        self,
        *,
        application: Any,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Removes application privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-delete-privilege.html>`_

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
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("DELETE", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def delete_role(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Removes roles in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-delete-role.html>`_

        :param name: Role name
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/role/{_quote(name)}"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("DELETE", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def delete_role_mapping(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Removes role mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-delete-role-mapping.html>`_

        :param name: Role-mapping name
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_security/role_mapping/{_quote(name)}"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("DELETE", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def delete_service_token(
        self,
        *,
        namespace: Any,
        service: Any,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes a service account token.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-delete-service-token.html>`_

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
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("DELETE", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def delete_user(
        self,
        *,
        username: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes users from the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-delete-user.html>`_

        :param username: username
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'username'")
        __path = f"/_security/user/{_quote(username)}"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("DELETE", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def disable_user(
        self,
        *,
        username: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Disables users in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-disable-user.html>`_

        :param username: The username of the user to disable
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'username'")
        __path = f"/_security/user/{_quote(username)}/_disable"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("PUT", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def enable_user(
        self,
        *,
        username: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Enables users in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-enable-user.html>`_

        :param username: The username of the user to enable
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'username'")
        __path = f"/_security/user/{_quote(username)}/_enable"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("PUT", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_api_key(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        id: Optional[Any] = None,
        name: Optional[Any] = None,
        owner: Optional[bool] = None,
        pretty: Optional[bool] = None,
        realm_name: Optional[Any] = None,
        username: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves information for one or more API keys.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-api-key.html>`_

        :param id: API key id of the API key to be retrieved
        :param name: API key name of the API key to be retrieved
        :param owner: flag to query API keys owned by the currently authenticated user
        :param realm_name: realm name of the user who created this API key to be retrieved
        :param username: user name of the user who created this API key to be retrieved
        """
        __path = "/_security/api_key"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_builtin_privileges(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves the list of cluster privileges and index privileges that are available
        in this version of Elasticsearch.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-builtin-privileges.html>`_
        """
        __path = "/_security/privilege/_builtin"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_privileges(
        self,
        *,
        application: Optional[Any] = None,
        name: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves application privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-privileges.html>`_

        :param application: Application name
        :param name: Privilege name
        """
        if application not in SKIP_IN_PATH and name not in SKIP_IN_PATH:
            __path = f"/_security/privilege/{_quote(application)}/{_quote(name)}"
        elif application not in SKIP_IN_PATH:
            __path = f"/_security/privilege/{_quote(application)}"
        else:
            __path = "/_security/privilege"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_role(
        self,
        *,
        name: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves roles in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-role.html>`_

        :param name: A comma-separated list of role names
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_security/role/{_quote(name)}"
        else:
            __path = "/_security/role"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_role_mapping(
        self,
        *,
        name: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves role mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-role-mapping.html>`_

        :param name: A comma-separated list of role-mapping names
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_security/role_mapping/{_quote(name)}"
        else:
            __path = "/_security/role_mapping"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_service_accounts(
        self,
        *,
        namespace: Optional[Any] = None,
        service: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves information about service accounts.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-service-accounts.html>`_

        :param namespace: An identifier for the namespace
        :param service: An identifier for the service name
        """
        if namespace not in SKIP_IN_PATH and service not in SKIP_IN_PATH:
            __path = f"/_security/service/{_quote(namespace)}/{_quote(service)}"
        elif namespace not in SKIP_IN_PATH:
            __path = f"/_security/service/{_quote(namespace)}"
        else:
            __path = "/_security/service"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_service_credentials(
        self,
        *,
        namespace: Any,
        service: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves information of all service credentials for a service account.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-service-credentials.html>`_

        :param namespace: Name of the namespace.
        :param service: Name of the service name.
        """
        if namespace in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'namespace'")
        if service in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'service'")
        __path = f"/_security/service/{_quote(namespace)}/{_quote(service)}/credential"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def get_token(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        grant_type: Optional[Any] = None,
        human: Optional[bool] = None,
        kerberos_ticket: Optional[str] = None,
        password: Optional[Any] = None,
        pretty: Optional[bool] = None,
        refresh_token: Optional[str] = None,
        scope: Optional[str] = None,
        username: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a bearer token for access without requiring basic authentication.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-token.html>`_

        :param grant_type:
        :param kerberos_ticket:
        :param password:
        :param refresh_token:
        :param scope:
        :param username:
        """
        __path = "/_security/oauth2/token"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_user(
        self,
        *,
        username: Optional[Union[Any, List[Any]]] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves information about users in the native realm and built-in users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-user.html>`_

        :param username: An identifier for the user. You can specify multiple usernames
            as a comma-separated list. If you omit this parameter, the API retrieves
            information about all users.
        """
        if username not in SKIP_IN_PATH:
            __path = f"/_security/user/{_quote(username)}"
        else:
            __path = "/_security/user"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_user_privileges(
        self,
        *,
        application: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        priviledge: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves security privileges for the logged in user.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-user-privileges.html>`_

        :param application: The name of the application. Application privileges are always
            associated with exactly one application. If you do not specify this parameter,
            the API returns information about all privileges for all applications.
        :param priviledge: The name of the privilege. If you do not specify this parameter,
            the API returns information about all privileges for the requested application.
        """
        __path = "/_security/user/_privileges"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
        ignore_deprecated_options={"api_key"},
    )
    async def grant_api_key(
        self,
        *,
        api_key: Any,
        grant_type: Any,
        access_token: Optional[str] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        password: Optional[Any] = None,
        pretty: Optional[bool] = None,
        username: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates an API key on behalf of another user.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-grant-api-key.html>`_

        :param api_key:
        :param grant_type:
        :param access_token:
        :param password:
        :param username:
        """
        if api_key is None:
            raise ValueError("Empty value passed for parameter 'api_key'")
        if grant_type is None:
            raise ValueError("Empty value passed for parameter 'grant_type'")
        __path = "/_security/api_key/grant"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
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
        if username is not None:
            __body["username"] = username
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def has_privileges(
        self,
        *,
        user: Optional[Any] = None,
        application: Optional[List[Any]] = None,
        cluster: Optional[List[Any]] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        index: Optional[List[Any]] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Determines whether the specified user has a specified list of privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-has-privileges.html>`_

        :param user: Username
        :param application:
        :param cluster:
        :param index:
        """
        if user not in SKIP_IN_PATH:
            __path = f"/_security/user/{_quote(user)}/_has_privileges"
        else:
            __path = "/_security/user/_has_privileges"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def invalidate_api_key(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        id: Optional[Any] = None,
        ids: Optional[List[Any]] = None,
        name: Optional[Any] = None,
        owner: Optional[bool] = None,
        pretty: Optional[bool] = None,
        realm_name: Optional[str] = None,
        username: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Invalidates one or more API keys.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-invalidate-api-key.html>`_

        :param id:
        :param ids:
        :param name:
        :param owner:
        :param realm_name:
        :param username:
        """
        __path = "/_security/api_key"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("DELETE", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def invalidate_token(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        realm_name: Optional[Any] = None,
        refresh_token: Optional[str] = None,
        token: Optional[str] = None,
        username: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Invalidates one or more access tokens or refresh tokens.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-invalidate-token.html>`_

        :param realm_name:
        :param refresh_token:
        :param token:
        :param username:
        """
        __path = "/_security/oauth2/token"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("DELETE", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_name="privileges",
    )
    async def put_privileges(
        self,
        *,
        privileges: Dict[str, Dict[str, Any]],
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Adds or updates application privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-privileges.html>`_

        :param privileges:
        :param refresh: If `true` (the default) then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh to
            make this operation visible to search, if `false` then do nothing with refreshes.
        """
        if privileges is None:
            raise ValueError("Empty value passed for parameter 'privileges'")
        __path = "/_security/privilege"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
        parameter_aliases={"global": "global_"},
    )
    async def put_role(
        self,
        *,
        name: Any,
        applications: Optional[List[Any]] = None,
        cluster: Optional[List[Any]] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        global_: Optional[Dict[str, Any]] = None,
        human: Optional[bool] = None,
        indices: Optional[List[Any]] = None,
        metadata: Optional[Any] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
        run_as: Optional[List[str]] = None,
        transient_metadata: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Adds and updates roles in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-role.html>`_

        :param name: Role name
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
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def put_role_mapping(
        self,
        *,
        name: Any,
        enabled: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        metadata: Optional[Any] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
        roles: Optional[List[str]] = None,
        rules: Optional[Any] = None,
        run_as: Optional[List[str]] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates and updates role mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-role-mapping.html>`_

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
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def put_user(
        self,
        *,
        username: Any,
        email: Optional[Union[None, str]] = None,
        enabled: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        full_name: Optional[Union[None, str]] = None,
        human: Optional[bool] = None,
        metadata: Optional[Any] = None,
        password: Optional[Any] = None,
        password_hash: Optional[str] = None,
        pretty: Optional[bool] = None,
        refresh: Optional[Any] = None,
        roles: Optional[List[str]] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Adds and updates users in the native realm. These users are commonly referred
        to as native users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-user.html>`_

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
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]
