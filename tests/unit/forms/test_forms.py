from datetime import date

from wtforms import DateField, PasswordField, RadioField, StringField, TextAreaField
from wtforms.validators import Length

from app.forms import InputForm, LoginForm, SignUpForm


class TestFormInputForm:
    def test_success_new(
        self,
        test_app,
    ):
        with test_app.test_request_context(
            "/new",
            method="POST",
            data={
                "input_date": "2026-08-09",
                "subject": "件名のテスト",
                "category": "カテゴリのテスト",
                "content": "1行目\n2行目",
                "level_radio": "medium",
                "close_date": "2026-08-09",
                "select_category": "organize",
            },
        ):
            form = InputForm(meta={"csrf": False})

            assert form.validate() is True

            assert isinstance(
                form.input_date,
                DateField,
            )

            assert isinstance(
                form.subject,
                StringField,
            )

            assert isinstance(
                form.category,
                StringField,
            )

            assert isinstance(
                form.content,
                TextAreaField,
            )

            assert isinstance(
                form.level_radio,
                RadioField,
            )

            assert isinstance(
                form.close_date,
                DateField,
            )

            assert form.input_date.data == date(
                2026,
                8,
                9,
            )

            assert form.close_date.data == date(
                2026,
                8,
                9,
            )

            assert form.subject.data == "件名のテスト"
            assert form.category.data == "カテゴリのテスト"
            assert form.content.data == "1行目\n2行目"

    def test_error_empty_new(
        self,
        test_app,
    ):
        with test_app.test_request_context(
            "/new",
            method="POST",
            data={
                "input_date": "",
                "subject": "",
                "category": "",
                "content": "",
            },
        ):
            form = InputForm(meta={"csrf": False})

            assert form.validate() is False
            assert "日付は入力必須です." in form.input_date.errors
            assert "件名は入力必須です." in form.subject.errors
            assert "カテゴリは入力必須です." in form.category.errors
            assert "内容は入力必須です." in form.content.errors

    def test_success_maxlength_new(
        self,
        test_app,
    ):
        with test_app.test_request_context("/new"):
            form = InputForm(meta={"csrf": False})

            subject_length = next(
                validator
                for validator in form.subject.validators
                if isinstance(
                    validator,
                    Length,
                )
            )

            category_length = next(
                validator
                for validator in form.category.validators
                if isinstance(
                    validator,
                    Length,
                )
            )

            content_length = next(
                validator
                for validator in form.content.validators
                if isinstance(
                    validator,
                    Length,
                )
            )

            assert subject_length.max == 30
            assert category_length.max == 25
            assert content_length.max == 180

    def test_success_length_new(
        self,
        test_app,
    ):
        with test_app.test_request_context("/new"):
            form = InputForm(meta={"csrf": False})

            assert form.subject.render_kw["maxlength"] == 30
            assert form.category.render_kw["maxlength"] == 25
            assert form.content.render_kw["maxlength"] == 180

            assert 'maxlength="30"' in str(form.subject())
            assert 'maxlength="25"' in str(form.category())
            assert 'maxlength="180"' in str(form.content())

    def test_error_length_new(
        self,
        test_app,
    ):
        with test_app.test_request_context(
            "/new",
            method="POST",
            data={
                "input_date": "2026-08-09",
                "subject": "あ" * 31,
                "category": "い" * 26,
                "content": "う" * 181,
            },
        ):
            form = InputForm(meta={"csrf": False})

            assert form.validate() is False

            assert "件名は30文字以内で入力してください." in form.subject.errors
            assert "カテゴリは25文字以内で入力してください." in form.category.errors
            assert "内容は180文字以内で入力してください." in form.content.errors


class TestFormLoginForm:
    def test_success_login(
        self,
        test_app,
    ):
        with test_app.test_request_context(
            "/login",
            method="POST",
            data={
                "username": "test",
                "password": "test",
            },
        ):
            form = LoginForm(meta={"csrf": False})

            assert form.validate() is True

            assert form.username.data == "test"
            assert form.password.data == "test"

            assert isinstance(
                form.username,
                StringField,
            )
            assert isinstance(
                form.password,
                PasswordField,
            )

    def test_error_empty_login(
        self,
        test_app,
    ):
        with test_app.test_request_context(
            "/login",
            method="POST",
            data={
                "username": "",
                "password": "",
            },
        ):
            form = LoginForm(meta={"csrf": False})

            assert form.validate() is False
            assert "ユーザー名は必須入力です." in form.username.errors
            assert "パスワードの長さは4文字以上10文字以内です." in form.password.errors

    def test_success_length_login(
        self,
        test_app,
    ):
        with test_app.test_request_context("/login"):
            form = LoginForm(meta={"csrf": False})

            password_length = next(
                validator
                for validator in form.password.validators
                if isinstance(
                    validator,
                    Length,
                )
            )

            assert password_length.min == 4
            assert password_length.max == 10

    def test_error_maxlength_login(
        self,
        test_app,
    ):
        with test_app.test_request_context(
            "/login",
            method="POST",
            data={
                "username": "test",
                "password": "あ" * 11,
            },
        ):
            form = LoginForm(meta={"csrf": False})

            assert form.validate() is False
            assert form.username.errors == []
            assert "パスワードの長さは4文字以上10文字以内です." in form.password.errors

    def test_error_minlength_login(
        self,
        test_app,
    ):
        with test_app.test_request_context(
            "/login",
            method="POST",
            data={
                "username": "test",
                "password": "あ" * 3,
            },
        ):
            form = LoginForm(meta={"csrf": False})

            assert form.validate() is False
            assert form.username.errors == []
            assert "パスワードの長さは4文字以上10文字以内です." in form.password.errors


class TestFormSignUpForm:
    def test_success_register(
        self,
        test_app,
    ):
        with test_app.test_request_context(
            "/register",
            method="POST",
            data={
                "username": "new_test_user",
                "password": "test",
            },
        ):
            form = SignUpForm(meta={"csrf": False})

            assert form.validate() is True, form.errors
            assert form.username.data == "new_test_user"
            assert form.password.data == "test"

            assert isinstance(
                form.username,
                StringField,
            )

            assert isinstance(
                form.password,
                PasswordField,
            )

    def test_error_empty_register(
        self,
        test_app,
    ):
        with test_app.test_request_context(
            "/register",
            method="POST",
            data={
                "username": "",
                "password": "",
            },
        ):
            form = SignUpForm(meta={"csrf": False})

            assert form.validate() is False
            assert "ユーザー名は必須入力です." in form.username.errors
            assert "パスワードの長さは4文字以上10文字以内です." in form.password.errors

    def test_success_length_register(
        self,
        test_app,
    ):
        with test_app.test_request_context("/register"):
            form = SignUpForm(meta={"csrf": False})

            password_length = next(
                validator
                for validator in form.password.validators
                if isinstance(
                    validator,
                    Length,
                )
            )

            assert password_length.min == 4
            assert password_length.max == 10
