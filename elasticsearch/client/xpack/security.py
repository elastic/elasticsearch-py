from ..utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class SecurityClient(NamespacedClient):
    @query_params()
    def authenticate(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-authenticate.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_security/_authenticate", params=params
        )

    @query_params("refresh")
    def change_password(self, body, username=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-change-password.html>`_

        :arg body: the new password for the user
        :arg username: The username of the user to change the password for
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "PUT",
            _make_path("_security", "user", username, "_password"),
            params=params,
            body=body,
        )

    @query_params("usernames")
    def clear_cached_realms(self, realms, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-clear-cache.html>`_

        :arg realms: Comma-separated list of realms to clear
        :arg usernames: Comma-separated list of usernames to clear from the
            cache
        """
        if realms in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'realms'.")
        return self.transport.perform_request(
            "POST",
            _make_path("_security", "realm", realms, "_clear_cache"),
            params=params,
        )

    @query_params()
    def clear_cached_roles(self, name, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-clear-role-cache.html>`_

        :arg name: Role name
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")
        return self.transport.perform_request(
            "POST", _make_path("_security", "role", name, "_clear_cache"), params=params
        )

    @query_params("refresh")
    def create_api_key(self, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html>`_

        :arg body: The api key request to create an API key
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "PUT", "/_security/api_key", params=params, body=body
        )

    @query_params("refresh")
    def delete_privileges(self, application, name, params=None):
        """
        `<TODO>`_

        :arg application: Application name
        :arg name: Privilege name
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        for param in (application, name):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "DELETE",
            _make_path("_security", "privilege", application, name),
            params=params,
        )

    @query_params("refresh")
    def delete_role(self, name, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-delete-role.html>`_

        :arg name: Role name
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")
        return self.transport.perform_request(
            "DELETE", _make_path("_security", "role", name), params=params
        )

    @query_params("refresh")
    def delete_role_mapping(self, name, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-delete-role-mapping.html>`_

        :arg name: Role-mapping name
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")
        return self.transport.perform_request(
            "DELETE", _make_path("_security", "role_mapping", name), params=params
        )

    @query_params("refresh")
    def delete_user(self, username, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-delete-user.html>`_

        :arg username: username
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")
        return self.transport.perform_request(
            "DELETE", _make_path("_security", "user", username), params=params
        )

    @query_params("refresh")
    def disable_user(self, username, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-disable-user.html>`_

        :arg username: The username of the user to disable
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")
        return self.transport.perform_request(
            "PUT", _make_path("_security", "user", username, "_disable"), params=params
        )

    @query_params("refresh")
    def enable_user(self, username, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-enable-user.html>`_

        :arg username: The username of the user to enable
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        if username in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'username'.")
        return self.transport.perform_request(
            "PUT", _make_path("_security", "user", username, "_enable"), params=params
        )

    @query_params("id", "name", "realm_name", "username")
    def get_api_key(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-api-key.html>`_

        :arg id: API key id of the API key to be retrieved
        :arg name: API key name of the API key to be retrieved
        :arg realm_name: realm name of the user who created this API key to be
            retrieved
        :arg username: user name of the user who created this API key to be
            retrieved
        """
        return self.transport.perform_request(
            "GET", "/_security/api_key", params=params
        )

    @query_params()
    def get_privileges(self, application=None, name=None, params=None):
        """
        `<TODO>`_

        :arg application: Application name
        :arg name: Privilege name
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_security", "privilege", application, name),
            params=params,
        )

    @query_params()
    def get_role(self, name=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-role.html>`_

        :arg name: Role name
        """
        return self.transport.perform_request(
            "GET", _make_path("_security", "role", name), params=params
        )

    @query_params()
    def get_role_mapping(self, name=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-role-mapping.html>`_

        :arg name: Role-Mapping name
        """
        return self.transport.perform_request(
            "GET", _make_path("_security", "role_mapping", name), params=params
        )

    @query_params()
    def get_token(self, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-token.html>`_

        :arg body: The token request to get
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "POST", "/_security/oauth2/token", params=params, body=body
        )

    @query_params()
    def get_user(self, username=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-user.html>`_

        :arg username: A comma-separated list of usernames
        """
        return self.transport.perform_request(
            "GET", _make_path("_security", "user", username), params=params
        )

    @query_params()
    def get_user_privileges(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-get-user-privileges.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_security/user/_privileges", params=params
        )

    @query_params()
    def has_privileges(self, body, user=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-has-privileges.html>`_

        :arg body: The privileges to test
        :arg user: Username
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "GET",
            _make_path("_security", "user", user, "_has_privileges"),
            params=params,
            body=body,
        )

    @query_params()
    def invalidate_api_key(self, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-invalidate-api-key.html>`_

        :arg body: The api key request to invalidate API key(s)
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "DELETE", "/_security/api_key", params=params, body=body
        )

    @query_params()
    def invalidate_token(self, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-invalidate-token.html>`_

        :arg body: The token to invalidate
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "DELETE", "/_security/oauth2/token", params=params, body=body
        )

    @query_params("refresh")
    def put_privileges(self, body, params=None):
        """
        `<TODO>`_

        :arg body: The privilege(s) to add
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "PUT", "/_security/privilege/", params=params, body=body
        )

    @query_params("refresh")
    def put_role(self, name, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-role.html>`_

        :arg name: Role name
        :arg body: The role to add
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "PUT", _make_path("_security", "role", name), params=params, body=body
        )

    @query_params("refresh")
    def put_role_mapping(self, name, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-role-mapping.html>`_

        :arg name: Role-mapping name
        :arg body: The role to add
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "PUT",
            _make_path("_security", "role_mapping", name),
            params=params,
            body=body,
        )

    @query_params("refresh")
    def put_user(self, username, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-user.html>`_

        :arg username: The username of the User
        :arg body: The user to add
        :arg refresh: If `true` (the default) then refresh the affected shards
            to make this operation visible to search, if `wait_for` then wait
            for a refresh to make this operation visible to search, if `false`
            then do nothing with refreshes., valid choices are: 'true', 'false',
            'wait_for'
        """
        for param in (username, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "PUT", _make_path("_security", "user", username), params=params, body=body
        )
