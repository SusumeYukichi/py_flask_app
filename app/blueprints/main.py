from flask import Blueprint, render_template
from flask_login import current_user, login_required

from ..extensions import db
from ..forms import InputForm
from ..models import Memo
from ..services import (
    get_categories,
    get_count_memo_number,
    get_memo_table,
    text_processing,
)

# url_prefix不要:('/')
main_bp = Blueprint(
    "main",
    __name__,
)


@main_bp.route("/")
def index():
    header_message = "トップページ画面"

    return render_template(
        "main/index.html",
        header_message=header_message,
    )


@main_bp.route("/input")
def input_file():
    header_message = ".txt表示画面"

    # ファイルのPath取得
    file_path = text_processing.get_input_file_path()

    # 対象ファイル取得 input.txt
    file_content = text_processing.read_input_file(file_path)

    # 対象ファイルのテキスト文字数カウント
    character_count = text_processing.count_characters(file_content)

    return render_template(
        "text_processing/input.html",
        header_message=header_message,
        file_content=file_content,
        character_count=character_count,
    )


@main_bp.route("/lists")
@login_required
def lists():
    header_message = "用語管理画面"

    memo_table = get_memo_table()
    memo_categories = get_categories(memo_table)

    memo_count = get_count_memo_number()

    return render_template(
        "memo/lists.html",
        header_message=header_message,
        memo_lists=memo_table,
        categories=memo_categories,
        memo_count=memo_count,
    )


@main_bp.route("/details")
@login_required
def lists_details():
    header_message = "用語確認画面"

    memo_table = db.session.scalars(
        db.select(Memo)
        .filter_by(
            user_id=current_user.id,
        )
        .order_by(Memo.id.asc())
    ).all()

    return render_template(
        "memo/details.html",
        header_message=header_message,
        memo_lists=memo_table,
    )


@main_bp.route("/delete")
@login_required
def lists_delete():
    header_message = "用語削除画面"

    form = InputForm()

    memo_table = db.session.scalars(
        db.select(Memo)
        .filter_by(
            user_id=current_user.id,
        )
        .order_by(Memo.id.asc())
    ).all()

    return render_template(
        "memo/delete.html",
        header_message=header_message,
        form=form,
        memo_lists=memo_table,
    )
