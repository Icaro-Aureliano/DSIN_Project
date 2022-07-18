from genericpath import exists
from flask import render_template, url_for, flash, redirect, session, request
from flask_login import login_user, logout_user
from app import app, db, lm
import datetime

from app.models.tables import User, Service, Record

from app.models.forms import LoginForm, RegisForm, ServiceForm

@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/")
def index():
    form = ServiceForm()
    return render_template("index.html", form = form, page = "Home")

@app.route("/historic")
def historic():
    if session["username"] != None or "username" not in session:
        name = session["username"]
        if name == "cabeleleila_leila":
            records = Record.query.all()
            return render_template("historic.html", page = "Histórico", records = records)
        user = User.query.filter_by(username=name).first()
        records = Record.query.filter_by(user_name=user.name).all()
        return render_template("historic.html", page = "Histórico", records = records)
    else:
        return redirect(url_for("login"))

@app.route("/services")
def service():
    if session["username"] != None or "username" not in session:
        name = session["username"]
        user = User.query.filter_by(username=name).first()
        services = Service.query.filter_by(user_id=user.id).all()
        exists = False
        if len(services) != 0:
            exists = True
        return render_template("service.html", page = "Agendamentos", services = services, exist = exists)
    else:
        return redirect(url_for("login"))

@app.route("/add_service", methods=["GET","POST"])
def add_service():
    if "username" in session and session["username"] != None:
        user_name = request.form["name_user"].lower()
        str_date = request.form["date"]
        date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
        content = request.form["content"]
        today = datetime.date.today()

        user = User.query.filter_by(username=user_name).first()
        if user:
            service = Service(user.id, date, content)
            db.session.add(service)
            db.session.commit()
            record = Record(today, user.name, service.content)
            db.session.add(record)
            db.session.commit()
            flash("Atendimento agendado.")
    else:
        flash("Faça login para agendar o atendimento.")

    return redirect(url_for("index"))

@app.route("/remove_service")
def remove_service():
    service_id = request.form["service_id"]
    return "ok"

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user and user.password == form.password.data:
            session["username"] = user.username
            login_user(user)
            flash("Usuario logado.")
            return redirect(url_for("index"))
        else:
            flash("Nome de usuario ou senha invalido.")

    return render_template("login.html", form = form, page = "Login")

@app.route("/logout")
def logout():
    session["username"] = None
    logout_user()
    flash("Usuario desconectado.")
    return redirect(url_for("index"))

@app.route("/registration", methods=["GET","POST"])
def regis():
    form = RegisForm()
    return render_template("registration.html", form = form, page = "Cadastro")

@app.route("/insert",methods=["GET","POST"])
def add_user():
        check = True
        username = request.form["username"].lower()
        password = request.form["password"].lower()
        name = request.form["name"].lower()
        email = request.form["email"].lower()

        if name != "":
            for caracter in name:
                if caracter.isnumeric():
                    flash("Nome invalido")
                    check = False
                    break
        else:
            flash("Nome invalido.")
            check = False

        if User.query.filter_by(username=username).first() and username != "":
            flash("Nome de usuario invalido.")
            check = False

        if User.query.filter_by(email=email).first() and email != "":
            flash("Email invalido.")
            check = False

        if check:
            user = User(username, password, name, email)
            db.session.add(user)
            db.session.commit()
            flash("Usuario cadastrado.")
            return redirect(url_for("login"))

        return redirect(url_for("regis"))