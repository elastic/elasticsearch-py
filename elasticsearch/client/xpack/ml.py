from ..utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class MlClient(NamespacedClient):
    @query_params("allow_no_jobs", "force", "timeout")
    def close_job(self, job_id, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-close-job.html>`_

        :arg job_id: The name of the job to close
        :arg body: The URL params optionally sent in the body
        :arg allow_no_jobs: Whether to ignore if a wildcard expression matches
            no jobs. (This includes `_all` string or when no jobs have been
            specified)
        :arg force: True if the job should be forcefully closed
        :arg timeout: Controls the time to wait until a job has closed. Default
            to 30 minutes
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_close"),
            params=params,
            body=body,
        )

    @query_params()
    def delete_calendar(self, calendar_id, params=None):
        """
        `<>`_

        :arg calendar_id: The ID of the calendar to delete
        """
        if calendar_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'calendar_id'."
            )
        return self.transport.perform_request(
            "DELETE", _make_path("_ml", "calendars", calendar_id), params=params
        )

    @query_params()
    def delete_calendar_event(self, calendar_id, event_id, params=None):
        """
        `<>`_

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
        )

    @query_params()
    def delete_calendar_job(self, calendar_id, job_id, params=None):
        """
        `<>`_

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
        )

    @query_params("force")
    def delete_datafeed(self, datafeed_id, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-delete-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to delete
        :arg force: True if the datafeed should be forcefully deleted
        """
        if datafeed_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'datafeed_id'."
            )
        return self.transport.perform_request(
            "DELETE", _make_path("_ml", "datafeeds", datafeed_id), params=params
        )

    @query_params()
    def delete_expired_data(self, params=None):
        """
        `<>`_
        """
        return self.transport.perform_request(
            "DELETE", "/_ml/_delete_expired_data", params=params
        )

    @query_params()
    def delete_filter(self, filter_id, params=None):
        """
        `<>`_

        :arg filter_id: The ID of the filter to delete
        """
        if filter_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'filter_id'.")
        return self.transport.perform_request(
            "DELETE", _make_path("_ml", "filters", filter_id), params=params
        )

    @query_params("allow_no_forecasts", "timeout")
    def delete_forecast(self, job_id, forecast_id=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-delete-forecast.html>`_

        :arg job_id: The ID of the job from which to delete forecasts
        :arg forecast_id: The ID of the forecast to delete, can be comma
            delimited list. Leaving blank implies `_all`
        :arg allow_no_forecasts: Whether to ignore if `_all` matches no
            forecasts
        :arg timeout: Controls the time to wait until the forecast(s) are
            deleted. Default to 30 seconds
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "DELETE",
            _make_path("_ml", "anomaly_detectors", job_id, "_forecast", forecast_id),
            params=params,
        )

    @query_params("force", "wait_for_completion")
    def delete_job(self, job_id, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-delete-job.html>`_

        :arg job_id: The ID of the job to delete
        :arg force: True if the job should be forcefully deleted, default False
        :arg wait_for_completion: Should this request wait until the operation
            has completed before returning, default True
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "DELETE", _make_path("_ml", "anomaly_detectors", job_id), params=params
        )

    @query_params()
    def delete_model_snapshot(self, job_id, snapshot_id, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-delete-snapshot.html>`_

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
        )

    @query_params(
        "charset",
        "column_names",
        "delimiter",
        "explain",
        "format",
        "grok_pattern",
        "has_header_row",
        "lines_to_sample",
        "quote",
        "should_trim_fields",
        "timeout",
        "timestamp_field",
        "timestamp_format",
    )
    def find_file_structure(self, body, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-file-structure.html>`_

        :arg body: The contents of the file to be analyzed
        :arg charset: Optional parameter to specify the character set of the
            file
        :arg column_names: Optional parameter containing a comma separated list
            of the column names for a delimited file
        :arg delimiter: Optional parameter to specify the delimiter character
            for a delimited file - must be a single character
        :arg explain: Whether to include a commentary on how the structure was
            derived, default False
        :arg format: Optional parameter to specify the high level file format,
            valid choices are: 'ndjson', 'xml', 'delimited',
            'semi_structured_text'
        :arg grok_pattern: Optional parameter to specify the Grok pattern that
            should be used to extract fields from messages in a semi-structured
            text file
        :arg has_header_row: Optional parameter to specify whether a delimited
            file includes the column names in its first row
        :arg lines_to_sample: How many lines of the file should be included in
            the analysis, default 1000
        :arg quote: Optional parameter to specify the quote character for a
            delimited file - must be a single character
        :arg should_trim_fields: Optional parameter to specify whether the
            values between delimiters in a delimited file should have whitespace
            trimmed from them
        :arg timeout: Timeout after which the analysis will be aborted, default
            '25s'
        :arg timestamp_field: Optional parameter to specify the timestamp field
            in the file
        :arg timestamp_format: Optional parameter to specify the timestamp
            format in the file - may be either a Joda or Java time format
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "POST",
            "/_ml/find_file_structure",
            params=params,
            body=self.client._bulk_body(body),
        )

    @query_params("advance_time", "calc_interim", "end", "skip_time", "start")
    def flush_job(self, job_id, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-flush-job.html>`_

        :arg job_id: The name of the job to flush
        :arg body: Flush parameters
        :arg advance_time: Advances time to the given value generating results
            and updating the model for the advanced interval
        :arg calc_interim: Calculates interim results for the most recent bucket
            or all buckets within the latency period
        :arg end: When used in conjunction with calc_interim, specifies the
            range of buckets on which to calculate interim results
        :arg skip_time: Skips time to the given value without generating results
            or updating the model for the skipped interval
        :arg start: When used in conjunction with calc_interim, specifies the
            range of buckets on which to calculate interim results
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_flush"),
            params=params,
            body=body,
        )

    @query_params("duration", "expires_in")
    def forecast(self, job_id, params=None):
        """
        `<>`_

        :arg job_id: The ID of the job to forecast for
        :arg duration: The duration of the forecast
        :arg expires_in: The time interval after which the forecast expires.
            Expired forecasts will be deleted at the first opportunity.
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_forecast"),
            params=params,
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
    def get_buckets(self, job_id, timestamp=None, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-bucket.html>`_

        :arg job_id: ID of the job to get bucket results from
        :arg timestamp: The timestamp of the desired single bucket result
        :arg body: Bucket selection details if not provided in URI
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
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "GET",
            _make_path(
                "_ml", "anomaly_detectors", job_id, "results", "buckets", timestamp
            ),
            params=params,
            body=body,
        )

    @query_params("end", "from_", "job_id", "size", "start")
    def get_calendar_events(self, calendar_id, params=None):
        """
        `<>`_

        :arg calendar_id: The ID of the calendar containing the events
        :arg end: Get events before this time
        :arg from_: Skips a number of events
        :arg job_id: Get events for the job. When this option is used
            calendar_id must be '_all'
        :arg size: Specifies a max number of events to get
        :arg start: Get events after this time
        """
        if calendar_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'calendar_id'."
            )
        return self.transport.perform_request(
            "GET", _make_path("_ml", "calendars", calendar_id, "events"), params=params
        )

    @query_params("from_", "size")
    def get_calendars(self, calendar_id=None, body=None, params=None):
        """
        `<>`_

        :arg calendar_id: The ID of the calendar to fetch
        :arg body: The from and size parameters optionally sent in the body
        :arg from_: skips a number of calendars
        :arg size: specifies a max number of calendars to get
        """
        return self.transport.perform_request(
            "GET", _make_path("_ml", "calendars", calendar_id), params=params, body=body
        )

    @query_params("from_", "size")
    def get_categories(self, job_id, category_id=None, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-category.html>`_

        :arg job_id: The name of the job
        :arg category_id: The identifier of the category definition of interest
        :arg body: Category selection details if not provided in URI
        :arg from_: skips a number of categories
        :arg size: specifies a max number of categories to get
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "GET",
            _make_path(
                "_ml", "anomaly_detectors", job_id, "results", "categories", category_id
            ),
            params=params,
            body=body,
        )

    @query_params("allow_no_datafeeds")
    def get_datafeed_stats(self, datafeed_id=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-datafeed-stats.html>`_

        :arg datafeed_id: The ID of the datafeeds stats to fetch
        :arg allow_no_datafeeds: Whether to ignore if a wildcard expression
            matches no datafeeds. (This includes `_all` string or when no
            datafeeds have been specified)
        """
        return self.transport.perform_request(
            "GET", _make_path("_ml", "datafeeds", datafeed_id, "_stats"), params=params
        )

    @query_params("allow_no_datafeeds")
    def get_datafeeds(self, datafeed_id=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeeds to fetch
        :arg allow_no_datafeeds: Whether to ignore if a wildcard expression
            matches no datafeeds. (This includes `_all` string or when no
            datafeeds have been specified)
        """
        return self.transport.perform_request(
            "GET", _make_path("_ml", "datafeeds", datafeed_id), params=params
        )

    @query_params("from_", "size")
    def get_filters(self, filter_id=None, params=None):
        """
        `<>`_

        :arg filter_id: The ID of the filter to fetch
        :arg from_: skips a number of filters
        :arg size: specifies a max number of filters to get
        """
        return self.transport.perform_request(
            "GET", _make_path("_ml", "filters", filter_id), params=params
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
    def get_influencers(self, job_id, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-influencer.html>`_

        :arg job_id: None
        :arg body: Influencer selection criteria
        :arg desc: whether the results should be sorted in decending order
        :arg end: end timestamp for the requested influencers
        :arg exclude_interim: Exclude interim results
        :arg from_: skips a number of influencers
        :arg influencer_score: influencer score threshold for the requested
            influencers
        :arg size: specifies a max number of influencers to get
        :arg sort: sort field for the requested influencers
        :arg start: start timestamp for the requested influencers
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "anomaly_detectors", job_id, "results", "influencers"),
            params=params,
            body=body,
        )

    @query_params("allow_no_jobs")
    def get_job_stats(self, job_id=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-job-stats.html>`_

        :arg job_id: The ID of the jobs stats to fetch
        :arg allow_no_jobs: Whether to ignore if a wildcard expression matches
            no jobs. (This includes `_all` string or when no jobs have been
            specified)
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "anomaly_detectors", job_id, "_stats"),
            params=params,
        )

    @query_params("allow_no_jobs")
    def get_jobs(self, job_id=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-job.html>`_

        :arg job_id: The ID of the jobs to fetch
        :arg allow_no_jobs: Whether to ignore if a wildcard expression matches
            no jobs. (This includes `_all` string or when no jobs have been
            specified)
        """
        return self.transport.perform_request(
            "GET", _make_path("_ml", "anomaly_detectors", job_id), params=params
        )

    @query_params("desc", "end", "from_", "size", "sort", "start")
    def get_model_snapshots(self, job_id, snapshot_id=None, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-snapshot.html>`_

        :arg job_id: The ID of the job to fetch
        :arg snapshot_id: The ID of the snapshot to fetch
        :arg body: Model snapshot selection criteria
        :arg desc: True if the results should be sorted in descending order
        :arg end: The filter 'end' query parameter
        :arg from_: Skips a number of documents
        :arg size: The default number of documents returned in queries as a
            string.
        :arg sort: Name of the field to sort on
        :arg start: The filter 'start' query parameter
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "GET",
            _make_path(
                "_ml", "anomaly_detectors", job_id, "model_snapshots", snapshot_id
            ),
            params=params,
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
    def get_overall_buckets(self, job_id, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-overall-buckets.html>`_

        :arg job_id: The job IDs for which to calculate overall bucket results
        :arg body: Overall bucket selection details if not provided in URI
        :arg allow_no_jobs: Whether to ignore if a wildcard expression matches
            no jobs. (This includes `_all` string or when no jobs have been
            specified)
        :arg bucket_span: The span of the overall buckets. Defaults to the
            longest job bucket_span
        :arg end: Returns overall buckets with timestamps earlier than this time
        :arg exclude_interim: If true overall buckets that include interim
            buckets will be excluded
        :arg overall_score: Returns overall buckets with overall scores higher
            than this value
        :arg start: Returns overall buckets with timestamps after this time
        :arg top_n: The number of top job bucket scores to be used in the
            overall_score calculation
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "GET",
            _make_path(
                "_ml", "anomaly_detectors", job_id, "results", "overall_buckets"
            ),
            params=params,
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
    def get_records(self, job_id, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-get-record.html>`_

        :arg job_id: None
        :arg body: Record selection criteria
        :arg desc: Set the sort direction
        :arg end: End time filter for records
        :arg exclude_interim: Exclude interim results
        :arg from_: skips a number of records
        :arg record_score:
        :arg size: specifies a max number of records to get
        :arg sort: Sort records by a particular field
        :arg start: Start time filter for records
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "GET",
            _make_path("_ml", "anomaly_detectors", job_id, "results", "records"),
            params=params,
            body=body,
        )

    @query_params()
    def info(self, params=None):
        """
        `<>`_
        """
        return self.transport.perform_request("GET", "/_ml/info", params=params)

    @query_params()
    def open_job(self, job_id, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-open-job.html>`_

        :arg job_id: The ID of the job to open
        """
        if job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'job_id'.")
        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_open"),
            params=params,
        )

    @query_params()
    def post_calendar_events(self, calendar_id, body, params=None):
        """
        `<>`_

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
            body=body,
        )

    @query_params("reset_end", "reset_start")
    def post_data(self, job_id, body, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-post-data.html>`_

        :arg job_id: The name of the job receiving the data
        :arg body: The data to process
        :arg reset_end: Optional parameter to specify the end of the bucket
            resetting range
        :arg reset_start: Optional parameter to specify the start of the bucket
            resetting range
        """
        for param in (job_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "anomaly_detectors", job_id, "_data"),
            params=params,
            body=self.client._bulk_body(body),
        )

    @query_params()
    def preview_datafeed(self, datafeed_id, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-preview-datafeed.html>`_

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
        )

    @query_params()
    def put_calendar(self, calendar_id, body=None, params=None):
        """
        `<>`_

        :arg calendar_id: The ID of the calendar to create
        :arg body: The calendar details
        """
        if calendar_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'calendar_id'."
            )
        return self.transport.perform_request(
            "PUT", _make_path("_ml", "calendars", calendar_id), params=params, body=body
        )

    @query_params()
    def put_calendar_job(self, calendar_id, job_id, params=None):
        """
        `<>`_

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
        )

    @query_params()
    def put_datafeed(self, datafeed_id, body, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-put-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to create
        :arg body: The datafeed config
        """
        for param in (datafeed_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "PUT", _make_path("_ml", "datafeeds", datafeed_id), params=params, body=body
        )

    @query_params()
    def put_filter(self, filter_id, body, params=None):
        """
        `<>`_

        :arg filter_id: The ID of the filter to create
        :arg body: The filter details
        """
        for param in (filter_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "PUT", _make_path("_ml", "filters", filter_id), params=params, body=body
        )

    @query_params()
    def put_job(self, job_id, body, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-put-job.html>`_

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
            body=body,
        )

    @query_params("delete_intervening_results")
    def revert_model_snapshot(self, job_id, snapshot_id, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-revert-snapshot.html>`_

        :arg job_id: The ID of the job to fetch
        :arg snapshot_id: The ID of the snapshot to revert to
        :arg body: Reversion options
        :arg delete_intervening_results: Should we reset the results back to the
            time of the snapshot?
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
            body=body,
        )

    @query_params("enabled", "timeout")
    def set_upgrade_mode(self, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-set-upgrade-mode.html>`_

        :arg enabled: Whether to enable upgrade_mode ML setting or not. Defaults
            to false.
        :arg timeout: Controls the time to wait before action times out.
            Defaults to 30 seconds
        """
        return self.transport.perform_request(
            "POST", "/_ml/set_upgrade_mode", params=params
        )

    @query_params("end", "start", "timeout")
    def start_datafeed(self, datafeed_id, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-start-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to start
        :arg body: The start datafeed parameters
        :arg end: The end time when the datafeed should stop. When not set, the
            datafeed continues in real time
        :arg start: The start time from where the datafeed should begin
        :arg timeout: Controls the time to wait until a datafeed has started.
            Default to 20 seconds
        """
        if datafeed_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'datafeed_id'."
            )
        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "datafeeds", datafeed_id, "_start"),
            params=params,
            body=body,
        )

    @query_params("allow_no_datafeeds", "force", "timeout")
    def stop_datafeed(self, datafeed_id, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-stop-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to stop
        :arg allow_no_datafeeds: Whether to ignore if a wildcard expression
            matches no datafeeds. (This includes `_all` string or when no
            datafeeds have been specified)
        :arg force: True if the datafeed should be forcefully stopped.
        :arg timeout: Controls the time to wait until a datafeed has stopped.
            Default to 20 seconds
        """
        if datafeed_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'datafeed_id'."
            )
        return self.transport.perform_request(
            "POST", _make_path("_ml", "datafeeds", datafeed_id, "_stop"), params=params
        )

    @query_params()
    def update_datafeed(self, datafeed_id, body, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-update-datafeed.html>`_

        :arg datafeed_id: The ID of the datafeed to update
        :arg body: The datafeed update settings
        """
        for param in (datafeed_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "POST",
            _make_path("_ml", "datafeeds", datafeed_id, "_update"),
            params=params,
            body=body,
        )

    @query_params()
    def update_filter(self, filter_id, body, params=None):
        """
        `<>`_

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
            body=body,
        )

    @query_params()
    def update_job(self, job_id, body, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-update-job.html>`_

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
            body=body,
        )

    @query_params()
    def update_model_snapshot(self, job_id, snapshot_id, body, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/ml-update-snapshot.html>`_

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
            body=body,
        )

    @query_params()
    def validate(self, body, params=None):
        """
        `<>`_

        :arg body: The job config
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "POST", "/_ml/anomaly_detectors/_validate", params=params, body=body
        )

    @query_params()
    def validate_detector(self, body, params=None):
        """
        `<>`_

        :arg body: The detector
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "POST",
            "/_ml/anomaly_detectors/_validate/detector",
            params=params,
            body=body,
        )
