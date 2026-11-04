from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, ValidationError

from .extensions import db
from .models import User


# InputForm
class InputForm(FlaskForm):
    input_date = DateField(
        "作成日",
        validators=[
            DataRequired(
                message="日付は入力必須です.",
            ),
        ],
        format="%Y-%m-%d",
    )

    subject = StringField(
        "タイトル",
        default="IT用語の情報整理",
        validators=[
            DataRequired(
                message="件名は入力必須です.",
            ),
            Length(
                max=30,
                message="件名は30文字以内で入力してください.",
            ),
        ],
        render_kw={"maxlength": 30},
    )

    select_category = SelectField(
        "分類",
        choices=[
            ("organize", "情報整理"),
            ("analysis", ".txt"),
        ],
    )

    level_radio = RadioField(
        "重要度",
        choices=[
            ("high", "高"),
            ("medium", "普通"),
            ("low", "低"),
        ],
        default="medium",
    )

    category = StringField(
        "登録用語",
        default="Prompt",
        validators=[
            DataRequired(
                message="カテゴリは入力必須です.",
            ),
            Length(
                max=25,
                message="カテゴリは25文字以内で入力してください.",
            ),
        ],
        render_kw={"maxlength": 25},
    )

    content = TextAreaField(
        "内容",
        default=("Prompt\n機能:AIに対するテキスト出力\n関連語:AI"),
        validators=[
            DataRequired(
                message="内容は入力必須です.",
            ),
            Length(
                max=180,
                message="内容は180文字以内で入力してください.",
            ),
        ],
        render_kw={
            "rows": 6,
            "cols": 30,
            "maxlength": 180,
        },
    )

    close_date = DateField(
        "用語更新予定日",
        validators=[
            DataRequired(
                message="日付は入力必須です.",
            ),
        ],
        format="%Y-%m-%d",
    )

    submit = SubmitField(
        "実行",
        render_kw={"class": "submit button"},
    )


# LoginForm
class LoginForm(FlaskForm):
    username = StringField(
        "ユーザー名:",
        validators=[
            DataRequired(
                "ユーザー名は必須入力です.",
            ),
        ],
    )

    password = PasswordField(
        "パスワード:",
        validators=[
            Length(
                4,
                10,
                "パスワードの長さは4文字以上10文字以内です.",
            ),
        ],
    )

    submit = SubmitField(
        "認証",
        render_kw={"class": "submit button"},
    )


# SignUpForm
class SignUpForm(LoginForm):
    submit = SubmitField(
        "登録",
        render_kw={"class": "submit button"},
    )

    # カスタムバリデータ
    def validate_username(
        self,
        username,
    ):
        user = db.session.scalar(
            db.select(User).filter_by(
                username=username.data,
            ),
        )

        if user:
            raise ValidationError(
                "そのユーザー名は既に使用されています.",
            )
