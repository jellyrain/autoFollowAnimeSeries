from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDB:
    # MongoDB数据库连接操作类
    def __init__(self, host: str, port: int, dbName: str, username: str = None, password: str = None) -> None:
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__dbName = dbName
        self.__client = MongoClient(self.__get_url())
        self.__db = self.__client[self.__dbName]

    def __get_url(self) -> str:
        # 获取连接字符串
        mongodb_url = 'mongodb://'
        if self.__username is not None and self.__password is not None:
            mongodb_url += self.__username + ':' + self.__password + '@'
        mongodb_url += self.__host + ':' + str(self.__port)
        return mongodb_url

    def get_collection(self, collectionName: str) -> Collection:
        # 获取集合对象
        return self.__db[collectionName]

    def create_collection(self, collectionName: str) -> Collection:
        # 创建集合
        return self.__db.create_collection(collectionName)

    def drop_collection(self, collectionName: str) -> None:
        # 删除集合
        self.__db.drop_collection(collectionName)

    def close(self) -> None:
        # 关闭数据库连接
        self.__client.close()

    def find_one(self, collectionName: str, filter: dict = None, projection: dict = None) -> dict:
        # 查询单条数据
        return self.get_collection(collectionName).find_one(filter, projection)

    def find(self, collectionName: str, filter: dict = None, projection: dict = None) -> dict:
        # 查询多条数据
        return self.get_collection(collectionName).find(filter, projection)

    def insert_one(self, collectionName: str, document: dict) -> None:
        # 插入单条数据
        self.get_collection(collectionName).insert_one(document)

    def insert_many(self, collectionName: str, documents: list) -> None:
        # 插入多条数据
        self.get_collection(collectionName).insert_many(documents)

    def update_one(self, collectionName: str, filter: dict, update: dict) -> None:
        # 更新单条数据
        self.get_collection(collectionName).update_one(filter, update)

    def update_many(self, collectionName: str, filter: dict, update: dict) -> None:
        # 更新多条数据
        self.get_collection(collectionName).update_many(filter, update)

    def delete_one(self, collectionName: str, filter: dict) -> None:
        # 删除单条数据
        self.get_collection(collectionName).delete_one(filter)

    def delete_many(self, collectionName: str, filter: dict) -> None:
        # 删除多条数据
        self.get_collection(collectionName).delete_many(filter)

    def count_documents(self, collectionName: str, filter: dict = None) -> int:
        # 统计数据条数
        return self.get_collection(collectionName).count_documents(filter)

    def aggregate(self, collectionName: str, pipeline: list) -> dict:
        # 聚合查询
        return self.get_collection(collectionName).aggregate(pipeline)


__all__ = ['MongoDB']
