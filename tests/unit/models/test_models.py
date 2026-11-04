from sqlalchemy import Date, Integer, String, Text

from app.models import Memo, User


class TestModelMemo:
    def test_table(self):
        assert Memo.__tablename__ == "memo_table"

    def test_columns(self):
        table = Memo.__table__

        assert list(table.columns.keys()) == [
            "id",
            "input_date",
            "subject",
            "category",
            "content",
            "level_radio",
            "close_date",
            "select_category",
            "user_id",
        ]

    def test_id(self):
        table = Memo.__table__

        assert isinstance(
            table.c.id.type,
            Integer,
        )

        assert table.c.id.primary_key is True
        assert table.c.id.autoincrement is True
        assert table.c.id.nullable is False

    def test_input_date(self):
        table = Memo.__table__

        assert isinstance(
            table.c.input_date.type,
            Date,
        )

        assert table.c.input_date.nullable is False

    def test_subject(self):
        table = Memo.__table__

        assert isinstance(
            table.c.subject.type,
            String,
        )

        assert table.c.subject.type.length == 30
        assert table.c.subject.nullable is False

    def test_category(self):
        table = Memo.__table__

        assert isinstance(
            table.c.category.type,
            String,
        )

        assert table.c.category.type.length == 30
        assert table.c.category.nullable is False
        assert table.c.category.default.arg == "未分類"

    def test_content(self):
        table = Memo.__table__

        assert isinstance(
            table.c.content.type,
            Text,
        )

        assert table.c.content.type.length == 200
        assert table.c.content.nullable is False


class TestModelUser:
    def test_table(self):
        assert User.__tablename__ == "users"

    def test_columns(self):
        table = User.__table__

        assert list(table.columns.keys()) == [
            "id",
            "username",
            "password",
        ]

    def test_id(self):
        table = User.__table__

        assert isinstance(
            table.c.id.type,
            Integer,
        )

        assert table.c.id.primary_key is True

    def test_username(self):
        table = User.__table__

        assert isinstance(
            table.c.username.type,
            String,
        )

        assert table.c.username.type.length == 50
        assert table.c.username.unique is True
        assert table.c.username.nullable is False

    def test_password(self):
        table = User.__table__

        assert isinstance(
            table.c.password.type,
            String,
        )

        assert table.c.password.type.length == 120
        assert table.c.password.nullable is False
