from django.shortcuts import render
from django.http import JsonResponse

from pymongo import MongoClient


client = MongoClient('localhost', 27017)


db = client['Data']
collection = db['cn_olbase']

from app.func import save, gen_rela, add_img, relactionship_search, func_search_new, build_synt_rela, build_updowns_rela
from app.es import search as sh
from app.es import get_data_cas
from app.func import get_wx


# Create your views here.
def search(request):
    kw = request.GET.get('kw', '')
    pageIndex = int(request.GET.get('pageIndex', 1))
    pageSize = int(request.GET.get('pageSize', 10))
    cate = request.GET.get('cate', '')
    # if not kw:
    #     return JsonResponse(dict(code=-1, msg='kw is null'))
    #
    # # 查询属性
    # # kw_type = ['CAS号', '中文名称', '中文别名', '英文名称', '英文别名']
    # cas = collection.find_one({'CAS ': kw})
    # # es.search()
    #
    # # item = None
    # # for t in kw_type:
    # #     result = collection.find_one({t: {'$regex': '.*' + kw+ '.*'}})
    # #     if result:
    # #         item = result
    # #         break
    # # save(item)
    # print(cas)
    # if cas:
    #     del cas['_id']
    return JsonResponse(dict(code=0, data=sh(kw, pageIndex, pageSize, cate)))

def get_data(request):
    kw = request.GET.get('cas', '')
    res = get_data_cas(kw)
    if res:
        return JsonResponse(dict(code=0, data=get_data_cas(kw)))
    else:
        return JsonResponse(dict(code=-1, data='数据不存在'))


def relaction(request):
    cas = request.GET.get('cas', '')
    # item = collection.find_one({'CAS号': cas})
    DB = client['OLBASE']
    document = DB['cn_olbase_rela']
    res = document.find_one({'cas': cas})
    if not res:
        # res = res['data']
        # res['synts'] = res['synts'][:3]
        # res['updown']['ups'] = res['updown']['ups'][:3]
        # res['updown']['downs'] = res['updown']['downs'][:3]
        # return JsonResponse(dict(data=res, code=0))
        res = gen_rela(cas)
        document.insert_many([{'cas': cas, 'data': res}])
        res = {'cas': cas, 'data': res}
    data = res['data']
    print(data)
    build_updowns_rela(data['updown'], cas)
    build_synt_rela(data['synts'])
    # sys = data['synts']
    # keys = []
    # for index, i in enumerate(sys):
    #     for curr, f in enumerate(i['front']):
    #         if f not in keys:
    #             sys[index]['front'][curr] = {'cas': f, 'url': add_img(f)}
    #             keys.append(f)
    #     for curr, f in enumerate(i['back']):
    #         if f not in keys:
    #             sys[index]['back'][curr] = {'cas': f, 'url': add_img(f)}
    #             keys.append(f)
    # for index, up in enumerate(data['updown']['ups']):
    #     if up not in keys:
    #         data['updown']['ups'][index] = {'cas': up, 'url': add_img(up)}
    #         keys.append(up)
    # for index, down in enumerate(data['updown']['downs']):
    #     if down not in keys:
    #         data['updown']['downs'][index] = {'cas': down, 'url': add_img(down)}
    #         keys.append(down)
    # print(data)

    data['synts'] = data['synts'][:3]
    data['updown']['ups'] = data['updown']['ups'][:3]
    data['updown']['downs'] = data['updown']['downs'][:3]
    return JsonResponse(dict(data=data, code=0))

def relactionshipSearch(request):
    target = request.GET.get('target', '')
    source = request.GET.get('source', '')
    level = request.GET.get('level', '3')
    # types = request.GET.get('type', '')
    types = ['合成路线', "上游", "下游"]
    # print(target)
    # print(source)
    # print(types)
    if target and source:
        result = []
        for typ in types:
            relas = relactionship_search(target, source, typ, level)
            result += relas
        return JsonResponse(dict(code=0, data=result))
    return JsonResponse(dict(code=-1, msg='params is null'))


def search_new(request):
    keyword = request.GET.get('kw', '')
    dict_new_data = func_search_new(keyword)
    return JsonResponse(dict_new_data)



# if __name__ == '__main__':
#     cas = '350-03-8'
#     # kw_type = ['CAS号', '中文名称', '中文别名', '英文名称', '英文别名']
#     # item = None
#     # for t in kw_type:
#     #     result = collection.find_one({t: {'$regex': '.*' + kw + '.*'}})
#     #     if result:
#     #         item = result
#     #         break
#     #
#     # save(item)
#     # item = collection.find_one({'CAS号': cas})
#     data = gen_rela(cas)
#     sys = data['synts']
#
#     keys = {}
#     for index, i in enumerate(sys):
#         for curr, f in enumerate(i['front']):
#
#             sys[index]['front'][curr] = {'cas': f, 'url': add_img(f)}
#         for curr, f in enumerate(i['back']):
#
#             sys[index]['back'][curr] = {'cas': f, 'url': add_img(f)}
#     for index, up in enumerate(data['updown']['ups']):
#
#         data['updown']['ups'][index] = {'cas': up, 'url': add_img(up)}
#     for index, down in enumerate(data['updown']['downs']):
#
#         data['updown']['downs'][index] = {'cas': down, 'url': add_img(down)}
#
#     print(data)


# 文献检索
def search_literature(request):
    cas = request.GET.get('cas', None)
    page = request.GET.get('page', None)
    if cas:
        doc_info = get_wx(cas, page)
        return JsonResponse({'docInfo': doc_info})
    else:
        return JsonResponse({'error': "cas can't be NULL"})

if __name__ == '__main__':
    DB = client['OLBASE']
    document = DB['cn_olbase_rela']
    # document.remove({})
    res = document.find_one({'cas': '947-42-2'})
    del res['_id']
    print(res)
    import json
    print(json.dumps(res))
