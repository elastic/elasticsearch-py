from ..utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class LicenseClient(NamespacedClient):
    @query_params()
    def delete(self, params=None):
        """
        `<https://www.elastic.co/guide/en/x-pack/current/license-management.html>`_
        """
        return self.transport.perform_request("DELETE", "/_license", params=params)

    @query_params("local")
    def get(self, params=None):
        """
        `<https://www.elastic.co/guide/en/x-pack/current/license-management.html>`_

        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        """
        return self.transport.perform_request("GET", "/_license", params=params)

    @query_params()
    def get_basic_status(self, params=None):
        """
        `<https://www.elastic.co/guide/en/x-pack/current/license-management.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_license/basic_status", params=params
        )

    @query_params()
    def get_trial_status(self, params=None):
        """
        `<https://www.elastic.co/guide/en/x-pack/current/license-management.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_license/trial_status", params=params
        )

    @query_params("acknowledge")
    def post(self, body=None, params=None):
        """
        `<https://www.elastic.co/guide/en/x-pack/current/license-management.html>`_

        :arg body: licenses to be installed
        :arg acknowledge: whether the user has acknowledged acknowledge messages
            (default: false)
        """
        return self.transport.perform_request(
            "PUT", "/_license", params=params, body=body
        )

    @query_params("acknowledge")
    def post_start_basic(self, params=None):
        """
        `<https://www.elastic.co/guide/en/x-pack/current/license-management.html>`_

        :arg acknowledge: whether the user has acknowledged acknowledge messages
            (default: false)
        """
        return self.transport.perform_request(
            "POST", "/_license/start_basic", params=params
        )

    @query_params("acknowledge", "doc_type")
    def post_start_trial(self, params=None):
        """
        `<https://www.elastic.co/guide/en/x-pack/current/license-management.html>`_

        :arg acknowledge: whether the user has acknowledged acknowledge messages
            (default: false)
        :arg doc_type: The type of trial license to generate (default: "trial")
        """
        return self.transport.perform_request(
            "POST", "/_license/start_trial", params=params
        )
