class TestMemoRoutes:
    def test_get_new_index(
        self,
        integration_client,
    ):
        response = integration_client.get("/memo/new")

        assert response.status_code == 302, (
            f"テスト失敗：期待値=302、実際値={response.status_code}"
        )
