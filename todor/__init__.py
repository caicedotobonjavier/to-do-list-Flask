from flask import Flask
#
from flask_sqlalchemy import SQLAlchemy
#
from flask import render_template
#


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)


    #Configuracion del proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'javier',
        SQLALCHEMY_DATABASE_URI = "sqlite:///todolist.db"
    )

    #inicializar la conexion a la base de datos
    db.init_app(app)


    #registro blueprint - urls
    from . import todo
    app.register_blueprint(todo.bp)
    #
    from . import auth
    app.register_blueprint(auth.bp)


    @app.route('/')
    def index():
        return render_template('index.html')


    #con esto migro todos los modelos a la base de datos
    with app.app_context():
        db.create_all()
    

    return app