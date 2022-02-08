from flask import *
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

bp=Blueprint('auth',__name__,url_prefix='/')
@bp.route("/login",methods=["POST","GET"])
def login():
    if request.method == 'POST':
        email=request.form.get("email")
        password=request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("login succsefful", category='good')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("incorrect password", category='error')
        else:
            flash("email deos not exist", category='error')
    return render_template("login.html")
@bp.route("/sign-in",methods=['POST','GET'])
def sign_in():
    if request.method == 'POST':
        email=request.form.get("email")
        password=request.form.get("password")
        username=request.form.get("username")
        new_user=User(email=email,username=username,password=generate_password_hash(password,method="sha256"))
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(email=email).first()
        if user:
            flash("email is already being used by another client",category='error')
            print("email is in use")
        elif len(username)<2:
            flash("firstname is too short",category="error")
            print("firstname is too short")
        elif len(email)<7:
            flash("email is too short",category="error")
            print('email is too short')
        elif len(password)<5:
            flash("password is too short",category="error")
            print("password is too short")
        else:
            new_user=User(email=email,firstname=username,password=generate_password_hash(password,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("sign-up was succsefful",category="good")
            print("sign-up succsefully")
            return redirect(url_for("views.home"))
            print(f"email: {email} password {password} username {username}")
        return redirect("/")

    return render_template("sign_in.html")
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("login")