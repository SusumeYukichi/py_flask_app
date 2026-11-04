class TestAuthRoutes:
    def test_register_page(
        self,
        integration_client,
    ):
        response = integration_client.get("/auth/register")

        assert response.status_code == 200, (
            f"テスト失敗：期待値=200、実際値={response.status_code}"
        )

    def test_login_page(
        self,
        integration_client,
    ):
        response = integration_client.get("/auth/login")

        assert response.status_code == 200, (
            f"テスト失敗：期待値=200、実際値={response.status_code}"
        )

    def test_logout_page(
        self,
        integration_client,
    ):
        response = integration_client.get("/auth/logout")

        assert response.status_code == 302, (
            f"テスト失敗：期待値=302、実際値={response.status_code}"
        )
