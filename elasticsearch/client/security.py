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

from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class SecurityClient(NamespacedClient):
    @query_params()
    def authenticate(self, params=None, headers=None):
        """
        Enables authentication as a user and retrieve information about the
        authenticated user.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-authenticate.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_security/_authenticate", params=params, headers=headers
        )

    @query_params("refresh")
    def change_password(self, body, username=None, params=None, headers=None):
        """
        Changes the passwords of users in the native realm and built-in users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-change-password.html>`_

        :arg body: the new password for the user
        :arg username: The username of the user to change the password
            for
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_security", "user", username, "_password"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("usernames")
    def clear_cached_realms(self, realms, params=None, headers=None):
        """
        Evicts users from the user cache. Can completely clear the cache or evict
        specific users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-clear-cache.html>`_

        :arg realms: Comma-separated list of realms to clear
        :arg usernames: Comma-separated list of usernames to clear from
            the cache
        """
        if realms in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'realms'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_security", "realm", realms, "_clear_cache"),
            params=params,
            headers=headers,
        )

    @query_params()
    def clear_cached_roles(self, name, params=None, headers=None):
        """
        Evicts roles from the native role cache.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-clear-role-cache.html>`_

        :arg name: Role name
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_security", "role", name, "_clear_cache"),
            params=params,
            headers=headers,
        )

    @query_params("refresh")
    def create_api_key(self, body, params=None, headers=None):
        """
        Creates an API key for access without requiring basic authentication.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-create-api-key.html>`_

        :arg body: The api key request to create an API key
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PUT", "/_security/api_key", params=params, headers=headers, body=body
        )

    @query_params("refresh")
    def delete_privileges(self, application, name, params=None, headers=None):
        """
        Removes application privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-delete-privilege.html>`_

        :arg application: Application name
        :arg name: Privilege name
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        for param in (application, name):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_security", "privilege", application, name),
            params=params,
            headers=headers,
        )

    @query_params("refresh")
    def delete_role(self, name, params=None, headers=None):
        """
        Removes roles in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-delete-role.html>`_

        :arg name: Role name
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_security", "role", name),
            params=params,
            headers=headers,
        )

    @query_params("refresh")
    def delete_role_mapping(self, name, params=None, headers=None):
        """
        Removes role mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-delete-role-mapping.html>`_

        :arg name: Role-mapping name
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_security", "role_mapping", name),
            params=params,
            headers=headers,
        )

    @query_params("refresh")
    def delete_user(self, username, params=None, headers=None):
        """
        Deletes users from the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-delete-user.html>`_

        :arg username: username
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_security", "user", username),
            params=params,
            headers=headers,
        )

    @query_params("refresh")
    def disable_user(self, username, params=None, headers=None):
        """
        Disables users in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-disable-user.html>`_

        :arg username: The username of the user to disable
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_security", "user", username, "_disable"),
            params=params,
            headers=headers,
        )

    @query_params("refresh")
    def enable_user(self, username, params=None, headers=None):
        """
        Enables users in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-enable-user.html>`_

        :arg username: The username of the user to enable
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_security", "user", username, "_enable"),
            params=params,
            headers=headers,
        )

    @query_params("id", "name", "owner", "realm_name", "username")
    def get_api_key(self, params=None, headers=None):
        """
        Retrieves information for one or more API keys.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-get-api-key.html>`_

        :arg id: API key id of the API key to be retrieved
        :arg name: API key name of the API key to be retrieved
        :arg owner: flag to query API keys owned by the currently
            authenticated user
        :arg realm_name: realm name of the user who created this API key
            to be retrieved
        :arg username: user name of the user who created this API key to
            be retrieved
        """
        return self.transport.perform_request(
            "GET", "/_security/api_key", params=params, headers=headers
        )

    @query_params()
    def get_privileges(self, application=None, name=None, params=None, headers=None):
        """
        Retrieves application privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-get-privileges.html>`_

        :arg application: Application name
        :arg name: Privilege name
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_security", "privilege", application, name),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_role(self, name=None, params=None, headers=None):
        """
        Retrieves roles in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-get-role.html>`_

        :arg name: A comma-separated list of role names
        """
        return self.transport.perform_request(
            "GET", _make_path("_security", "role", name), params=params, headers=headers
        )

    @query_params()
    def get_role_mapping(self, name=None, params=None, headers=None):
        """
        Retrieves role mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-get-role-mapping.html>`_

        :arg name: A comma-separated list of role-mapping names
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_security", "role_mapping", name),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_token(self, body, params=None, headers=None):
        """
        Creates a bearer token for access without requiring basic authentication.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-get-token.html>`_

        :arg body: The token request to get
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST", "/_security/oauth2/token", params=params, headers=headers, body=body
        )

    @query_params()
    def get_user(self, username=None, params=None, headers=None):
        """
        Retrieves information about users in the native realm and built-in users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-get-user.html>`_

        :arg username: A comma-separated list of usernames
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_security", "user", username),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_user_privileges(self, params=None, headers=None):
        """
        Retrieves application privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-get-privileges.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_security/user/_privileges", params=params, headers=headers
        )

    @query_params()
    def has_privileges(self, body, user=None, params=None, headers=None):
        """
        Determines whether the specified user has a specified list of privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-has-privileges.html>`_

        :arg body: The privileges to test
        :arg user: Username
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_security", "user", user, "_has_privileges"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def invalidate_api_key(self, body, params=None, headers=None):
        """
        Invalidates one or more API keys.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-invalidate-api-key.html>`_

        :arg body: The api key request to invalidate API key(s)
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "DELETE", "/_security/api_key", params=params, headers=headers, body=body
        )

    @query_params()
    def invalidate_token(self, body, params=None, headers=None):
        """
        Invalidates one or more access tokens or refresh tokens.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-invalidate-token.html>`_

        :arg body: The token to invalidate
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "DELETE",
            "/_security/oauth2/token",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("refresh")
    def put_privileges(self, body, params=None, headers=None):
        """
        Adds or updates application privileges.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-put-privileges.html>`_

        :arg body: The privilege(s) to add
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "PUT", "/_security/privilege/", params=params, headers=headers, body=body
        )

    @query_params("refresh")
    def put_role(self, name, body, params=None, headers=None):
        """
        Adds and updates roles in the native realm.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-put-role.html>`_

        :arg name: Role name
        :arg body: The role to add
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_security", "role", name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("refresh")
    def put_role_mapping(self, name, body, params=None, headers=None):
        """
        Creates and updates role mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-put-role-mapping.html>`_

        :arg name: Role-mapping name
        :arg body: The role mapping to add
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_security", "role_mapping", name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("refresh")
    def put_user(self, username, body, params=None, headers=None):
        """
        Adds and updates users in the native realm. These users are commonly referred
        to as native users.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-put-user.html>`_

        :arg username: The username of the User
        :arg body: The user to add
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        for param in (username, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_security", "user", username),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def get_builtin_privileges(self, params=None, headers=None):
        """
        Retrieves the list of cluster privileges and index privileges that are
        available in this version of Elasticsearch.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-get-builtin-privileges.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_security/privilege/_builtin", params=params, headers=headers
        )

    @query_params()
    def clear_cached_privileges(self, application, params=None, headers=None):
        """
        Evicts application privileges from the native application privileges cache.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-clear-privilege-cache.html>`_

        :arg application: A comma-separated list of application names
        """
        if application in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'application'."
            )

        return self.transport.perform_request(
            "POST",
            _make_path("_security", "privilege", application, "_clear_cache"),
            params=params,
            headers=headers,
        )

    @query_params()
    def clear_api_key_cache(self, ids, params=None, headers=None):
        """
        Clear a subset or all entries from the API key cache.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-clear-api-key-cache.html>`_

        :arg ids: A comma-separated list of IDs of API keys to clear
            from the cache
        """
        if ids in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'ids'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_security", "api_key", ids, "_clear_cache"),
            params=params,
            headers=headers,
        )

    @query_params("refresh")
    def grant_api_key(self, body, params=None, headers=None):
        """
        Creates an API key on behalf of another user.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/security-api-grant-api-key.html>`_

        :arg body: The api key request to create an API key
        :arg refresh: If `true` (the default) then refresh the affected
            shards to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false` then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST",
            "/_security/api_key/grant",
            params=params,
            headers=headers,
            body=body,
        )
