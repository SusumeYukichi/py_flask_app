from flask_login import current_user

from app.extensions import db
from app.models import User


class TestAuthViews:
    def test_register_views(
        self,
        test_app,
    ):
        with test_app.app_context():
            db.create_all()

        client = test_app.test_client()

        with client:
            response = client.post(
                "/auth/register",
                data={
                    "username": "test",
                    "password": "test",
                },
            )

            assert response.status_code == 302
            assert current_user.is_authenticated is True
            assert current_user.username == "test"

        with test_app.app_context():
            saved_user = db.session.execute(
                db.select(User).where(
                    User.username == "test",
                )
            ).scalar_one_or_none()

            assert saved_user is not None
            assert saved_user.check_password("test") is True

    def test_logout_views(
        self,
        test_app,
    ):
        with test_app.app_context():
            db.create_all()

        client = test_app.test_client()

        with client:
            client.post(
                "/auth/register",
                data={
                    "username": "test",
                    "password": "test123",
                },
            )

            assert current_user.is_authenticated is True

            response = client.get("/auth/logout")

            assert response.status_code == 302
            assert current_user.is_authenticated is False
