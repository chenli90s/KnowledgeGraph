from elasticsearch import Elasticsearch
import json

es = Elasticsearch('127.0.0.1:9200')

def search(kw, pageIndex, pageSize, cate=None):
    body = {
        'query': {
            "multi_match": {
                "query": kw,
                "fields": ["cas", "zh", "zh-alias", "en", "en-alias"]
            }
        }
    }

    resp = es.search(index='knowledgegraph',
                     doc_type='KnowledgeGraph',
                     from_=(pageIndex - 1) * pageSize,
                     size=pageSize,
                     body=body)

    items = []
    for hit in resp.get('hits',{}).get('hits',[]):
        content = json.loads(hit['_source']['content'])
        if cate:
            # flag = False
            for cat in cate.split(','):
                if cat in content['category']:
                    items.append(content)
                    break
                # if cat in content['category']:
                #     flag = True
                # else:
                #     flag = False
            # print(flag)
            # if flag:
            #     items.append(content)
        elif not cate:
            items.append(content)
    return {'pageIndex': pageIndex,
            'pageSize': pageSize,
            'total': resp.get('hits',{}).get('total', 0),
            'result': items
            }


def get_data_cas(cas):
    # body = {
    #     'query': {
    #         'cas': cas
    #     }
    # }

    resp = es.search(index='knowledgegraph',
                     doc_type='KnowledgeGraph',
                     q='_id:%s'%cas)

    return json.loads(resp['hits']['hits'][0]['_source']['content'])

if __name__ == '__main__':
    # print(search('9-氯-9-苯基氧杂蒽', 1, 10))
    print(get_data_cas('56803-37-3'))