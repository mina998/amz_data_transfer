from multiprocessing import Process
from random import choice
from amazon.goods import Goods
from amazon.cookies import Cookies
from helper.tools import Tools as tools
from web.app import app
# 美国城市邮编
zips = [90017]
debug = True  #

class Main(object):
    #
    def cookies(self):
        while True:
            tools.sleep(5)
            obj = Cookies(zip=choice(zips), debug=debug)
            obj.get()


    def goods(self):
        n = 1 #计数
        i = [6,9,20,11,15] # 为求随机
        api = 'http://127.0.0.1:1015/get?m=mina998'
        api = 'http://198.35.45.110:1015/get?m=mina998'
        obj = Goods(debug=debug, proxy_api=api)
        while True:
            if n % choice(i) == 0: is_proxy = False
            else: is_proxy = True
            # 下次运行时间(秒)
            if debug: exe = 600
            else: exe = tools.next_time_stamp() - tools.time_stamp_now(True)
            if obj.get(is_proxy) == 'ok': tools.sleep(exe)
            n += 1

    def web(self):
        app.run(host='0.0.0.0',port=5000)

    def run(self):
        web = Process(target=self.web)
        web.start()

        cookies = Process(target=self.cookies)
        cookies.start()

        goods = Process(target=self.goods)
        tools.sleep(60*5) #等侍5分钟后启动 这几分钟可添加数据
        goods.start()


if __name__ == '__main__':
    Main().run()
