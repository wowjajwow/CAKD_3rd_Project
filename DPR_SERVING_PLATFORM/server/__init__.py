from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from config import *

# flask-migrate 를 pip 해주고 cmd창에서 flask db init을 해주면 migrations 폴더가 자동으로 생성됨

import config

db = SQLAlchemy()
migrate = Migrate()
es = Elasticsearch({'host':'52.78.186.115','port':9200,'scheme': 'http'})
es = Elasticsearch({'host':'localhost','port':9200,'scheme': 'http'})
#es.indices.delete(index='my_index')
es.indices.create(index ='my_index',ignore=400,settings=settings,mappings=mappings)
def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
    
    # 블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app

