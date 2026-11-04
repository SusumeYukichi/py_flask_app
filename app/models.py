from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class Memo(db.Model):
    __tablename__ = "memo_table"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    input_date = db.Column(
        db.Date,
        nullable=False,
    )

    subject = db.Column(
        db.String(30),
        nullable=False,
    )

    category = db.Column(
        db.String(30),
        nullable=False,
        default="未分類",
    )

    content = db.Column(
        db.Text(200),
        nullable=False,
    )

    level_radio = db.Column(
        db.String(10),
        nullable=False,
        default="medium",
    )

    close_date = db.Column(
        db.Date,
        nullable=False,
    )

    select_category = db.Column(
        db.String(10),
        nullable=False,
    )
    # 外部キー
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            name="fk_memos_users",
        ),
        nullable=False,
    )

    # Memo側
    user = relationship(
        "User",
        back_populates="memos",
    )


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
    )

    password = db.Column(
        db.String(120),
        nullable=False,
    )

    # リレーション:User側
    memos = relationship(
        "Memo",
        back_populates="user",
    )

    def set_password(
        self,
        password,
    ):
        self.password = generate_password_hash(password)

    def check_password(
        self,
        password,
    ):
        return check_password_hash(
            self.password,
            password,
        )
