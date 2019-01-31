from elasticsearch import Elasticsearch
import pymongo
import json

db = pymongo.MongoClient('10.102.22.70', port=27017)
collection = db['olbase_test']['cn_olbase'].find()

es = Elasticsearch('127.0.0.1:9200')

# cates = {'生物及医药化学品': 1, '农用化学品': 2, '有机原料与中间体': 4, '催化剂及助剂': 8, '香精与香料': 5, '染料及颜料': 6, '无机化学品': 7, '其他': 8, '食品与饲料添加剂': 9}


def import_data():
    # print(collection)
    for item in collection[90533:]:
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
        except:
            pass


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
