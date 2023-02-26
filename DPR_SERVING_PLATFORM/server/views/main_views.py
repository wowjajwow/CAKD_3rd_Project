from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename # 업로드 된 파일의 이름이 안전한가를 확인해주는 함수. 해킹 공격에 대해 보안을 하고자 사용되기도 함.
import os
import config
from ..forms import Compare_sentence_sim, Context_file, Compare_SnF
from server.search_engines.similarity import *
from server.search_engines.data_utils import *
from server.search_engines.index import *
from server import db
from server import es
from server.models import Documents

bp = Blueprint('main', __name__, url_prefix='/')
simil_result = []

@bp.route('/')
def base():
    client_ip = request.remote_addr
    return render_template('base.html', client_ip=client_ip)

@bp.route('/similarity/<client_ip>', methods=['GET', 'POST'])
def similarity(client_ip):
    form = Compare_sentence_sim()

    if request.method == "POST":
        value1 = form.text1.data
        value2 = form.text2.data
        indicies = get_idx(str(value1), str(value2))
        embeddings = get_pooleroutput(indicies)
        scores = []
        for i in range(1, len(embeddings)):
            scores.append(get_total_scores(embeddings[0], embeddings[i]))
        simil_result.append([str(value1), str(value2), scores])
        return render_template('similarity.html', res=simil_result, client_ip = client_ip)
    else:
        return render_template('similarity.html',client_ip=client_ip)

@bp.route('/file_upload/<client_ip>', methods = ['GET', 'POST'])
def file_upload(client_ip):
    form = Context_file()
    if request.method == "POST":
        f = form.file.data
        if f == None:
            return render_template('file_upload.html', string='status : failed', client_ip=client_ip)
        fname = secure_filename(f.filename)
        print(fname)
        upload_folder = config.UPLOAD_FOLDER
        #doc = Documents(file_name=fname, file_dir=upload_folder)
        save_success,file_path=file_save(f,fname,upload_folder)

        #file_upload_in_db(db, doc)
        indexing_success=file_indexing(file_path)
        save_success = save_success & indexing_success
        if save_success:
            return render_template('file_upload.html', string='status : success', client_ip=client_ip)
        else:
            return render_template('file_upload.html', string='status : failed', client_ip=client_ip)
    else:
        return render_template('file_upload.html', client_ip=client_ip)

@bp.route('/search/<client_ip>', methods = ['GET','POST'])
def search(client_ip):
    form = Compare_SnF()

    if request.method == 'POST':
        q = form.query.data
        n = form.number.data
        # db로 연동시
        # file_list = Documents.query.all()
        # f = merge_file(file_list
        result_list = search_in_es(str(q), int(n))
        return render_template('search.html', result=result_list, client_ip=client_ip)
    else:
        return render_template('search.html', client_ip=client_ip)
@bp.route('/test/<client_ip>', methods = ['GET','POST'])
def test(client_ip):
    query = {
        "query": {
            "match_all": {}
        }
    }
    res=es.search(index='my_index', body=query)

    hits = res.get('hits', {}).get('hits', []) # 실제 데이터가 있는 hits 리스트를 추출합니다
    data = [] # 반환할 데이터를 담을 리스트를 초기화합니다

    # 각각의 문서에 대해서 필요한 정보만 추출하여 data 리스트에 추가합니다
    for hit in hits:
        source = hit.get('_source', {})
        item = {
            'title': source.get('title', ''),
            'content': source.get('content', ''),
            'title_dpr': source.get('title_dpr', []),
            'content_dpr': source.get('content_dpr', []),
        }
        data.append(item)

    return jsonify(data)

@bp.route('/indexing/<client_ip>', methods = ['GET','POST'])
def indexing(client_ip):

    success=file_indexing('./data/data2_new_utf.json')
    if success:
        return "success"
    else :
        return "false"
@bp.route('/delete/<client_ip>', methods = ['GET','POST'])
def delete(client_ip):
    es.indices.delete(index='my_index')
    return 'index deleted'




