import os
import json
from .similarity import *
from server import es
from konlpy.tag import Hannanum,Mecab,Komoran
import time
from elasticsearch.helpers import bulk
mecab = Komoran()
def file_save(f,fname,upload_folder):
    try :
        file_path = os.path.join(upload_folder, fname)
        print(file_path)
        f.save(file_path)
        if fname in os.listdir(upload_folder):
            print('success')
            return (True, file_path)
        else :
            print('failed')
            return (False, file_path)

    except Exception as e:
        print('-----------------------------------------------------')
        print(e)
        return (False, file_path)


def file_upload_in_db(db, document_obj):
    try:
        db.session.add(document_obj)
        db.session.commit()
        return True
    except:
        return False
def get_morphs(item):
    res = mecab.morphs(item.replace('[^가-힣a-zA-Z0-9]',''))
    return res

def file_indexing(path):
    with open(path,'r',encoding='utf-8') as f:
        json_file=json.load(f)
        count = 0
        for item in json_file:
            start = time.time()
            new_dict = {}
            #title_dpr = model(tokenizer(item['title'], return_tensors="pt")["input_ids"]).pooler_output.detach().numpy().tolist()
            title_dpr = get_title_dpr(item['title'])
            new_dict['title'] = item['title']
            new_dict['title_dpr'] = title_dpr
            #passages=item['content'].split('.')
            #for x in passages:
            #    if x == '':
            #        passages.remove(x)
            #res = []
            #for y in passages:
            #    content_dpr = model(tokenizer(y, return_tensors="pt")["input_ids"]).pooler_output.detach().numpy().tolist()
            #    res.extend(content_dpr)
            #content_dpr = model(tokenizer(item['content'], return_tensors="pt",truncation=True,max_length=512)["input_ids"]).pooler_output.detach().numpy().tolist()
            content_dpr = get_content_dpr(item['content'])
            new_dict['content'] = item['content']
            new_dict['content_dpr'] = content_dpr
            new_dict['content_morphs'] = get_morphs(item['content'])
            new_dict['title_morphs'] = get_morphs(item['title'])
            new_dict['DOCID'] = item['DOCID']
            if item.get("board"):
                new_dict['board'] = item['board']
            if item.get('price'):
                new_dict['price'] = item['price']
            es.index(index='my_index', body=new_dict,id = new_dict['DOCID'])
            end = time.time()
            count += 1
            print(count,':',end-start)

        #bulk(es,json_file,index = 'my_index')
    return True




# if __name__=="__main__":
#     with open('C:/Users/sel20/Downloads/B-99-197001010101-00008-I-C.json','r',encoding="utf-8") as f:
#         data=json.load(f)
#     print(file_indexing(data))




