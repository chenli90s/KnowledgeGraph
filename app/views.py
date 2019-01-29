from django.shortcuts import render
from django.http import JsonResponse

from pymongo import MongoClient


client = MongoClient('47.100.104.246', 27017, username='root', password='rootadmin', authSource='admin', authMechanism='DEFAULT')


db = client['Data']
collection = db['cn_olbase']

from app.func import save, gen_rela, add_img
from app.es import search as sh

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

def relaction(request):
    cas = request.GET.get('cas', '')
    # item = collection.find_one({'CAS号': cas})
    data = gen_rela(cas)
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
    print(data)
    return JsonResponse(dict(data=data, code=0))



if __name__ == '__main__':
    cas = '350-03-8'
    # kw_type = ['CAS号', '中文名称', '中文别名', '英文名称', '英文别名']
    # item = None
    # for t in kw_type:
    #     result = collection.find_one({t: {'$regex': '.*' + kw + '.*'}})
    #     if result:
    #         item = result
    #         break
    #
    # save(item)
    # item = collection.find_one({'CAS号': cas})
    data = gen_rela(cas)
    sys = data['synts']

    keys = {}
    for index, i in enumerate(sys):
        for curr, f in enumerate(i['front']):

            sys[index]['front'][curr] = {'cas': f, 'url': add_img(f)}
        for curr, f in enumerate(i['back']):

            sys[index]['back'][curr] = {'cas': f, 'url': add_img(f)}
    for index, up in enumerate(data['updown']['ups']):

        data['updown']['ups'][index] = {'cas': up, 'url': add_img(up)}
    for index, down in enumerate(data['updown']['downs']):

        data['updown']['downs'][index] = {'cas': down, 'url': add_img(down)}
    print(data)




