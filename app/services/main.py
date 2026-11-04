from flask_login import current_user

from ..extensions import db
from ..models import Memo


def get_memo_table():

    memo_table = db.session.scalars(
        db.select(Memo)
        .filter_by(
            user_id=current_user.id,
        )
        .order_by(Memo.id.asc())
    ).all()

    return memo_table


def get_categories(memo_table):
    memo_categories = {memo.category for memo in memo_table}

    return memo_categories


def get_count_memo_number():
    memo_count = db.session.scalar(
        db.select(
            db.func.count(Memo.id),
        ).where(
            Memo.user_id == current_user.id,
        )
    )

    return memo_count
