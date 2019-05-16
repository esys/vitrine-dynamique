import config
from logging.config import dictConfig

dictConfig(config.log_config)

import os
from flask import Flask, request
from vitrinedynamique.usecases.getannonce import GetAnnonceRequest, GetAnnonceUseCaseFromDatabase, \
    GetAnnonceUseCaseFromNfr
from vitrinedynamique.usecases.listannonces import ListAnnoncesRequest, ListAnnonceUseCaseFromDatabase, \
    ListAnnonceUseCaseFromNfr
from vitrinedynamique.usecases.gethealth import GetHealthRequest, GetHealthUseCase
from vitrinedynamique.usecases.launchtask import LaunchTaskRequest, LaunchTaskUseCase

app = Flask(__name__)
ENV = os.environ.get('STAGE', 'dev')


@app.route('/health')
def health():
    return GetHealthUseCase().execute(GetHealthRequest()).serialize()


@app.route('/annonces/<string:annonce_id>')
def get_annonce(annonce_id: str):
    # use_case = GetAnnonceUseCaseFromDatabase()
    use_case = GetAnnonceUseCaseFromNfr()
    param = GetAnnonceRequest.create(annonce_id)

    return use_case.execute(param).serialize()


@app.route('/annonces')
def list_annonces():
    # use_case = ListAnnonceUseCaseFromDatabase()
    use_case = ListAnnonceUseCaseFromNfr()
    param = ListAnnoncesRequest.create(request.args)

    return use_case.execute(param).serialize()


@app.route('/task/<string:task_name>')
def execute_task(task_name: str):
    use_case = LaunchTaskUseCase()
    param = LaunchTaskRequest.create(task_name, request.args)

    return use_case.execute(param).serialize()
