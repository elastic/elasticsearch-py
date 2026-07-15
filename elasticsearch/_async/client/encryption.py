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
from .utils import (
    Stability,
    _availability_warning,
    _rewrite_parameters,
)


class EncryptionClient(NamespacedClient):

    @_rewrite_parameters()
    @_availability_warning(Stability.EXPERIMENTAL)
    async def reset(
        self,
        *,
        accept_data_loss: bool,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Reset the project encryption key.</p>
          <p>Destroy the current project encryption key (PEK) and generate a new one.
          This is the recovery path for when the on-disk encrypted PEK becomes permanently
          inaccessible, for example because the key encryption material protecting it was lost.</p>
          <p>All data that was encrypted under the destroyed key becomes permanently unrecoverable.
          Each feature that stores encrypted data decides how to handle its own data during the
          reset: some features drop the encrypted values entirely, while others preserve the rest
          of the affected data and only clear the values that can no longer be decrypted.</p>
          <p>Because this operation causes permanent data loss, it requires the <code>accept_data_loss</code>
          query parameter to be set to <code>true</code>.</p>


        `<https://www.elastic.co/docs/api/doc/elasticsearch#TODO>`_

        :param accept_data_loss: Acknowledge that resetting the project encryption key
            permanently destroys all data that was encrypted under the current key. The
            request fails if this is not set to `true`.
        :param master_timeout: The period to wait for a connection to the master node.
            If no response is received before the timeout expires, the request fails
            and returns an error.
        :param timeout: The period to wait for a response. If no response is received
            before the timeout expires, the request fails and returns an error.
        """
        if accept_data_loss is None:
            raise ValueError("Empty value passed for parameter 'accept_data_loss'")
        __path_parts: t.Dict[str, str] = {}
        __path = "/_encryption/_reset"
        __query: t.Dict[str, t.Any] = {}
        if accept_data_loss is not None:
            __query["accept_data_loss"] = accept_data_loss
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "POST",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="encryption.reset",
            path_parts=__path_parts,
        )
