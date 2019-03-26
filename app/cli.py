from haipproxy.client.py_cli import ProxyFetcher
import logging
from requests.exceptions import ReadTimeout, \
    ProxyError, ConnectTimeout, TooManyRedirects, ConnectionError
from urllib3.exceptions import MaxRetryError
import os
from redis import StrictRedis

# def get_log(chart):
#     logger = logging.getLogger(chart)
#     logger.setLevel(level=logging.INFO)
#     handler = logging.FileHandler("log_%s.log" % chart)
#     handler.setLevel(logging.INFO)
#     # handler.setLevel(logging.ERROR)
#     # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     return logger

# log = get_log('proxy')
# err_log = get_log('err_log')
# log_time = get_log('time')
# log_url = get_log('urls')

from .setting import redis_address

import requests

args = dict(host=redis_address, port=6379, password='yunshuadmin', db=0)
args1 = dict(host=redis_address, port=6379, password='yunshuadmin', db=1)
args2 = dict(host=redis_address, port=6379, password='yunshuadmin', db=2)

usedConn = StrictRedis(**args1)
# badConn = StrictRedis(**args2)
# badConn.flushdb()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    'Host': 'baike.molbase.cn',
    # 'Sec-Metadata': 'cause="forced", destination="document", target="top-level", site="same-origin"',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
}

import random

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
]


class Proxy:

    def __init__(self):
        self.fetcher = ProxyFetcher('https', strategy='greedy', redis_args=args)
        self.pools = self.fetcher.pool
        self.used = 1
        # self.usedConn = StrictRedis(**args)

    def get_ip(self):
        self.used += 1
        # log.info("pid: {} , used: {}, length: {}, ***** {} %".format(os.getpid(), self.used, len(self.pools),
        #                                                              self.used / (len(self.pools) + 1) * 100))
        if self.used > len(self.pools) / 3:
            # self.fetcher = ProxyFetcher('http', strategy='greedy', redis_args=args)
            self.pools = self.fetcher.get_available_proxies(self.fetcher.conn)
            self.used = 0
            # log.info("""
            #         ******************************
            #         ******    {}    use   ********
            #         ******************************
            #         """.format(str(len(self.pools))))
        return random.choice(self.pools)
        # use = self.usedConn.srandmember('haipproxy:all').decode()
        # log.info(use)
        # return use

    def remove(self, url):
        self.fetcher.delete_proxy(url)
        self.pools.remove(url)


proxy = ''

from lxml import etree
from datetime import datetime





def check(content, url):
    if url.find('sds') > 0:
        return True
    # try:
    #     eles = etree.HTML(content)
    #     keys = eles.xpath('//div[@class="product clearfix"]/dl/dd/table/tbody/tr/th/text()')
    #     keys = [key[:-1] for key in keys]
    #     vals = eles.xpath('//div[@class="product clearfix"]/dl/dd/table/tbody/tr/td')
    #     vals = [ele.xpath('string(.)') for ele in vals]
    #     dt = dict(zip(keys, vals))
    #     if dt['分子式 ']:
    #         return True
    #     bads(url, content)
    # except:
    #     bads(url, content)
    #     return False
    return True


def get_data(url):
    global proxy
    if not proxy:
        proxy = Proxy()
    success = True
    retry = 2
    ips = proxy.get_ip()
    # log_url.info(url)
    while success:
        try:
            retry -= 1
            # time.sleep(3)
            headers['User-Agent'] = random.choice(USER_AGENTS)
            start = time.time()
            resp = requests.get(url, headers=headers, proxies={'http': ips}, timeout=15, allow_redirects=False)
            # resp = requests.get(url, headers=headers, timeout=6)
            if not ips:
                continue
            if resp.status_code == 200:
                # nerr = check(resp.content.decode(), url)
                usedConn.sadd('useful', ips)
                end = time.time()
                # log_time.info('         * {} *     {}    '.format(str(end - start), ips))
                # usedConn.delete(url)
                return resp

            # print(resp.status_code)
            usedConn.sadd('bads', ips)
            # err_log.info(resp.status_code)
            # err_log.info(resp.url)
            # log.info(resp.status_code)
            # if retry < 0:
            ips = proxy.get_ip()
        # except ReadTimeout:
        #     print('timeout')
        except (MaxRetryError, ProxyError, TooManyRedirects, ConnectionError):
            # proxy.remove(ips)
            # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
            ips = proxy.get_ip()
        except:
            # print(e)
            # log.exception(e)
            # log.info(ips)
            if retry < 0:
                # proxy.remove(ips)
                # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = proxy.get_ip()


# class UseProxy:
#
#     def __init__(self):
#         self.pools = list(usedConn.smembers('useful'))
#         self.used = 1
#
#
#
#     def get_ips(self):
#         self.used += 1
#         log.info("pid: {} , used: {}, length: {}, ***** {} %".format(os.getpid(), self.used, len(self.pools),
#                                                                      self.used / (len(self.pools) + 1) * 100))
#         if self.used > len(self.pools) / 3:
#             # self.fetcher = ProxyFetcher('http', strategy='greedy', redis_args=args)
#             self.pools = list(usedConn.smembers('useful'))
#             self.used = 0
#             log.info("""
#                     ******************************
#                     ******    {}          ********
#                     ******************************
#                     """.format(str(len(self.pools))))
#         return random.choice(self.pools).decode()
#         # use = self.usedConn.srandmember('haipproxy:all').decode()
#         # log.info(use)
#         # return use
#
# useProxy = UseProxy()

def get_ips():
    ips = usedConn.srandmember('useful')
    if ips:
        return ips.decode()


def get_use_data(url):
    success = True
    retry = 2
    ips = get_ips()
    # log_url.info(url)
    while success:
        try:
            retry -= 1
            # time.sleep(3)
            if not ips:
                time.sleep(5)
                continue
            # time.sleep(1)
            headers['User-Agent'] = random.choice(USER_AGENTS)
            start = time.time()
            resp = requests.get(url, headers=headers, proxies={'http': ips}, timeout=15, allow_redirects=False)
            # resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 200:
                # nerr = check(resp.content.decode(), url)
                # if nerr:
                #     # usedConn.delete(url)
                end = time.time()
                # log_time.info('         * {} *     {}    '.format(str(end - start), ips))
                if (end - start) < 5:
                    # pass
                    usedConn.sadd('ttl', ips)
                return resp
            usedConn.sadd('bads', ips)
            # err_log.info(resp.status_code)
            # err_log.info(resp.url)
            print(resp.status_code)
            # log.info(resp.status_code)
            # if retry < 0:
            if retry < 0:
                if ips:
                    usedConn.srem('useful', ips)
                # log.info("^^^^^  remove {} +++++{}++++".format(ips, url))
                ips = get_ips()
        # except ReadTimeout:
        #     print('timeout')
        except (MaxRetryError, ProxyError, TooManyRedirects, ConnectionError):
            if retry < 0:
                if ips:
                    usedConn.srem('useful', ips)
                # log.info("====  remove {} ===={}====".format(ips, url))
                ips = get_ips()
        except:
            # print(e)
            # log.exception(e)
            # log.info(ips)
            # if retry < 0:
            if retry < 0:
                if ips:
                    usedConn.srem('useful', ips)
                # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = get_ips()


def get_data_header(url, headers):
    global proxy
    if not proxy:
        proxy = Proxy()
    success = True
    retry = 2
    ips = proxy.get_ip()
    # log_url.info(url)
    while success:
        try:
            retry -= 1
            # time.sleep(3)
            headers['User-Agent'] = random.choice(USER_AGENTS)
            resp = requests.get(url, headers=headers, proxies={'http': ips}, timeout=15, allow_redirects=False)
            # resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 302:
                # nerr = check(resp.content.decode(), url)
                # usedConn.sadd('useful', ips)
                # usedConn.delete(url)
                return resp
                # else:
                #     proxy.remove(ips)
                #     log.info("^^{}^^^  remove {} +++++{}++++".format(os.getpid(), ips, url))
                #     ips = proxy.get_ip()
            usedConn.sadd('bads', ips)
            if resp.status_code == 200:
                return
            else:
                pass
                # err_log.info(resp.status_code)
                # err_log.info(resp.url)
            print(resp.status_code)
            # log.info(resp.status_code)
            if retry < 0:
                ips = get_ips()
        # except ReadTimeout:
        #     print('timeout')
        except (MaxRetryError, ProxyError, TooManyRedirects, ConnectionError):
            if retry < 0:
                # proxy.remove(ips)
                # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = get_ips()
        except:
            # print(e)
            # log.exception(e)
            # log.info(ips)
            if retry < 0:
                # proxy.remove(ips)
                # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = get_ips()


import time


def get_c_data_header(url, headers):
    success = True
    while success:
        try:
            time.sleep(3)
            resp = requests.get(url, headers=headers, proxies={'http': '222.186.44.10:4321'}, timeout=15,
                                allow_redirects=False)
            if resp.status_code == 302:
                return resp
            if resp.status_code == 200:
                return
            else:
                pass
                # err_log.info(resp.status_code)
                # err_log.info(resp.url)
            # print(resp.status_code)
            # log.info(resp.status_code)
        except Exception as e:
            pass
            # log.exception(e)
            # log.info('222.186.44.10:4321+++++++++except')


def get_c_data(url):
    success = True
    while success:
        try:
            time.sleep(1)
            resp = requests.get(url, headers=headers, proxies={'http': '222.186.44.10:4321'}, timeout=15,
                                allow_redirects=False)
            if resp.status_code == 200:
                return resp
            else:
                pass
                # log.info('222.186.44.10:4321*** status{}'.format(resp.status_code))
        except Exception as e:
            pass
            # log.exception(e)
            # log.info('222.186.44.10:4321+++++++++except')


import hashlib

app_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WoW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Content-Length': '34',
    'Accept-Encoding': 'gzip',
    'Host': 'zh.molbase.com',
    'Cookie': 'my_mbcookie=8877784019; ECM_ID=20nloqkhc5a1clor40tv72mv54; ECM_ID=20nloqkhc5a1clor40tv72mv54',
    'Connection': 'keep-alive',
}


def main():
    params = 'hdkCMA!qxH8Qv&IVZHEn2ar#oqCW!%mM'
    l = str(time.time()).split('.')[0]
    md5 = hashlib.md5()
    md5.update((params + l).encode())
    return md5.hexdigest().upper() + l


types = ['result_21', 'basic', 'physical',
         'secure', 'toxic', 'customs',
         'synthetic', 'msds', 'stream', ]


def get_app_data(url, data):
    global proxy
    if not proxy:
        proxy = Proxy()
    success = True
    retry = 3
    ips = proxy.get_ip()
    # log_url.info(url)
    while success:
        try:
            retry -= 1
            resp = requests.post(url, headers=app_header, proxies={'http': ips}, data=data,
                                 timeout=15, allow_redirects=False)
            if resp.status_code == 200:
                usedConn.sadd('useful', ips)
                return resp
            usedConn.sadd('bads', ips)
            # err_log.info(resp.status_code)
            # err_log.info(resp.url)
            # log.info(resp.status_code)
            # if retry < 0:
            ips = proxy.get_ip()
        # except ReadTimeout:
        #     print('timeout')
        # except (MaxRetryError, ProxyError,
        #         ConnectTimeout, TooManyRedirects, ConnectionError):
        #     # proxy.remove(ips)
        #     # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
        #     ips = proxy.get_ip()
        except Exception as e:
            # print(e)
            # err_log.exception(e)
            # log.info(ips)
            if retry < 0:
                # proxy.remove(ips)
                # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = proxy.get_ip()


def get_app_use_data(url, data):
    success = True
    retry = 3
    ips = get_ips()
    # log_url.info(url)
    while success:
        try:
            retry -= 1
            if not ips:
                time.sleep(20)
                continue
            resp = requests.post(url, headers=app_header, proxies={'http': ips}, data=data,
                                 timeout=15, allow_redirects=False)
            # resp = requests.get(url, headers=headers, timeout=6)
            if resp.status_code == 200:
                return resp

            usedConn.sadd('bads', ips)
            # err_log.info(resp.status_code)
            # err_log.info(resp.url)
            # print(resp.status_code)
            # log.info(resp.status_code)
            # if retry < 0:
            if retry < 0:
                usedConn.srem('useful', ips)
                # log.info("^^^^^  remove {} +++++{}++++".format(ips, url))
                ips = get_ips()
        # except ReadTimeout:
        #     print('timeout')
        # except (MaxRetryError, ProxyError,
        #         ConnectTimeout, TooManyRedirects, ConnectionError):
        #     if retry < 0:
        #         usedConn.srem('useful', ips)
        #         log.info("====  remove {} ===={}====".format(ips, url))
        #         ips = get_ips()
        except Exception as e:
            # err_log.exception(e)
            # print(e)
            # log.exception(e)
            # log.info(ips)
            # if retry < 0:
            if retry < 0:
                usedConn.srem('useful', ips)
                # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = get_ips()



json_header = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://m.molbase.cn/baike/27620',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}


def get_tag_data(url):
    global proxy
    if not proxy:
        proxy = Proxy()
    success = True
    retry = 2
    ips = proxy.get_ip()
    while success:
        try:
            retry -= 1
            # headers['User-Agent'] = random.choice(USER_AGENTS)
            start = time.time()
            resp = requests.get(url, headers=json_header, proxies={'http': ips}, timeout=15, allow_redirects=False)
            if not ips:
                continue
            if resp.status_code == 200:
                usedConn.sadd('useful', ips)
                end = time.time()
                # log_time.info('         * {} *     {}    '.format(str(end - start), ips))
                return resp

            usedConn.sadd('bads', ips)
            # err_log.info(resp.status_code)
            # err_log.info(resp.url)
            # log.info(resp.status_code)
            ips = proxy.get_ip()
        except (MaxRetryError, ProxyError, TooManyRedirects, ConnectionError):
            ips = proxy.get_ip()
        except:
            if retry < 0:
                ips = proxy.get_ip()

def get_use_tag_data(url):
    success = True
    retry = 2
    ips = get_ips()
    while success:
        try:
            retry -= 1
            if not ips:
                time.sleep(5)
                continue
            headers['User-Agent'] = random.choice(USER_AGENTS)
            start = time.time()
            resp = requests.get(url, headers=json_header, proxies={'http': ips}, timeout=15, allow_redirects=False)
            if resp.status_code == 200:
                end = time.time()
                # log_time.info('         * {} *     {}    '.format(str(end - start), ips))
                if (end - start) < 5:
                    # pass
                    usedConn.sadd('ttl', ips)
                return resp
            usedConn.sadd('bads', ips)
            # err_log.info(resp.status_code)
            # err_log.info(resp.url)
            print(resp.status_code)
            # log.info(resp.status_code)
            if retry < 0:
                if ips:
                    usedConn.srem('useful', ips)
                # log.info("^^^^^  remove {} +++++{}++++".format(ips, url))
                ips = get_ips()
        except (MaxRetryError, ProxyError, TooManyRedirects, ConnectionError):
            if retry < 0:
                if ips:
                    usedConn.srem('useful', ips)
                # log.info("====  remove {} ===={}====".format(ips, url))
                ips = get_ips()
        except:
            if retry < 0:
                if ips:
                    usedConn.srem('useful', ips)
                # log.info("++{}++  remove {} +++++{}++++".format(os.getpid(), ips, url))
                ips = get_ips()




if __name__ == '__main__':
    # import sentry_sdk
    #     # sentry_sdk.init("https://34a7992a425e4144a9f4f1eadd193278@sentry.io/1355103")
    #     # from db import get_urls
    #     # urls = get_urls().find()[60000:60010]
    #     # for url in urls:
    #     #     print(get_data(url['url']).text)
    #     # try:
    #     #     requests.get("djjjkks")
    #     # except:
    #     #     pass
    # resp = get_data('http://baike.molbase.cn/cidian/35609?search_keyword=67287-36-9&page=1&per_page=10')
    # print(resp.status_code)
    print(main())
