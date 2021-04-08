from flask import Flask, render_template, request, flash, url_for, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from flask_mail import Mail, Message
from datetime import datetime
# from werkzeug.exceptions import BadGateway, BadRequest, HTTPException


app = Flask(__name__)

app.config.from_object("config")

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail(app)

from app.api.routes import api
from app.login.routes import login

app.register_blueprint(api)
app.register_blueprint(login)

from app.login.forms import LoginForm, Usuario
from app.models.tables import Usuario

@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))

@app.errorhandler(404)
def not_found_error(error):
    return render_template("error.html"),404