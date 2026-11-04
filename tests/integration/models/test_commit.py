from datetime import date

from app.extensions import db
from app.models import Memo, User


class TestModelCommit:
    def test_users_commit(
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

            memo = Memo(
                input_date=date(
                    2026,
                    8,
                    10,
                ),
                subject="DB保存テスト",
                category="DB保存カテゴリ保存テスト",
                content="DB保存内容保存テスト",
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

            saved_memo = db.session.get(
                Memo,
                memo.id,
            )

            assert saved_memo is not None
            assert saved_memo.input_date == date(
                2026,
                8,
                10,
            )
            assert saved_memo.subject == "DB保存テスト"
            assert saved_memo.category == "DB保存カテゴリ保存テスト"
            assert saved_memo.content == "DB保存内容保存テスト"

    def test_users_update_commit(
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

            memo = Memo(
                input_date=date(
                    2026,
                    8,
                    10,
                ),
                subject="DB保存テスト",
                category="DB保存カテゴリ保存テスト",
                content="DB保存内容保存テスト",
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

            memo.subject = "更新後件名"
            memo.category = "更新後カテゴリ"
            memo.content = "更新後内容"
            db.session.commit()

            updated_memo = db.session.get(
                Memo,
                memo.id,
            )

            assert updated_memo is not None

            assert updated_memo.subject == "更新後件名"
            assert updated_memo.category == "更新後カテゴリ"
            assert updated_memo.content == "更新後内容"

            assert updated_memo.input_date == date(
                2026,
                8,
                10,
            )

            assert updated_memo.user_id == users.id

    def test_users_delate_commit(
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
            memo = Memo(
                input_date=date(
                    2026,
                    8,
                    10,
                ),
                subject="DB保存テスト",
                category="DB保存カテゴリ保存テスト",
                content="DB保存内容保存テスト",
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

            saved_memo = db.session.get(
                Memo,
                memo.id,
            )

            assert saved_memo is not None

            db.session.delete(memo)
            db.session.commit()
            deleted_memo = db.session.get(
                Memo,
                memo.id,
            )

            assert deleted_memo is None
