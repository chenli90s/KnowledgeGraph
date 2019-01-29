from elasticsearch import Elasticsearch
import pymongo
import json

db = pymongo.MongoClient('10.102.22.70', port=27017)
collection = db['olbase_test']['cn_olbase'].find()

es = Elasticsearch('127.0.0.1:9200')


def import_data():
    # print(collection)
    for item in collection[27618:]:
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
    #                 }
    #             }
    #         }
    #     }
    # }
    # es.indices.create(index='knowledgegraph', body=mapping)
    # import_data()
    cate_forearch()
