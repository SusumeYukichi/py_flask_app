from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

migrate = Migrate()

csrf = CSRFProtect()

db = SQLAlchemy()

login_manager = LoginManager()
