from pathlib import Path

from bs4 import BeautifulSoup


class TestMainViews:
    def test_read_txt_views(
        self,
        integration_client,
        test_app,
    ):
        response = integration_client.get("/input")

        assert response.status_code == 200

        file_path = Path(test_app.root_path) / "text_files" / "input" / "input.txt"

        assert file_path.is_file()

        assert file_path.name == "input.txt"

        assert file_path.parent.name == "input"

        assert file_path.parent.parent.name == "text_files"

        input_text = file_path.read_text(encoding="utf-8")

        assert input_text != ""

        assert isinstance(
            input_text,
            str,
        )

    def test_read_html_views(
        self,
        integration_client,
        test_app,
    ):

        file_path = Path(test_app.root_path) / "text_files" / "input" / "input.txt"

        input_txt = file_path.read_text(encoding="utf-8")

        response = integration_client.get("input")

        assert response.status_code == 200

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        input_element = soup.select_one(".bs4-input-text")

        assert input_element is not None

        assert input_txt.strip() == input_element.get_text().strip()

    def test_check_html_views(
        self,
        integration_client,
    ):
        response = integration_client.get("/input")

        html = response.get_data(as_text=True)
        assert response.status_code == 200

        # 先頭文字
        assert "ネットワーク" in html
        # 中間付近
        assert "Wi-Fi" in html
        # 末尾付近
        assert "配信します。" in html

    def test_lists_views(
        self,
        test_app,
    ):
        from app.extensions import db
        from app.models import User

        client = test_app.test_client()

        with test_app.app_context():
            db.create_all()
            user = User(
                username="test",
                password="test",
            )

            db.session.add(user)
            db.session.commit()
            user_id = user.id

        client = test_app.test_client()

        with client.session_transaction() as session:
            session["_user_id"] = str(user_id)
            session["_fresh"] = True

        response = client.get("/lists")

        assert response.status_code == 200, (
            f"テスト失敗：期待値=200、実際値={response.status_code}"
        )
