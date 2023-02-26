import os

DEBUG=False
# config.py

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
UPLOAD_FOLDER='./data/'

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'cakd.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False


# 인덱스 생성

settings = {
        'analysis': {
            'analyzer': {
                'korean': {
                    'type': 'custom',
                    'tokenizer': 'seunjeon_tokenizer'
                }
            }
        }
    }
mappings = {
        'properties': {
            'title': {'type': 'text', 'analyzer': 'korean'},
            'content': {'type': 'text', 'analyzer': 'korean'}
        }
    }
