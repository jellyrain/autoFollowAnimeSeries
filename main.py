import multiprocessing
import os

import requests

from src.proxy.ShadowsocksR.proxy import start, get_proxys, is_valid_connect


def job():
    os.system(
        'ShadowsocksR.exe -s mysql.accessconnect.cc -p 6001 -k di15PV -m rc4-md5 -t 120 -O auth_aes128_md5 -G 264021:IlDiOH -o tls1.2_ticket_auth -g 5d0a6264021.www.gov.hk  -b 127.0.0.1 -l 3060 -u 0')


if __name__ == '__main__':
    print(is_valid_connect('mysql.accessconnect.cc', 6001))

    # multiprocessing.freeze_support()

    # url = 'https://mikanani.me/RSS/Bangumi'
    # #
    # # id = '645a5135c5e541330cf40032'
    # #
    # # data = get_ssr_by_id(id)
    # #
    # p = multiprocessing.Process(target=job)
    # #
    # p.start()
    # print(requests.get(url, proxies=get_proxys(local_port=3060), headers={
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    # }, params={
    #     'bangumiId': 2793,
    #     'subgroupid': 53
    # }).text)
    #
    # p.terminate()
