from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import datetime
# -*- coding: utf-8 -*-
"""
Configuración del servidor Flask y la base de datos
Este módulo configura la aplicación Flask, la base de datos SQLite y las extensiones necesarias.
Este archivo es parte del proyecto de gestión de reclamos y usuarios.
"""

app = Flask("server")
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

def crear_engine():
    engine = create_engine("sqlite:///docs/base_datos.db")
    Session = sessionmaker(bind=engine)
    return engine, Session

app.config.from_object(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=5)
Session(app)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
# Bootstrap
Bootstrap(app)

login_manager.login_view = 'iniciar_sesion'