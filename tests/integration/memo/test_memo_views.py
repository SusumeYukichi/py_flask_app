from datetime import date

from app.extensions import db
from app.models import Memo, User


class TestMemoViews:
    def test_new_index_views(
        self,
        test_app,
    ):
        with test_app.app_context():
            db.create_all()

            users = User(
                username="test",
                password="test",
            )

            db.session.add(users)
            db.session.commit()
            user_id = users.id

        client = test_app.test_client()

        with client.session_transaction() as session:
            session["_user_id"] = str(user_id)
            session["_fresh"] = True

        response = client.post(
            "/memo/new",
            data={
                "input_date": "2026-08-10",
                "subject": "新規登録テスト",
                "category": "テストカテゴリ",
                "content": "新規登録の結合テスト",
                "level_radio": "medium",
                "close_date": "2026-08-11",
                "select_category": "organize",
            },
        )

        assert response.status_code == 302

        with test_app.app_context():
            saved_memo = db.session.execute(
                db.select(Memo).where(
                    Memo.subject == "新規登録テスト",
                )
            ).scalar_one_or_none()

            assert saved_memo is not None

            assert saved_memo.input_date == date(
                2026,
                8,
                10,
            )
            assert saved_memo.subject == "新規登録テスト"
            assert saved_memo.category == "テストカテゴリ"
            assert saved_memo.content == "新規登録の結合テスト"

    def test_edit_memo_views(
        self,
        test_app,
    ):
        with test_app.app_context():
            db.create_all()

            users = User(
                username="test",
                password="test",
            )

            db.session.add(users)
            db.session.commit()
            user_id = users.id

        client = test_app.test_client()

        with client.session_transaction() as session:
            session["_user_id"] = str(user_id)
            session["_fresh"] = True

        with test_app.app_context():
            db.create_all()

            memo = Memo(
                input_date=date(
                    2026,
                    8,
                    10,
                ),
                subject="テスト",
                category="Python",
                content="編集前",
                close_date=date(
                    2026,
                    8,
                    10,
                ),
                select_category="整理",
                user_id=user_id,
            )

            assert memo.user_id == users.id

            db.session.add(memo)
            db.session.commit()
            memo_id = memo.id

            response = client.get(f"/memo/edit/{memo_id}")

            assert response.status_code == 200

    def test_delete_memo_views(
        self,
        test_app,
    ):
        with test_app.app_context():
            db.create_all()

            users = User(
                username="test",
                password="test",
            )

            db.session.add(users)
            db.session.commit()
            user_id = users.id

        client = test_app.test_client()

        with client.session_transaction() as session:
            session["_user_id"] = str(user_id)
            session["_fresh"] = True

        with test_app.app_context():
            db.create_all()

            memo = Memo(
                input_date=date(
                    2026,
                    8,
                    10,
                ),
                subject="一覧表示テスト",
                category="テストカテゴリ",
                content="一覧表示の結合テスト",
                close_date=date(
                    2026,
                    8,
                    10,
                ),
                select_category="整理",
                user_id=user_id,
            )

            db.session.add(memo)
            db.session.commit()

            assert memo.user_id == users.id

            memo_id = memo.id

        response = client.post(f"/memo/delete/{memo_id}")

        assert response.status_code == 302

        with test_app.app_context():
            deleted_memo = db.session.get(
                Memo,
                memo_id,
            )

            assert deleted_memo is None
