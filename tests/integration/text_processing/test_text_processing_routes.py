class TestText_ProcessingRoutes:
    def test_new_line_page(
        self,
        integration_client,
    ):
        response = integration_client.get("/txt/replace")

        assert response.status_code == 200, (
            f"テスト失敗：期待値=200、実際値={response.status_code}"
        )

    def test_get_regex_page(
        self,
        integration_client,
    ):
        response = integration_client.get("/txt/regex")

        assert response.status_code == 200, (
            f"テスト失敗：期待値=200、実際値={response.status_code}"
        )
