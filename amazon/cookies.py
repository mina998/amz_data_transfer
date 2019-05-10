import json
from random import choice
from urllib.parse import quote
from amazon.db import sqlite
from helper.tools import Tools as tools
from helper.http import Http

class Cookies(Http):
    def __init__(self, zip=10001, log_show=False):
        """
        zip 城市邮编
        :param zip:
        """
        super().__init__()
        self.__zip_code = zip
        self.__log_show = log_show

    def __token_get(self):
        # 获取首页cookies
        urls = [
            'https://www.amazon.com/gp/goldbox?ref_=nav_cs_gb_azl',
            'https://www.amazon.com/b/ref=gc_surl_giftcards?node=2238192011',
            'https://www.amazon.com/ref=nav_logo',
            'https://www.amazon.com/gp/help/customer/display.html?nodeId=508510&ref_=nav_cs_help'
            'https://www.amazon.com/b/?_encoding=UTF8&ld=AZUSSOA-sell&node=12766669011&ref_=nav_cs_sell',
            'https://www.amazon.com/Outlet/b/?ie=UTF8&node=517808&ref_=sv_subnav_goldbox_3'
        ]
        url = choice(urls)
        self.request(url=url)
        tools.sleep(3)
        self.__change_cidy()
        if not self.session.cookies.get('ubid-main'):
            self.logger.warning('[%s][%s] Token Failed: %s'% (tools.current_time(), self.__zip_code, url))
            return None
        # 显示成功日志
        if self.__log_show: self.logger.warning('[%s]: Token Success.'%tools.current_time())

        cookies = self.session.cookies
        cookies = self.dict_from_cookiejar(cookies)
        return cookies



    def __change_cidy(self):
        url = 'https://www.amazon.com/gp/delivery/ajax/address-change.html'
        # 获取此页面设置的必要cookies
        data = {
            'locationType': 'LOCATION_INPUT',
            'zipCode': self.__zip_code,
            'storeContext': 'generic',
            'deviceType': 'web',
            'pageType': 'Gateway',
            'actionSource': 'glow'
        }
        self.request(method='POST', url=url, data=data)


    def get(self):
        # 统计Cookie获取数量
        tongji = sqlite.execute('select count(*) from cookies').fetchone()
        self.tongji = tongji[0] if tongji else 0
        # 获取Cooklie
        cookies = self.__token_get()
        if cookies is None: return False
        # 保存Cookie
        cookies = quote(json.dumps(cookies))
        sqlite.execute('INSERT INTO cookies (row) VALUES ("%s")' %cookies)
        sqlite.commit()

if __name__ == '__main__':

    Cookies().get()
