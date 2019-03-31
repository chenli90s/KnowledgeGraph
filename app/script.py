from elasticsearch import Elasticsearch
import pymongo
import json
from googletrans import Translator
translator = Translator(service_urls=['translate.google.cn'])


db = pymongo.MongoClient('10.102.24.46', port=27017)
collection = db['Data']['cn_olbase_sup'].find()

es = Elasticsearch('10.102.24.46:9200')

# cates = {'生物及医药化学品': 1, '农用化学品': 2, '有机原料与中间体': 4, '催化剂及助剂': 8, '香精与香料': 5, '染料及颜料': 6, '无机化学品': 7, '其他': 8, '食品与饲料添加剂': 9}


def import_data():
    # print(collection)
    for item in collection:
        try:
            es.index(index='knowledgegraph', doc_type="KnowledgeGraph", id=item['CAS号'],
                     body={
                         'cas': item['CAS号'],
                         'zh': item.get('中文名称', ''),
                         'zh-alias': item.get('中文别名', ''),
                         'en': item.get('英文名称', ''),
                         'en-alias': item.get('英文别名', ''),
                         'content': json.dumps(item['item'])
                        }
                     )
            # import_molbase(item['CAS号'])
        except:
            pass

def check_synthesis():
    cn_app = db['OLBASE']['cn_app_1']
    cn_rela = db['OLBASE']['cn_relaction']
    rela_key = ['synthesis', 'upstream', 'downstream']
    datas = cn_app.find()
    for data in datas:
        res = data['info']['retval']['result_cas']
        keys = []
        for key in rela_key:
            if res[key]:
                keys.append(key)
        try:
            if res['synthesis'] or res['upstream'] or res['downstream']:
                cn_rela.insert_many([{'mol_id': res['mol_id'], 'cas': res['cas_no'], 'keys': keys}])
        except:
            pass

from app.cli import get_tag_data, get_app_data
# from app.func import build_updowns_rela, build_synt_rela
import time
import hashlib

def token():
    params = 'hdkCMA!qxH8Qv&IVZHEn2ar#oqCW!%mM'
    l = str(time.time()).split('.')[0]
    md5 = hashlib.md5()
    md5.update((params + l).encode())
    return md5.hexdigest().upper() + l

def get_mol_id(cas):
    try:
        search_url = 'http://zh.molbase.com/index.php?app=api&c=search&a=result_21&lang=zh&clientType=1&v=2.0&TOKEN=' + token()

        resp = get_app_data(search_url, {'page': 1, 'keyword': cas, 'SN_API': ''})
        basic = resp.json()
        mol_id = basic['retval']['result_cas']['mol_id']
        return mol_id
    except:
        pass

def import_molbase(cas):
    # rela_db = db['OLBASE']['cn_relaction']
    # res = rela_db.find_one({'cas': cas})
    url = 'https://m.molbase.cn/api/moldata/detail/tag?keywords=%s&tag=xianlu&page=1&page_size=100'
    up_url = 'https://m.molbase.cn/api/moldata/detail/tag?keywords=%s&page=1&page_size=100&tag=shangyou'
    down_url = 'https://m.molbase.cn/api/moldata/detail/tag?keywords=%s&page=1&page_size=100&tag=xiayou'

    # id = res['mol_id']
    id = get_mol_id(cas)
    if id:
        datas = []
        res = get_tag_data(url%id).json()

        for data in res['data']:
            front = []
            for f in data['upper']:
                front.append({'cas': f['cas_no'], 'url': 'http:'+f['s_pic'], 'name': get_node_name(f['cas_no'])})
            back = []
            for b in data['upper']:
                back.append({'cas': b['cas_no'], 'url': 'http:'+b['s_pic'], 'name': get_node_name(b['cas_no'])})

            trans = translator.translate(data['conditions'], src='en', dest='zh-cn').text
            datas.append({'front': front, 'back': back, 'pre': data['yield_all'], 'conditions': trans})

        res = get_tag_data(up_url % id).json()
        ups = []
        for data in res['data']:
            ups.append({'cas': data['cas_no'], 'url': 'http:' + data['s_pic'], 'name': get_node_name(data['cas_no'])})

        res = get_tag_data(down_url % id).json()
        downs = []
        for data in res['data']:
            downs.append({'cas': data['cas_no'], 'url': 'http:' + data['s_pic'], 'name': get_node_name(data['cas_no'])})

        updowns = {'ups': ups, 'downs': downs}

        # print(datas)
        # print(updowns)

        return datas, updowns

def get_node_name(cas):
    doc = db['Data']['cn_migration']
    res = doc.find_one({'cas': cas})
    print(cas)
    if res:
        return res.get('中文名称', '')
    return ''


if __name__ == '__main__':
    # kw_type = ['CAS号', '中文名称', '中文别名', '英文名称', '英文别名']
    # mapping = {
    #     "mappings": {
    #         "KnowledgeGraph": {
    #             "properties": {
    #                 "cas": {
    #                     "type": "text",
    #                     "analyzer": "ik_max_word",
    #                     "search_analyzer": "ik_max_word"
    #                 },
    #                 "zh": {
    #                     "type": "text",
    #                     "analyzer": "ik_max_word",
    #                     "search_analyzer": "ik_max_word"
    #                 },
    #                 "zh-alias": {
    #                     "type": "text",
    #                     "analyzer": "ik_max_word",
    #                     "search_analyzer": "ik_max_word"
    #                 },
    #                 "en": {
    #                     "type": "text",
    #                     "analyzer": "ik_max_word",
    #                     "search_analyzer": "ik_max_word"
    #                 },
    #                 "en-alias": {
    #                     "type": "text",
    #                     "analyzer": "ik_max_word",
    #                     "search_analyzer": "ik_max_word"
    #                 },
    #                 'content': {
    #                     'type': 'text'
    #                 },
    #             }
    #         }
    #     }
    # }
    # es.indices.create(index='knowledgegraph', body=mapping)
    import_data()
    # check_synthesis()
    # import_molbase('1631-83-0')
    # print(get_mol_id('5345-47-1'))
    # es.indices.delete
