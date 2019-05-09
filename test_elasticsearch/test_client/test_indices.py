from test_elasticsearch.test_cases import ElasticsearchTestCase


class TestIndices(ElasticsearchTestCase):
    def test_create_one_index(self):
        self.client.indices.create("test-index")
        self.assert_url_called("PUT", "/test-index")

    def test_delete_multiple_indices(self):
        self.client.indices.delete(["test-index", "second.index", "third/index"])
        self.assert_url_called("DELETE", "/test-index,second.index,third%2Findex")

    def test_exists_index(self):
        self.client.indices.exists("second.index,third/index")
        self.assert_url_called("HEAD", "/second.index,third%2Findex")

    def test_passing_empty_value_for_required_param_raises_exception(self):
        self.assertRaises(ValueError, self.client.indices.exists, index=None)
        self.assertRaises(ValueError, self.client.indices.exists, index=[])
        self.assertRaises(ValueError, self.client.indices.exists, index="")
