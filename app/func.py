import requests
from lxml import etree
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import time
import random
graph = Graph('http://10.102.24.46:9292', username='neo4j', password='admin')

matcher = NodeMatcher(graph)
rela_matcher = RelationshipMatcher(graph)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    # 'cookie': "my_mbcookie=9381740248; gr_user_id=aadb4e55-834c-4b15-9629-0ad5b46be83f; grwng_uid=8afb463c-2554-482a-b175-584868f76b76; _ga=GA1.2.1853337866.1539237768; deny_ip=UWMHa1ViACtWYFBoVGAHLgBvAzJReAg0VmUGMw%3D%3D; g_step_tmp=1; _pk_ref.2.9731=%5B%22%22%2C%22%22%2C1541396804%2C%22http%3A%2F%2Fwww.molbase.com%2Fen%2F488-93-7-moldata-179475.html%22%5D; _pk_ses.2.9731=*; ad747e1972c640de_gr_session_id=7e1a2bb0-a122-4b3f-a364-e2ecd53690c0; _gid=GA1.2.1927091434.1541396804; ad747e1972c640de_gr_session_id_7e1a2bb0-a122-4b3f-a364-e2ecd53690c0=true; current_user_key=689615e92a91e9b63ff65108985e2782; count_views_key=113c494d84d1f9713d661963f783d079; ECM_ID=rf5ko34u1lcn6vn2vd67s0t061; ECM_ID=rf5ko34u1lcn6vn2vd67s0t061; Hm_lvt_16ee3e47bd5e54a79fa2659fe457ff1e=1539237692,1539323463,1541127887,1541396811; _pk_id.2.9731=b06a2f06be918374.1539237692.7.1541399717.1541396804.; Hm_lpvt_16ee3e47bd5e54a79fa2659fe457ff1e=1541399717; lighting=eyJpdiI6IjFJNnJQUTNuUjh0TzQ3WFZcL1ZlOG13PT0iLCJ2YWx1ZSI6IlhYK1UyVW50ekx6SzVnTWlScXkxbzUwTEJCOW1Eb1BtdEIxTXRaWnE1SzR6RTNrM1JJMXRcL0tpRCtKSmgxaHptNTB2VTdTTnl5OFZqOTZ6V05INDJSZz09IiwibWFjIjoiMTIxYTRhZWJiZjJlYjAyYzg1MmFjNzUzZmZiODg1OTJlOTE1NGI2YzZkMzYxNmY1MGRlMTU4NTg5Y2ViZmQwZiJ9",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Host': 'data.huaxuejia.cn',
    'Accept-Encoding': 'gzip, deflate'
}


def set_imgs(cas):
    num = cas.split('-')[0]
    num = num[-3:] if len(num) > 3 else num
    return 'http://data.huaxuejia.cn/casimg/%s/%s.png' % (num, cas), 'http://data.huaxuejia.cn/casimg/%s/%s.gif' % (
        num, cas)


def loading_updownstream(content):
    eles = etree.HTML(content)
    updowns = eles.xpath('//ul[@class="list-inline mb20 udStream_list"]')
    up = []
    try:
        ups = updowns[0].xpath('./li/p[1]/text()')
        ups_img = updowns[0].xpath('./li/div/a/img/@src')

        for index, i in enumerate(ups):
            up.append(dict(cas=i, url=ups_img[index]))
    except:
        pass
    down = []
    try:
        downs = updowns[1].xpath('./li/p[1]/text()')
        downs_img = updowns[1].xpath('./li/div/a/img/@src')

        for index, i in enumerate(downs):
            down.append(dict(cas=i, url=downs_img[index]))
    except:
        pass
    item = eles.xpath('//div[@class="ip_box"]/dl')
    content = []
    for i in item:
        content.append(i.xpath('string(.)'))
    return {'ups': up, 'downs': down}, content


def local_page(cas):
    """
    local synthesis html
    :param cas:
    :return:
    """
    # num = cas.split('-')[0]
    # num = num[-3:] if len(num)>3 else num
    # url = 'http://data.huaxuejia.cn/html/%s/syn_%s.html'%(num, cas)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'data.huaxuejia.cn',
        'Accept-Encoding': 'gzip, deflate'
    }
    req = requests.session()
    req.post('http://data.huaxuejia.cn/search.php', headers=headers,
             data={'search_keyword': cas, 'cookies': 'Y'})
    time.sleep(0.5)
    req.post('http://data.huaxuejia.cn/search.php', headers=headers,
             data={'search_keyword': cas, 'cookies': 'Y'})
    time.sleep(0.5)
    resp = req.post('http://data.huaxuejia.cn/search.php', headers=headers,
                    data={'search_keyword': cas, 'cookies': 'Y'})
    updowns, items = loading_updownstream(resp.content)
    print(resp.url)
    resp = requests.get(resp.url.replace('cas', 'syn'), headers=headers)
    eles = etree.HTML(resp.content)
    return eles, updowns, items


def parse_synthesis(cas):
    """
    parse synthesis html info
    :param cas:
    :return:
    """
    eles, updowns, its = local_page(cas)
    items = eles.xpath('//div[@class="synRoute"]')
    routes = []
    if len(items)>5:
        items = items[:4]
    for item in items:
        route = synthesis(item)
        routes.append(route)
    return routes, updowns, its


def synthesis(item):
    urls = item.xpath('./ul/li/p[1]/text()')
    imgs = item.xpath('./ul/li/div/a/img/@src')
    pre = '~'
    # get pre
    for index, url in enumerate(urls):
        if url == '→':
            val = item.xpath('./ul/li[%d]/p[2]/text()' % (index + 1))
            if val:
                pre = val[0]
    str_url = ''.join(urls).split('→')
    fronts = str_url[0].split('+')
    backs = str_url[1].split('+')
    front = []
    back = []
    for index, cas in enumerate(urls[::2]):
        if cas in fronts:
            front.append(dict(cas=cas, url=imgs[index]))
        else:
            back.append(dict(cas=cas, url=imgs[index]))
    return {'front': front, 'back': back, 'pre': pre, 'conditions': ''}


def parse_updownstream(url):
    # num = cas.split('-')[0]
    # num = num[1:] if len(num) > 3 else num
    # url = 'http://data.huaxuejia.cn/html/%s/cas_%s.html'%(num, cas)
    resp = requests.get(url, headers=headers, )
    # resp = requests.get(url, headers=headers)
    eles = etree.HTML(resp.content)
    ups = eles.xpath('//ul[@id="up-list"]/li/p[1]/a/text()')
    downs = eles.xpath('//ul[@id="down-list"]/li/p[1]/a/text()')
    if len(ups) > 3:
        ups = ups[:3]
    if len(downs) > 3:
        downs = downs[:3]
    ups = list(map(lambda x: x.strip(), ups))
    downs = list(map(lambda x: x.strip(), downs))
    return {'ups': ups, 'downs': downs}


def save(item):
    if matcher.match('英文名称', title=item.get('英文名称', '').split(',')[0]).first():
        return
    cats = item['category']
    for c in cats:
        if not matcher.match('category', title=c).first():
            category = Node('category', title=c)
            graph.create(category)

    cas = matcher.match('cas', title=item.get('CAS ', '').split(',')[0]).first()
    if not cas:
        cas = Node('cas', title=item['CAS '])

    graph.create(cas)

    for c in item['category']:
        # node = Node(label='category', title=c)
        rela_cas = build_relationship(cas, 'category', matcher.match('category', title=c).first())
        # graph.create(rela_cas)

    for en_name in item.get('英文名称', '').split(','):
        if en_name:
            node = Node('英文名称', title=en_name)
            graph.create(node)
            rela = build_relationship(cas, '英文名', node)
            # graph.create(rela)

    for cn_name in item.get('中文别名', '').split(';'):
        if cn_name:
            node = Node('中文别名', title=cn_name)
            graph.create(node)
            rela = build_relationship(cas, '中文别名', node)
            # graph.create(rela)

    for cn_name in item.get('英文别名', '').split(';'):
        if cn_name:
            node = Node('英文别名', title=cn_name)
            graph.create(node)
            rela = build_relationship(cas, '英文别名', node)
            # graph.create(rela)
    try:
        del item['item']
        del item['_id']
        del item['CAS ']
        del item['category']
        # del item['英文名称']
        # del item['中文别名']
        # del item['英文别名']
    except:
        pass

    for k, v in item.items():
        if k is not '英文名称' and k is not '中文别名' and k is not '英文别名':
            if k:
                v = v.strip()
                print(k)
                if '：' in k:
                    k = k[:-1]
                if ':' in k:
                    continue
                try:
                    node = Node(k.strip(), title=v)
                    graph.create(node)
                    rela = build_relationship(cas, k.strip(), node)
                    # graph.create(cas | rela | node)
                except:
                    pass
    # 动态加载上下游关系，合成路线
    print('loading rela')
    synt = parse_synthesis(item['CAS号'])
    print(synt)
    updown = parse_updownstream(item['url'])
    print(updown)
    save_synthesis(synt, cas)
    save_updown(updown, cas)


from app.script import import_molbase
def gen_rela(cas):
    # synts, updown, items = parse_synthesis(cas)
    synts, updown = import_molbase(cas)

    print(synts)
    print(updown)
    # print(items)

    build_synt_rela(synts)
    build_updowns_rela(updown, cas)

    # return {'synts': synts, 'updown': updown, 'items': items, 'info': {'cas': cas, 'url': add_img(cas)}}
    return {'synts': synts, 'updown': updown, 'info': {'cas': cas, 'url': add_img(cas)}}


def build_synt_rela(synts):
    for synt in synts:
        label = ':'.join(map(lambda x: x['cas'], synt['front'])) + 'pre' + ':'.join(
            map(lambda x: x['cas'], synt['back']))
        rela = get_Node(label, synt['pre'], conditions=synt['conditions'])
        for front in synt['front']:
            node = get_Node('cas', front['cas'], url=front['url'])
            build_relationship(node, '合成路线', rela)
        for back in synt['back']:
            node = get_Node('cas', back['cas'], url=back['url'])
            build_relationship(rela, '合成路线', node)


def build_updowns_rela(updowns, cas):
    core = get_Node('cas', cas)
    for ups in updowns['ups']:
        node = get_Node('cas', ups['cas'], url=ups['url'])
        build_relationship(node, '上游', core)
    for downs in updowns['downs']:
        node = get_Node('cas', downs['cas'], url=downs['url'])
        build_relationship(node, '下游', core)


def get_Node(label, title, **kwargs):
    """
    with label and title search, if it's not exist will be create node.
    :param label:
    :param title:
    :return:
    """
    node = matcher.match(label, title=title, **kwargs).first()
    if not node:
        node = Node(label, title=title, **kwargs)
        graph.create(node)
    return node


def build_relationship(node, label, n):
    if not rela_matcher.match([node, n], label).first():
        rela_cas = Relationship(node, label, n)
        rel = node | n | rela_cas
        graph.create(rel)


def save_synthesis(synts, cas):
    for item in synts:
        handle_synthesis(item, cas)


def handle_synthesis(item, cas):
    pre = item[-1]
    print(''.join(item[:-1]))
    syn = ''.join(item[:-1]).split('→')
    front = syn[0].split('+')
    back = syn[1].split('+')
    rela_node = Node('→', title=pre)
    graph.create(rela_node)
    for f in front:
        node = get_Node('cas', f)
        build_relationship(node, '构成', rela_node)
    for b in back:
        node1 = get_Node('cas', b)
        build_relationship(rela_node, '转化', node1)
    # build_relationship(rela_node, )
    return front, back


def save_updown(updowns, cas):
    ups = updowns['ups']
    downs = updowns['downs']
    for up in ups:
        node = get_Node('cas', up)
        build_relationship(node, '上游', cas)
    for down in downs:
        node = get_Node('cas', down)
        build_relationship(node, '下游', cas)


def add_img(cas):
    imgs = set_imgs(cas)
    url = imgs[0]
    resp = requests.head(url, headers=headers)

    if resp.status_code == 200:
        return url
    if requests.head(imgs[1], headers=headers).status_code == 200:
        return url
    return ''


def relactionship_search(cas1, cas2, rela, level):
    cql = "match data=(na:cas{title:'%s'})-[:%s*1..%s]->(nb:cas{title:'%s'}) return data" % (cas1, rela, level, cas2)
    print(cql)
    resp = graph.run(cql)
    if len(resp.data()) < 1:
        cql = "match data=(na:cas{title:'%s'})-[:%s*1..%s]->(nb:cas{title:'%s'}) return data" % (
            cas2, rela, level, cas1)
    # nodes = []
    # links = []
    # keys = []
    resp = graph.run(cql)
    paths = []
    for index, r in enumerate(resp):
        path = tranform_rela_node(r, rela)
        paths.append(path)
        # subgraph = r.to_subgraph()
        # tranform_keys_node(subgraph.start_node, keys, nodes, links)
        # tranform_keys_node(subgraph.end_node, keys, nodes, links)
        # for count, link in enumerate(subgraph.relationships):
        #     for node in link.nodes:
        #         tranform_keys_node(node, keys, nodes, links)
        #     source = link.nodes[0]
        #     target = link.nodes[1]
        #     links.append({
        #         'source': source.get('title', '') if source.get('url', '') else str(source.labels),
        #         'target': target.get('title', '') if target.get('url', '') else str(target.labels),
        #         'value': rela,
        #         'name': rela,
        #         'lineStyle':
        #             {'normal': {}}
        #     })
    # return {'nodes': nodes, "links": links, 'type': rela}
    return paths


def tranform_keys_node(node, keys, nodes, links):
    title = node.get('title', '')
    url = node.get('url', '')
    conditions = node.get('conditions', '')
    flag = title if url else str(node.labels)
    if not url and str(node.labels) == ':cas':
        return
    if flag not in keys:
        keys.append(flag)
        nodes.append({
            'id': flag,
            'name': flag,
            'symbol': "image://" + url if url else "diamond",
            'type': 'entity' if url else 'virtual',
            # 'symbolSize': 30 if url else 15,
            # 'label': {'normal': {'show': True if url else False}},
            'value': title,
            'conditions': conditions if conditions else '',
        })


def load_rela_data(keys, nodes, links):
    for key in keys:
        if len(key.split('pre'))>1:
            flag = key
            front, back = flag[2:-1].split('pre')
            front = front.split(':')
            back = back.split(':')
            print(front)
            print(back)
            for f in front:
                nd = get_Node('cas', f)
                if nd.get('title') not in keys:
                    nodes.append({
                        'id': nd.get('title'),
                        'name': nd.get('title'),
                        'symbol': "image://" + nd.get('url'),
                        # 'symbolSize': 30,
                        # 'label': {'normal': {'show': True}},
                        'value': nd.get('title'),
                        # 'conditions': nd.get('conditions')
                    })
                    links.append({
                        'source': nd.get('title'),
                        'target': flag,
                        'value': "合成路线",
                        'name': "合成路线",
                        # 'lineStyle':
                        #     {'normal': {}}
                    })
            for f in back:
                nd = get_Node('cas', f)
                if nd.get('title') not in keys:
                    nodes.append({
                        'id': nd.get('title'),
                        'name': nd.get('title'),
                        'symbol': "image://" + nd.get('url'),
                        # 'symbolSize': 30,
                        # 'label': {'normal': {'show': True}},
                        'value': nd.get('title')
                    })
                    links.append({
                        'source': flag,
                        'target': nd.get('title'),
                        'value': "合成路线",
                        'name': "合成路线",
                        # 'lineStyle':
                        #     {'normal': {}}
                    })

def tranform_rela_node(r, rela):
    subgraph = r.to_subgraph()
    nodes = []
    links = []
    keys = []
    links_keys = []
    tranform_keys_node(subgraph.start_node, keys, nodes, links)
    tranform_keys_node(subgraph.end_node, keys, nodes, links)
    for count, link in enumerate(subgraph.relationships):
        for node in link.nodes:
            tranform_keys_node(node, keys, nodes, links)
        source = link.nodes[0]
        target = link.nodes[1]
        links.append({
            'source': source.get('title', '') if source.get('url', '') else str(source.labels),
            'target': target.get('title', '') if target.get('url', '') else str(target.labels),
            'value': rela,
            'name': rela,
            'lineStyle':
                {'normal': {}}
        })
    load_rela_data(keys, nodes, links)
    return {'nodes': nodes, "links": links, 'type': rela}


def func_search_new(keyword):
    # url = "http://news.baidu.com/ns?rn=11&ie=utf-8&tn=newstitle&word{}".format(keyword)
    url = "http://news.baidu.com/ns?ie=utf-8&cl=2&ct=1&bs=intitle%3A%28%E8%8B%AF%29&rsv_bp=1&sr=0&f=8&prevct=no&tn=newstitle&word={}".format(keyword)
    html = requests.get(url, headers=headers).content.decode()
    etree_html = etree.HTML(html)
    all_news_data = etree_html.xpath('//*[@class="result title"]')
    new_list = []
    if len(all_news_data) > 0:
        for i in all_news_data:
            per_dict = {}
            per_dict['title'] = i.xpath('./h3/a')[0].xpath('string(.)').replace('\n', '').strip()
            per_dict['link'] = i.xpath('./h3/a/@href')[0]
            per_dict['source_web'] = i.xpath('./div[@class="c-title-author"]/text()')[0]
            new_list.append(per_dict)
    return {'data': new_list}


# 文献检索
from KnowledgeGraph.settings import IP_LIST


def get_wx(cas, page=None):
    url = str('https://www.chemsrc.com/PaperResult/{}/'.format(str(cas)))
    if page:
        url = url + '?page={}'.format(str(page))

    proxy_ip = '213.23.122.170:443'
    res_status = False
    while not res_status:
        try:
            request_doc = requests.get(url, headers=headers, proxies={'https': proxy_ip, 'http': proxy_ip})
            res_status = True
        except Exception as e:
            print(str(e))
            print('proxy_ip = ' + str(proxy_ip))
            proxy_ip = random.choice(IP_LIST)

    if request_doc.status_code == 200:
        html_doc = request_doc.content.decode()

        # with open('123.html', 'w', encoding='utf-8')as f:
        #     f.write(html_doc)

        xpath_doc = etree.HTML(html_doc)
        info_times = xpath_doc.xpath('//*[@id="idxTbl"]/tr')

        j = 1
        docInfo = []
        for i in info_times:
            info = {}
            e = xpath_doc.xpath('//*[@id="idxTbl"]/tr[{}]/td/a'.format(str(j)))
            info['herf'] = 'https://www.chemsrc.com/' + e[0].attrib['href']
            info['title'] = e[0].text
            info['author'] = xpath_doc.xpath('//*[@id="idxTbl"]/tr[{}]/td/p[1]'.format(str(j)))[0].text
            info['periodical'] = xpath_doc.xpath('//*[@id="idxTbl"]/tr[{}]/td/p[2]'.format(str(j)))[0].text
            info['abstract'] = xpath_doc.xpath('//*[@id="idxTbl"]/tr[{}]/td/p[3]/i'.format(str(j)))[0].text
            if info['abstract'] == None:
                info['abstract'] = ''
            if info['author'] == None:
                info['author'] = ''
            if info['title'] == None:
                info['title'] = ''
            docInfo.append(info)
            j = j + 1
        return docInfo
    else:
        return request_doc.status_code






if __name__ == '__main__':
    # graph.delete_all()
    # a = parse_synthesis('765-43-5')
    # print(a)
    # print(parse_updownstream('http://baike.molbase.cn/cidian/340'))
    print(gen_rela('947-42-2'))
    # a = relactionship_search('100-59-4', '149-74-6', '合成路线', '3')
    # import json
    #
    # print(json.dumps(a))
