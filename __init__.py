from flask import *
from flask_sqlalchemy import *
from os import *
from flask_login import LoginManager

db=SQLAlchemy()
db_name="database.db"
def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'hey there guy'  
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)

    from . import views
    from. import auth
    from .models import User,Image

    app.register_blueprint(views.bp)
    app.register_blueprint(auth.bp)

    create_database(app)

    login_manager=LoginManager()
    login_manager.login_view="auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app

def create_database(app):
    if not path.exists(f"website/{db_name}"):
        db.create_all(app=app)
        print("created database")