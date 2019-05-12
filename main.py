from multiprocessing import Process
from random import choice
from amazon.goods import Goods
from amazon.cookies import Cookies
from helper.tools import Tools as tools
from web.app import app
# 美国城市邮编
zips = [90017]
# zips = [
#     35201, 35238, 35240, 35242, 35246, 35249, 35253, 35255, 35259, 35261, 35263, 35266, 35277, 35283, 35285, 35299,
#     36101, 36125, 36130, 36135, 36140, 36142, 36177, 36191, 90001, 90068, 90070, 90084, 90086, 90097, 90099, 90101,
#     90103, 90174, 90185, 90189, 39201, 39207, 39209, 39213, 39215, 39217, 39225, 39235, 39236, 39250, 39269, 39271,
#     39282, 39284, 39286, 39289, 39296, 39298, 43085, 43201, 43224, 43226, 43232, 43234, 43235, 43236, 43240, 43251,
#     43260, 43265, 43266, 43268, 43271, 43272, 43279, 43287, 43291, 43299, 10001, 10041, 10043, 10048, 10055, 10060,
#     10069, 10072, 10079, 10082, 10087, 10090, 10094, 10096, 10098, 10099, 10101, 10126, 10128, 10133, 10138, 10149,
#     10179, 10184, 10185, 10196, 10197, 10199, 10203, 10211, 10213, 10242, 10249, 10256, 10261, 10265, 10268, 10282,
#     10285, 10286, 10292, 14602, 14627, 14638, 14639, 14642, 14647, 14649, 14653, 14664, 14673, 14683, 14692, 14694,
#     14201, 14228, 14231, 14233, 14240, 14241, 14260, 14261, 14263, 14265, 14267, 14269, 14270, 14272, 14273, 14276,
#     14280, 87101, 87116, 87118, 87123, 87125, 87131, 87151, 87153, 87154, 87158, 87176, 87181, 87184, 87185, 87187,
#     87190, 87199, 87500, 87509, 87592, 87594
# ]

# 不重要日志禁输出
# 不显示成功日志
log = True

class Main(object):
    #
    def cookies(self):
        while True:
            tools.sleep(1)
            obj = Cookies(zip=choice(zips), log_show=log)
            obj.get()
            if obj.tongji > 300: tools.sleep(600)

    def goods(self):
        n = 1 #计数
        i = [6,9,20,11,15] # 为求随机
        api = 'http://127.0.0.1:1015/get?m=mina998'
        obj = Goods(log_show=log, proxy_api=api)
        while True:
            if n % choice(i) == 0: is_proxy = False
            else: is_proxy = True
            # 下次运行时间(秒)
            if log: exe = 600
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
    a = Main()
    a.run()
