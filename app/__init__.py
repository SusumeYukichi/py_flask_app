import logging
from pathlib import Path

from flask import Flask, render_template

from .admin import load_user
from .blueprints.auth import auth_bp
from .blueprints.main import main_bp
from .blueprints.memo import memo_bp
from .blueprints.text_processing import txt_bp
from .config import Config
from .extensions import csrf, db, login_manager, migrate
from .filters import register_filters


def create_app(
    config_class=Config,
):

    APP_DIR = Path(__file__).resolve().parent

    app = Flask(
        __name__,
        instance_path=str(APP_DIR / "instance"),
    )

    app.logger.setLevel(logging.INFO)

    app.config.from_object(config_class)

    db.init_app(app)

    migrate.init_app(
        app,
        db,
        directory=str(APP_DIR / "migrations"),
    )

    csrf.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(memo_bp)
    app.register_blueprint(txt_bp)

    register_filters(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "ログイン認証エラー:\n再ログインしてください."
    login_manager.user_loader(load_user)

    # エラーハンドラー
    @app.errorhandler(404)
    def show_404_page(error):
        msg = error.description
        print(
            "404エラー内容:",
            msg,
        )

        header_message = "ステータスコード:404"
        error_message = "お探しのページは見つかりませんでした."

        return render_template(
            "error/404.html",
            header_message=header_message,
            error_message=error_message,
        ), 404

    return app
