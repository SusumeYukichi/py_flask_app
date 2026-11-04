class TestCreateAppRoutes:
    def test_404_page(
        self,
        integration_client,
    ):
        response = integration_client.get("/this-page-does-not-exist")

        assert response.status_code == 404, (
            f"テスト失敗：期待値=404、実際値={response.status_code}"
        )
