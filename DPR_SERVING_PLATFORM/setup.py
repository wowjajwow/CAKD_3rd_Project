from setuptools import setup, find_packages

setup_requires = [
    "setuptools >=18.0",
]

install_requires = [
    'Flask==2.2.2',
    'Flask_WTF==1.1.1',
    'numpy==1.24.2',
    'transformers==4.26.1',
    'torch==1.12.1+cu113',
    'Flask-Migrate==4.0.4',
    'Flask-SQLAlchemy==3.0.3',
    'elasticsearch==8.6.1>=8.6.1',
    'konlpy==0.6.0',
    'sentencepiece=0.1.97',
    'omegaconf==2.3.0'
    ]

setup(
    name='dpr_serving_platform',
    version='0.3',
    description='dpr_serving_platform',
    author='Seil',
    author_email='sel2015103@gmail.com',
    install_requires=install_requires,
    setup_requires=setup_requires,
    )