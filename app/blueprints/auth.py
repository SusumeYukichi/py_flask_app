from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from ..extensions import db
from ..forms import LoginForm, SignUpForm
from ..models import User

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


@auth_bp.route(
    "/register",
    methods=["GET", "POST"],
)
def register():
    header_message = "アカウント作成画面"

    form = SignUpForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"ようこそ {user.username} さん.\nユーザー新規登録が完了しました.")

        return redirect(url_for("main.lists"))

    # GETまたはPOST:バリデーションFalse
    return render_template(
        "auth/register.html",
        header_message=header_message,
        form=form,
    )


@auth_bp.route(
    "/login",
    methods=["GET", "POST"],
)
def login():
    header_message = "ログイン画面"

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = db.session.scalar(
            db.select(User).filter_by(username=username),
        )

        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"ようこそ {user.username} さん.")

            return redirect(url_for("main.lists"))

        # Formバリデーション:True userのIF判定:False
        flash("ログイン認証エラー:\nユーザー名またはパスワードをご確認ください.\n")

    # GETまたはFormバリデーション:False
    return render_template(
        "auth/login.html",
        header_message=header_message,
        form=form,
    )


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウト完了しました.")

    return redirect(url_for("auth.login"))
