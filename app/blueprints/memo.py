from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..forms import InputForm
from ..models import Memo

memo_bp = Blueprint(
    "memo",
    __name__,
    url_prefix="/memo",
)


@memo_bp.route(
    "/new",
    methods=["GET", "POST"],
)
@login_required
def new_index():
    header_message = "用語新規作成画面"

    form = InputForm()

    if form.validate_on_submit():
        memo = Memo(
            input_date=form.input_date.data,
            subject=form.subject.data,
            category=form.category.data,
            content=form.content.data,
            level_radio=form.level_radio.data,
            close_date=form.close_date.data,
            select_category=form.select_category.data,
            user_id=current_user.id,
        )
        db.session.add(memo)
        db.session.commit()
        flash("新規作成しました.")

        return redirect(url_for("main.lists"))

    # GETまたはPOST:バリデーションFalse
    return render_template(
        "memo/new.html",
        header_message=header_message,
        form=form,
    )


@memo_bp.route(
    "/edit/<int:memo_id>",
    methods=["GET", "POST"],
)
@login_required
def edit_memo(memo_id):
    header_message = "用語編集(更新)画面"

    memo = db.first_or_404(
        db.select(Memo).filter_by(
            id=memo_id,
            user_id=current_user.id,
        )
    )

    form = InputForm(obj=memo)

    if form.validate_on_submit():
        memo.input_date = form.input_date.data
        memo.subject = form.subject.data
        memo.category = form.category.data
        memo.content = form.content.data
        memo.level_radio = form.level_radio.data
        memo.close_date = form.close_date.data
        memo.select_category = form.select_category.data
        db.session.commit()
        flash("編集完了しました.")

        return redirect(url_for("main.lists"))

    # GETまたはPOST:バリデーションFalse
    return render_template(
        "memo/edit.html",
        header_message=header_message,
        form=form,
    )


@memo_bp.route(
    "/delete/<int:memo_id>",
    methods=["POST"],
)
@login_required
def delete_memo(memo_id):

    memo = db.first_or_404(
        db.select(Memo).filter_by(
            id=memo_id,
            user_id=current_user.id,
        )
    )

    db.session.delete(memo)
    db.session.commit()
    flash("削除完了しました.")

    return redirect(url_for("main.lists"))
