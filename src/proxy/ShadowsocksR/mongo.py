from bson import ObjectId

from src.dbConnent.mongoDB import MongoDB
from src.proxy.ShadowsocksR.parse import parse_subscribe


def get_db():
    # 获取 MongoDB 数据库连接
    return MongoDB('10.0.0.7', 27017, 'ssrData')


def parse_to_mongo(subscribe_url: str) -> None:
    # 解析订阅链接并存入 MongoDB
    db = get_db()
    for item in parse_subscribe(subscribe_url):
        db.insert_one('ssrNode', item)
    db.close()


def get_ssr_list() -> list[dict[str, str]]:
    # 获取 ssr 节点列表
    db = get_db()
    return list(
        map(lambda x: {'id': str(x['_id']), 'remarks': x['remarks']}, db.find('ssrNode', {}, {'_id': 1, 'remarks': 1})))


def get_ssr_by_id(_id: str) -> dict[str, str]:
    # 根据 id 获取 ssr 节点
    db = get_db()
    return db.find_one('ssrNode', {'_id': ObjectId(_id)})


__all__ = ['parse_to_mongo', 'get_ssr_list', 'get_ssr_by_id']
