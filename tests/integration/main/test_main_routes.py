class TestMain_Routes:
    def test_bp_404_page(
        self,
        integration_client,
    ):
        response = integration_client.get("/not-found")

        assert response.status_code == 404

    def test_get_input_page(
        self,
        integration_client,
    ):
        response = integration_client.get("/input")

        assert response.status_code == 200, (
            f"テスト失敗：期待値=200、実際値={response.status_code}"
        )

    def test_get_lists_delete(
        self,
        integration_client,
    ):
        response = integration_client.get("/delete")

        assert response.status_code == 302, (
            f"テスト失敗：期待値=302、実際値={response.status_code}"
        )
