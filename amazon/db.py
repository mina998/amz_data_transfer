import sqlite3
from os import sep, path

SQLITE_DB_URI = '%sdata.db'% (sep.join(path.dirname(path.realpath(__file__)).split(sep)[:-1])+sep)


class Db(object):
    __instance = None
    sqlite_uri = SQLITE_DB_URI

    def execute(self,sql):
        """
        执行SQL语句
        :param sql:
        :return:
        """
        try: return self.__cur.execute(sql)
        except Exception as e:  print(e)

    def commit(self):
        self.__con.commit()


    def close(self):
        self.__con.close()


    def __new__(cls, *args, **kwargs):
        """
        单例模式
        :param args:
        :param kwargs:
        :return:
        """
        if cls.__instance == None:
            cls.__con = sqlite3.connect(cls.sqlite_uri, timeout=60)
            cls.__cur = cls.__con.cursor()
            cls.__instance = object.__new__(cls)
        return cls.__instance

sqlite = Db()