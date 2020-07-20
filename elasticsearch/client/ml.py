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

from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH, _bulk_body


class MlClient(NamespacedClient):
    @query_params("allow_no_jobs", "force", "timeout")
    def close_job(self, job_id, body=None, params=None, headers=None):
        """
        Closes one or more anomaly detection jobs. A job can be opened and closed
        multiple times throughout its lifecycle.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-close-job.html>`_

        :arg job_id: The name of the job to close
        :arg body: The URL params optionally sent in the body
        :arg allow_no_jobs: Whether to ignore if a wildcard expression
            matches no jobs. (This includes `_all` string or when no jobs have been
            specified)
        :arg force: True if the job should be forcefully closed
        :arg timeout: Controls the time to wait until a job has closed.
            Default to 30 minutes
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_close"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def delete_calendar(self, calendar_id, params=None, headers=None):
        """
        Deletes a calendar.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-delete-calendar.html>`_

        :arg calendar_id: The ID of the calendar to delete
        """
        if calendar_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'calendar_id'."
            )

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "calendars", calendar_id),
            params=params,
            headers=headers,
        )

    @query_params()
    def delete_calendar_event(self, calendar_id, event_id, params=None, headers=None):
        """
        Deletes scheduled events from a calendar.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-delete-calendar-event.html>`_

        :arg calendar_id: The ID of the calendar to modify
        :arg event_id: The ID of the event to remove from the calendar
        """
        for param in (calendar_id, event_id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "calendars", calendar_id, "events", event_id),
            params=params,
            headers=headers,
        )

    @query_params()
    def delete_calendar_job(self, calendar_id, job_id, params=None, headers=None):
        """
        Deletes anomaly detection jobs from a calendar.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-delete-calendar-job.html>`_

        :arg calendar_id: The ID of the calendar to modify
        :arg job_id: The ID of the job to remove from the calendar
        """
        for param in (calendar_id, job_id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "calendars", calendar_id, "jobs", job_id),
            params=params,
            headers=headers,
        )

    @query_params("force")
    def delete_datafeed(self, datafeed_id, params=None, headers=None):
        """
        Deletes an existing datafeed.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-delete-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to delete
        :arg force: True if the datafeed should be forcefully deleted
        """
        if datafeed_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'datafeed_id'."
            )

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "datafeeds", datafeed_id),
            params=params,
            headers=headers,
        )

    @query_params("requests_per_second", "timeout")
    def delete_expired_data(self, body=None, job_id=None, params=None, headers=None):
        """
        Deletes expired and unused machine learning data.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-delete-expired-data.html>`_

        :arg body: deleting expired data parameters
        :arg job_id: The ID of the job(s) to perform expired data
            hygiene for
        :arg requests_per_second: The desired requests per second for
            the deletion processes.
        :arg timeout: How long can the underlying delete processes run
            until they are canceled
        """
        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "_delete_expired_data", job_id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def delete_filter(self, filter_id, params=None, headers=None):
        """
        Deletes a filter.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-delete-filter.html>`_

        :arg filter_id: The ID of the filter to delete
        """
        if filter_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'filter_id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "filters", filter_id),
            params=params,
            headers=headers,
        )

    @query_params("allow_no_forecasts", "timeout")
    def delete_forecast(self, job_id, forecast_id=None, params=None, headers=None):
        """
        Deletes forecasts from a machine learning job.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-delete-forecast.html>`_

        :arg job_id: The ID of the job from which to delete forecasts
        :arg forecast_id: The ID of the forecast to delete, can be comma
            delimited list. Leaving blank implies `_all`
        :arg allow_no_forecasts: Whether to ignore if `_all` matches no
            forecasts
        :arg timeout: Controls the time to wait until the forecast(s)
            are deleted. Default to 30 seconds
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "anomaly_detectors", job_id, "_forecast", forecast_id),
            params=params,
            headers=headers,
        )

    @query_params("force", "wait_for_completion")
    def delete_job(self, job_id, params=None, headers=None):
        """
        Deletes an existing anomaly detection job.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-delete-job.html>`_

        :arg job_id: The ID of the job to delete
        :arg force: True if the job should be forcefully deleted
        :arg wait_for_completion: Should this request wait until the
            operation has completed before returning  Default: True
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "anomaly_detectors", job_id),
            params=params,
            headers=headers,
        )

    @query_params()
    def delete_model_snapshot(self, job_id, snapshot_id, params=None, headers=None):
        """
        Deletes an existing model snapshot.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-delete-snapshot.html>`_

        :arg job_id: The ID of the job to fetch
        :arg snapshot_id: The ID of the snapshot to delete
        """
        for param in (job_id, snapshot_id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "DELETE",
            _make_path(
                "_ml", "anomaly_detectors", job_id, "model_snapshots", snapshot_id
            ),
            params=params,
            headers=headers,
        )

    @query_params(
        "charset",
        "column_names",
        "delimiter",
        "explain",
        "format",
        "grok_pattern",
        "has_header_row",
        "line_merge_size_limit",
        "lines_to_sample",
        "quote",
        "should_trim_fields",
        "timeout",
        "timestamp_field",
        "timestamp_format",
    )
    def find_file_structure(self, body, params=None, headers=None):
        """
        Finds the structure of a text file. The text file must contain data that is
        suitable to be ingested into Elasticsearch.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-find-file-structure.html>`_

        :arg body: The contents of the file to be analyzed
        :arg charset: Optional parameter to specify the character set of
            the file
        :arg column_names: Optional parameter containing a comma
            separated list of the column names for a delimited file
        :arg delimiter: Optional parameter to specify the delimiter
            character for a delimited file - must be a single character
        :arg explain: Whether to include a commentary on how the
            structure was derived
        :arg format: Optional parameter to specify the high level file
            format  Valid choices: ndjson, xml, delimited, semi_structured_text
        :arg grok_pattern: Optional parameter to specify the Grok
            pattern that should be used to extract fields from messages in a semi-
            structured text file
        :arg has_header_row: Optional parameter to specify whether a
            delimited file includes the column names in its first row
        :arg line_merge_size_limit: Maximum number of characters
            permitted in a single message when lines are merged to create messages.
            Default: 10000
        :arg lines_to_sample: How many lines of the file should be
            included in the analysis  Default: 1000
        :arg quote: Optional parameter to specify the quote character
            for a delimited file - must be a single character
        :arg should_trim_fields: Optional parameter to specify whether
            the values between delimiters in a delimited file should have whitespace
            trimmed from them
        :arg timeout: Timeout after which the analysis will be aborted
            Default: 25s
        :arg timestamp_field: Optional parameter to specify the
            timestamp field in the file
        :arg timestamp_format: Optional parameter to specify the
            timestamp format in the file - may be either a Joda or Java time format
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return self.transport.perform_request(
            "POST",
            "/_ml/find_file_structure",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("advance_time", "calc_interim", "end", "skip_time", "start")
    def flush_job(self, job_id, body=None, params=None, headers=None):
        """
        Forces any buffered data to be processed by the job.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-flush-job.html>`_

        :arg job_id: The name of the job to flush
        :arg body: Flush parameters
        :arg advance_time: Advances time to the given value generating
            results and updating the model for the advanced interval
        :arg calc_interim: Calculates interim results for the most
            recent bucket or all buckets within the latency period
        :arg end: When used in conjunction with calc_interim, specifies
            the range of buckets on which to calculate interim results
        :arg skip_time: Skips time to the given value without generating
            results or updating the model for the skipped interval
        :arg start: When used in conjunction with calc_interim,
            specifies the range of buckets on which to calculate interim results
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_flush"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("duration", "expires_in", "max_model_memory")
    def forecast(self, job_id, params=None, headers=None):
        """
        Predicts the future behavior of a time series by using its historical behavior.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-forecast.html>`_

        :arg job_id: The ID of the job to forecast for
        :arg duration: The duration of the forecast
        :arg expires_in: The time interval after which the forecast
            expires. Expired forecasts will be deleted at the first opportunity.
        :arg max_model_memory: The max memory able to be used by the
            forecast. Default is 20mb.
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_forecast"),
            params=params,
            headers=headers,
        )

    @query_params(
        "anomaly_score",
        "desc",
        "end",
        "exclude_interim",
        "expand",
        "from_",
        "size",
        "sort",
        "start",
    )
    def get_buckets(self, job_id, body=None, timestamp=None, params=None, headers=None):
        """
        Retrieves anomaly detection job results for one or more buckets.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-bucket.html>`_

        :arg job_id: ID of the job to get bucket results from
        :arg body: Bucket selection details if not provided in URI
        :arg timestamp: The timestamp of the desired single bucket
            result
        :arg anomaly_score: Filter for the most anomalous buckets
        :arg desc: Set the sort direction
        :arg end: End time filter for buckets
        :arg exclude_interim: Exclude interim results
        :arg expand: Include anomaly records
        :arg from_: skips a number of buckets
        :arg size: specifies a max number of buckets to get
        :arg sort: Sort buckets by a particular field
        :arg start: Start time filter for buckets
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "POST",
            _make_path(
                "_ml", "anomaly_detectors", job_id, "results", "buckets", timestamp
            ),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("end", "from_", "job_id", "size", "start")
    def get_calendar_events(self, calendar_id, params=None, headers=None):
        """
        Retrieves information about the scheduled events in calendars.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-calendar-event.html>`_

        :arg calendar_id: The ID of the calendar containing the events
        :arg end: Get events before this time
        :arg from_: Skips a number of events
        :arg job_id: Get events for the job. When this option is used
            calendar_id must be '_all'
        :arg size: Specifies a max number of events to get
        :arg start: Get events after this time
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        if calendar_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'calendar_id'."
            )

        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "calendars", calendar_id, "events"),
            params=params,
            headers=headers,
        )

    @query_params("from_", "size")
    def get_calendars(self, body=None, calendar_id=None, params=None, headers=None):
        """
        Retrieves configuration information for calendars.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-calendar.html>`_

        :arg body: The from and size parameters optionally sent in the
            body
        :arg calendar_id: The ID of the calendar to fetch
        :arg from_: skips a number of calendars
        :arg size: specifies a max number of calendars to get
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "calendars", calendar_id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("from_", "partition_field_value", "size")
    def get_categories(
        self, job_id, body=None, category_id=None, params=None, headers=None
    ):
        """
        Retrieves anomaly detection job results for one or more categories.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-category.html>`_

        :arg job_id: The name of the job
        :arg body: Category selection details if not provided in URI
        :arg category_id: The identifier of the category definition of
            interest
        :arg from_: skips a number of categories
        :arg partition_field_value: Specifies the partition to retrieve
            categories for. This is optional, and should never be used for jobs
            where per-partition categorization is disabled.
        :arg size: specifies a max number of categories to get
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "POST",
            _make_path(
                "_ml", "anomaly_detectors", job_id, "results", "categories", category_id
            ),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("allow_no_datafeeds")
    def get_datafeed_stats(self, datafeed_id=None, params=None, headers=None):
        """
        Retrieves usage information for datafeeds.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-datafeed-stats.html>`_

        :arg datafeed_id: The ID of the datafeeds stats to fetch
        :arg allow_no_datafeeds: Whether to ignore if a wildcard
            expression matches no datafeeds. (This includes `_all` string or when no
            datafeeds have been specified)
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "datafeeds", datafeed_id, "_stats"),
            params=params,
            headers=headers,
        )

    @query_params("allow_no_datafeeds")
    def get_datafeeds(self, datafeed_id=None, params=None, headers=None):
        """
        Retrieves configuration information for datafeeds.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeeds to fetch
        :arg allow_no_datafeeds: Whether to ignore if a wildcard
            expression matches no datafeeds. (This includes `_all` string or when no
            datafeeds have been specified)
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "datafeeds", datafeed_id),
            params=params,
            headers=headers,
        )

    @query_params("from_", "size")
    def get_filters(self, filter_id=None, params=None, headers=None):
        """
        Retrieves filters.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-filter.html>`_

        :arg filter_id: The ID of the filter to fetch
        :arg from_: skips a number of filters
        :arg size: specifies a max number of filters to get
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "filters", filter_id),
            params=params,
            headers=headers,
        )

    @query_params(
        "desc",
        "end",
        "exclude_interim",
        "from_",
        "influencer_score",
        "size",
        "sort",
        "start",
    )
    def get_influencers(self, job_id, body=None, params=None, headers=None):
        """
        Retrieves anomaly detection job results for one or more influencers.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-influencer.html>`_

        :arg job_id: Identifier for the anomaly detection job
        :arg body: Influencer selection criteria
        :arg desc: whether the results should be sorted in decending
            order
        :arg end: end timestamp for the requested influencers
        :arg exclude_interim: Exclude interim results
        :arg from_: skips a number of influencers
        :arg influencer_score: influencer score threshold for the
            requested influencers
        :arg size: specifies a max number of influencers to get
        :arg sort: sort field for the requested influencers
        :arg start: start timestamp for the requested influencers
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "results", "influencers"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("allow_no_jobs")
    def get_job_stats(self, job_id=None, params=None, headers=None):
        """
        Retrieves usage information for anomaly detection jobs.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-job-stats.html>`_

        :arg job_id: The ID of the jobs stats to fetch
        :arg allow_no_jobs: Whether to ignore if a wildcard expression
            matches no jobs. (This includes `_all` string or when no jobs have been
            specified)
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "anomaly_detectors", job_id, "_stats"),
            params=params,
            headers=headers,
        )

    @query_params("allow_no_jobs")
    def get_jobs(self, job_id=None, params=None, headers=None):
        """
        Retrieves configuration information for anomaly detection jobs.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-job.html>`_

        :arg job_id: The ID of the jobs to fetch
        :arg allow_no_jobs: Whether to ignore if a wildcard expression
            matches no jobs. (This includes `_all` string or when no jobs have been
            specified)
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "anomaly_detectors", job_id),
            params=params,
            headers=headers,
        )

    @query_params("desc", "end", "from_", "size", "sort", "start")
    def get_model_snapshots(
        self, job_id, body=None, snapshot_id=None, params=None, headers=None
    ):
        """
        Retrieves information about model snapshots.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-snapshot.html>`_

        :arg job_id: The ID of the job to fetch
        :arg body: Model snapshot selection criteria
        :arg snapshot_id: The ID of the snapshot to fetch
        :arg desc: True if the results should be sorted in descending
            order
        :arg end: The filter 'end' query parameter
        :arg from_: Skips a number of documents
        :arg size: The default number of documents returned in queries
            as a string.
        :arg sort: Name of the field to sort on
        :arg start: The filter 'start' query parameter
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "POST",
            _make_path(
                "_ml", "anomaly_detectors", job_id, "model_snapshots", snapshot_id
            ),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "allow_no_jobs",
        "bucket_span",
        "end",
        "exclude_interim",
        "overall_score",
        "start",
        "top_n",
    )
    def get_overall_buckets(self, job_id, body=None, params=None, headers=None):
        """
        Retrieves overall bucket results that summarize the bucket results of multiple
        anomaly detection jobs.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-overall-buckets.html>`_

        :arg job_id: The job IDs for which to calculate overall bucket
            results
        :arg body: Overall bucket selection details if not provided in
            URI
        :arg allow_no_jobs: Whether to ignore if a wildcard expression
            matches no jobs. (This includes `_all` string or when no jobs have been
            specified)
        :arg bucket_span: The span of the overall buckets. Defaults to
            the longest job bucket_span
        :arg end: Returns overall buckets with timestamps earlier than
            this time
        :arg exclude_interim: If true overall buckets that include
            interim buckets will be excluded
        :arg overall_score: Returns overall buckets with overall scores
            higher than this value
        :arg start: Returns overall buckets with timestamps after this
            time
        :arg top_n: The number of top job bucket scores to be used in
            the overall_score calculation
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "POST",
            _make_path(
                "_ml", "anomaly_detectors", job_id, "results", "overall_buckets"
            ),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "desc",
        "end",
        "exclude_interim",
        "from_",
        "record_score",
        "size",
        "sort",
        "start",
    )
    def get_records(self, job_id, body=None, params=None, headers=None):
        """
        Retrieves anomaly records for an anomaly detection job.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-get-record.html>`_

        :arg job_id: The ID of the job
        :arg body: Record selection criteria
        :arg desc: Set the sort direction
        :arg end: End time filter for records
        :arg exclude_interim: Exclude interim results
        :arg from_: skips a number of records
        :arg record_score: Returns records with anomaly scores greater
            or equal than this value
        :arg size: specifies a max number of records to get
        :arg sort: Sort records by a particular field
        :arg start: Start time filter for records
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "results", "records"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def info(self, params=None, headers=None):
        """
        Returns defaults and limits used by machine learning.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/get-ml-info.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_ml/info", params=params, headers=headers
        )

    @query_params()
    def open_job(self, job_id, params=None, headers=None):
        """
        Opens one or more anomaly detection jobs.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-open-job.html>`_

        :arg job_id: The ID of the job to open
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_open"),
            params=params,
            headers=headers,
        )

    @query_params()
    def post_calendar_events(self, calendar_id, body, params=None, headers=None):
        """
        Posts scheduled events in a calendar.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-post-calendar-event.html>`_

        :arg calendar_id: The ID of the calendar to modify
        :arg body: A list of events
        """
        for param in (calendar_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "calendars", calendar_id, "events"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("reset_end", "reset_start")
    def post_data(self, job_id, body, params=None, headers=None):
        """
        Sends data to an anomaly detection job for analysis.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-post-data.html>`_

        :arg job_id: The name of the job receiving the data
        :arg body: The data to process
        :arg reset_end: Optional parameter to specify the end of the
            bucket resetting range
        :arg reset_start: Optional parameter to specify the start of the
            bucket resetting range
        """
        for param in (job_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        body = _bulk_body(self.transport.serializer, body)
        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_data"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def preview_datafeed(self, datafeed_id, params=None, headers=None):
        """
        Previews a datafeed.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-preview-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to preview
        """
        if datafeed_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'datafeed_id'."
            )

        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "datafeeds", datafeed_id, "_preview"),
            params=params,
            headers=headers,
        )

    @query_params()
    def put_calendar(self, calendar_id, body=None, params=None, headers=None):
        """
        Instantiates a calendar.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-put-calendar.html>`_

        :arg calendar_id: The ID of the calendar to create
        :arg body: The calendar details
        """
        if calendar_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'calendar_id'."
            )

        return self.transport.perform_request(
            "PUT",
            _make_path("_ml", "calendars", calendar_id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def put_calendar_job(self, calendar_id, job_id, params=None, headers=None):
        """
        Adds an anomaly detection job to a calendar.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-put-calendar-job.html>`_

        :arg calendar_id: The ID of the calendar to modify
        :arg job_id: The ID of the job to add to the calendar
        """
        for param in (calendar_id, job_id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_ml", "calendars", calendar_id, "jobs", job_id),
            params=params,
            headers=headers,
        )

    @query_params(
        "allow_no_indices", "expand_wildcards", "ignore_throttled", "ignore_unavailable"
    )
    def put_datafeed(self, datafeed_id, body, params=None, headers=None):
        """
        Instantiates a datafeed.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-put-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to create
        :arg body: The datafeed config
        :arg allow_no_indices: Ignore if the source indices expressions
            resolves to no concrete indices (default: true)
        :arg expand_wildcards: Whether source index expressions should
            get expanded to open or closed indices (default: open)  Valid choices:
            open, closed, hidden, none, all
        :arg ignore_throttled: Ignore indices that are marked as
            throttled (default: true)
        :arg ignore_unavailable: Ignore unavailable indexes (default:
            false)
        """
        for param in (datafeed_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_ml", "datafeeds", datafeed_id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def put_filter(self, filter_id, body, params=None, headers=None):
        """
        Instantiates a filter.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-put-filter.html>`_

        :arg filter_id: The ID of the filter to create
        :arg body: The filter details
        """
        for param in (filter_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_ml", "filters", filter_id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def put_job(self, job_id, body, params=None, headers=None):
        """
        Instantiates an anomaly detection job.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-put-job.html>`_

        :arg job_id: The ID of the job to create
        :arg body: The job
        """
        for param in (job_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_ml", "anomaly_detectors", job_id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("delete_intervening_results")
    def revert_model_snapshot(
        self, job_id, snapshot_id, body=None, params=None, headers=None
    ):
        """
        Reverts to a specific snapshot.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-revert-snapshot.html>`_

        :arg job_id: The ID of the job to fetch
        :arg snapshot_id: The ID of the snapshot to revert to
        :arg body: Reversion options
        :arg delete_intervening_results: Should we reset the results
            back to the time of the snapshot?
        """
        for param in (job_id, snapshot_id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path(
                "_ml",
                "anomaly_detectors",
                job_id,
                "model_snapshots",
                snapshot_id,
                "_revert",
            ),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("enabled", "timeout")
    def set_upgrade_mode(self, params=None, headers=None):
        """
        Sets a cluster wide upgrade_mode setting that prepares machine learning indices
        for an upgrade.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-set-upgrade-mode.html>`_

        :arg enabled: Whether to enable upgrade_mode ML setting or not.
            Defaults to false.
        :arg timeout: Controls the time to wait before action times out.
            Defaults to 30 seconds
        """
        return self.transport.perform_request(
            "POST", "/_ml/set_upgrade_mode", params=params, headers=headers
        )

    @query_params("end", "start", "timeout")
    def start_datafeed(self, datafeed_id, body=None, params=None, headers=None):
        """
        Starts one or more datafeeds.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-start-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to start
        :arg body: The start datafeed parameters
        :arg end: The end time when the datafeed should stop. When not
            set, the datafeed continues in real time
        :arg start: The start time from where the datafeed should begin
        :arg timeout: Controls the time to wait until a datafeed has
            started. Default to 20 seconds
        """
        if datafeed_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'datafeed_id'."
            )

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "datafeeds", datafeed_id, "_start"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("allow_no_datafeeds", "force", "timeout")
    def stop_datafeed(self, datafeed_id, params=None, headers=None):
        """
        Stops one or more datafeeds.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-stop-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to stop
        :arg allow_no_datafeeds: Whether to ignore if a wildcard
            expression matches no datafeeds. (This includes `_all` string or when no
            datafeeds have been specified)
        :arg force: True if the datafeed should be forcefully stopped.
        :arg timeout: Controls the time to wait until a datafeed has
            stopped. Default to 20 seconds
        """
        if datafeed_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'datafeed_id'."
            )

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "datafeeds", datafeed_id, "_stop"),
            params=params,
            headers=headers,
        )

    @query_params(
        "allow_no_indices", "expand_wildcards", "ignore_throttled", "ignore_unavailable"
    )
    def update_datafeed(self, datafeed_id, body, params=None, headers=None):
        """
        Updates certain properties of a datafeed.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-update-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to update
        :arg body: The datafeed update settings
        :arg allow_no_indices: Ignore if the source indices expressions
            resolves to no concrete indices (default: true)
        :arg expand_wildcards: Whether source index expressions should
            get expanded to open or closed indices (default: open)  Valid choices:
            open, closed, hidden, none, all
        :arg ignore_throttled: Ignore indices that are marked as
            throttled (default: true)
        :arg ignore_unavailable: Ignore unavailable indexes (default:
            false)
        """
        for param in (datafeed_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "datafeeds", datafeed_id, "_update"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def update_filter(self, filter_id, body, params=None, headers=None):
        """
        Updates the description of a filter, adds items, or removes items.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-update-filter.html>`_

        :arg filter_id: The ID of the filter to update
        :arg body: The filter update
        """
        for param in (filter_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "filters", filter_id, "_update"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def update_job(self, job_id, body, params=None, headers=None):
        """
        Updates certain properties of an anomaly detection job.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-update-job.html>`_

        :arg job_id: The ID of the job to create
        :arg body: The job update settings
        """
        for param in (job_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_update"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def update_model_snapshot(
        self, job_id, snapshot_id, body, params=None, headers=None
    ):
        """
        Updates certain properties of a snapshot.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-update-snapshot.html>`_

        :arg job_id: The ID of the job to fetch
        :arg snapshot_id: The ID of the snapshot to update
        :arg body: The model snapshot properties to update
        """
        for param in (job_id, snapshot_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path(
                "_ml",
                "anomaly_detectors",
                job_id,
                "model_snapshots",
                snapshot_id,
                "_update",
            ),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def validate(self, body, params=None, headers=None):
        """
        Validates an anomaly detection job.
        `<https://www.elastic.co/guide/en/machine-learning/current/ml-jobs.html>`_

        :arg body: The job config
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST",
            "/_ml/anomaly_detectors/_validate",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def validate_detector(self, body, params=None, headers=None):
        """
        Validates an anomaly detection detector.
        `<https://www.elastic.co/guide/en/machine-learning/current/ml-jobs.html>`_

        :arg body: The detector
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST",
            "/_ml/anomaly_detectors/_validate/detector",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("force", "timeout")
    def delete_data_frame_analytics(self, id, params=None, headers=None):
        """
        Deletes an existing data frame analytics job.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/delete-dfanalytics.html>`_

        :arg id: The ID of the data frame analytics to delete
        :arg force: True if the job should be forcefully deleted
        :arg timeout: Controls the time to wait until a job is deleted.
            Defaults to 1 minute
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "data_frame", "analytics", id),
            params=params,
            headers=headers,
        )

    @query_params()
    def evaluate_data_frame(self, body, params=None, headers=None):
        """
        Evaluates the data frame analytics for an annotated index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/evaluate-dfanalytics.html>`_

        :arg body: The evaluation definition
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST",
            "/_ml/data_frame/_evaluate",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("allow_no_match", "from_", "size")
    def get_data_frame_analytics(self, id=None, params=None, headers=None):
        """
        Retrieves configuration information for data frame analytics jobs.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/get-dfanalytics.html>`_

        :arg id: The ID of the data frame analytics to fetch
        :arg allow_no_match: Whether to ignore if a wildcard expression
            matches no data frame analytics. (This includes `_all` string or when no
            data frame analytics have been specified)  Default: True
        :arg from_: skips a number of analytics
        :arg size: specifies a max number of analytics to get  Default:
            100
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "data_frame", "analytics", id),
            params=params,
            headers=headers,
        )

    @query_params("allow_no_match", "from_", "size")
    def get_data_frame_analytics_stats(self, id=None, params=None, headers=None):
        """
        Retrieves usage information for data frame analytics jobs.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/get-dfanalytics-stats.html>`_

        :arg id: The ID of the data frame analytics stats to fetch
        :arg allow_no_match: Whether to ignore if a wildcard expression
            matches no data frame analytics. (This includes `_all` string or when no
            data frame analytics have been specified)  Default: True
        :arg from_: skips a number of analytics
        :arg size: specifies a max number of analytics to get  Default:
            100
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "data_frame", "analytics", id, "_stats"),
            params=params,
            headers=headers,
        )

    @query_params()
    def put_data_frame_analytics(self, id, body, params=None, headers=None):
        """
        Instantiates a data frame analytics job.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/put-dfanalytics.html>`_

        :arg id: The ID of the data frame analytics to create
        :arg body: The data frame analytics configuration
        """
        for param in (id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_ml", "data_frame", "analytics", id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("timeout")
    def start_data_frame_analytics(self, id, body=None, params=None, headers=None):
        """
        Starts a data frame analytics job.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/start-dfanalytics.html>`_

        :arg id: The ID of the data frame analytics to start
        :arg body: The start data frame analytics parameters
        :arg timeout: Controls the time to wait until the task has
            started. Defaults to 20 seconds
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "data_frame", "analytics", id, "_start"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("allow_no_match", "force", "timeout")
    def stop_data_frame_analytics(self, id, body=None, params=None, headers=None):
        """
        Stops one or more data frame analytics jobs.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/stop-dfanalytics.html>`_

        :arg id: The ID of the data frame analytics to stop
        :arg body: The stop data frame analytics parameters
        :arg allow_no_match: Whether to ignore if a wildcard expression
            matches no data frame analytics. (This includes `_all` string or when no
            data frame analytics have been specified)
        :arg force: True if the data frame analytics should be
            forcefully stopped
        :arg timeout: Controls the time to wait until the task has
            stopped. Defaults to 20 seconds
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "data_frame", "analytics", id, "_stop"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def delete_trained_model(self, model_id, params=None, headers=None):
        """
        Deletes an existing trained inference model that is currently not referenced by
        an ingest pipeline.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/delete-inference.html>`_

        :arg model_id: The ID of the trained model to delete
        """
        if model_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'model_id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "inference", model_id),
            params=params,
            headers=headers,
        )

    @query_params()
    def explain_data_frame_analytics(
        self, body=None, id=None, params=None, headers=None
    ):
        """
        Explains a data frame analytics config.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/explain-dfanalytics.html>`_

        :arg body: The data frame analytics config to explain
        :arg id: The ID of the data frame analytics to explain
        """
        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "data_frame", "analytics", id, "_explain"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "allow_no_match",
        "decompress_definition",
        "for_export",
        "from_",
        "include_model_definition",
        "size",
        "tags",
    )
    def get_trained_models(self, model_id=None, params=None, headers=None):
        """
        Retrieves configuration information for a trained inference model.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/get-inference.html>`_

        :arg model_id: The ID of the trained models to fetch
        :arg allow_no_match: Whether to ignore if a wildcard expression
            matches no trained models. (This includes `_all` string or when no
            trained models have been specified)  Default: True
        :arg decompress_definition: Should the model definition be
            decompressed into valid JSON or returned in a custom compressed format.
            Defaults to true.  Default: True
        :arg for_export: Omits fields that are illegal to set on model
            PUT
        :arg from_: skips a number of trained models
        :arg include_model_definition: Should the full model definition
            be included in the results. These definitions can be large. So be
            cautious when including them. Defaults to false.
        :arg size: specifies a max number of trained models to get
            Default: 100
        :arg tags: A comma-separated list of tags that the model must
            have.
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "inference", model_id),
            params=params,
            headers=headers,
        )

    @query_params("allow_no_match", "from_", "size")
    def get_trained_models_stats(self, model_id=None, params=None, headers=None):
        """
        Retrieves usage information for trained inference models.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/get-inference-stats.html>`_

        :arg model_id: The ID of the trained models stats to fetch
        :arg allow_no_match: Whether to ignore if a wildcard expression
            matches no trained models. (This includes `_all` string or when no
            trained models have been specified)  Default: True
        :arg from_: skips a number of trained models
        :arg size: specifies a max number of trained models to get
            Default: 100
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "inference", model_id, "_stats"),
            params=params,
            headers=headers,
        )

    @query_params()
    def put_trained_model(self, model_id, body, params=None, headers=None):
        """
        Creates an inference trained model.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/put-inference.html>`_

        :arg model_id: The ID of the trained models to store
        :arg body: The trained model configuration
        """
        for param in (model_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_ml", "inference", model_id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def estimate_model_memory(self, body, params=None, headers=None):
        """
        Estimates the model memory
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/ml-apis.html>`_

        :arg body: The analysis config, plus cardinality estimates for
            fields it references
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST",
            "/_ml/anomaly_detectors/_estimate_model_memory",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def update_data_frame_analytics(self, id, body, params=None, headers=None):
        """
        Updates certain properties of a data frame analytics job.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.9/update-dfanalytics.html>`_

        :arg id: The ID of the data frame analytics to update
        :arg body: The data frame analytics settings to update
        """
        for param in (id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "data_frame", "analytics", id, "_update"),
            params=params,
            headers=headers,
            body=body,
        )
