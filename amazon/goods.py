import json
from helper.http import Http
from urllib.parse import unquote
from helper.tools import Tools as tools
from amazon.db import sqlite


class Goods(Http):

    def __init__(self, log_show=False, proxy_api=None):
        super().__init__()
        self.__exe_next_time = 0
        self.__log_show = log_show
        self.__proxy_api = proxy_api

    def get(self, is_proxy=False):
        self.__is_proxy = is_proxy
        # 1. 获取Asin
        if not self.__asin_get(): return 'ok'
        # 2. 更新Cookie
        if not self.__cookies_up(): return False
        # 3. 获取页面数据
        info = self.__info_get()
        if not info: return False
        # 4. 更新数据库
        insert = "insert into marks (bsr,price,stock,asin_id,uptime) values ('{bsr}','{price}','{stock}','{aid}','{uptime}')".format(**info)
        update = 'update listing set status=1,img="{img}" where asin="{asin}"'.format(img=info['img'], asin=self.__asin)
        delete = 'delete from cookies where id = %s' % self.__token_id

        sqlite.execute(insert)
        sqlite.execute(update)
        sqlite.execute(delete)
        sqlite.commit()

    def __asin_get(self):
        """
        获取Listing信息
        :return:
        """
        row = sqlite.execute('select id,asin,seller from listing where status =0 order by random() limit 5').fetchone()

        if row:
            self.__aid = row[0]
            self.__asin = row[1]
            self.__seller = row[2]
            return True
        self.logger.warning('[%s]: 本轮完成.等待中......' % tools.current_time())
        self.__status_up()
        return False


    def __cookies_up(self):
        """
        更新Cookies
        :return:
        """
        token = sqlite.execute('select id,row from cookies limit 1').fetchone()
        if token:
            self.__token_id = token[0]
            cookies = json.loads(unquote(token[1]))
            self.session.cookies = self.cookiejar_from_dict(cookies)
            return True
        self.logger.warning('[%s]: 数据库中Cookie为空,等待300秒...'%tools.current_time())
        tools.sleep(300)
        return False


    def __status_up(self):
        """
        更新抓取状态
        :return:
        """
        sqlite.execute('update listing set status=0')
        sqlite.commit()

    def __info_get(self):
        # 设置代理
        if self.__is_proxy: self.session.proxies = self.__get_proxies_ip()
        # 组装url
        query = '/?m=%s' % self.__seller if self.__seller else ''
        url = 'https://www.amazon.com/dp/%s%s' % (self.__asin, query)
        # 获取Html
        html = self.request(url=url)
        if not html: return False
        img, bsr, pre, sto = self.__item_(html)
        if not (pre and sto):
            self.logger.warning('[%s]: 排名:%s, 价格:%s, 库存:%s  %s' % (tools.current_time(), bsr, pre, sto, url))
            return False
        # 显示成功日志
        if self.__log_show: self.logger.warning('排名:%s, 价格:%s, 库存:%s' % (bsr, pre, sto))
        return dict(bsr=bsr, price=pre, stock=sto, img=img, uptime=tools.current_time('%Y-%m-%d %H:%M:%S'), aid=self.__aid)


    def __item_(self, html):
        #
        sid = tools.xpath_one('//input[@id="session-id"][@name="session-id"]/@value', html)
        #
        oid = tools.xpath_one('//input[@id="offerListingID"][@name="offerListingID"]/@value', html)
        # 产品图片
        img = tools.re_one(r'colorImages\'.*?(https.*?)"', html)
        # 获取BSR排名
        bsr = tools.re_one(r"#([\d,]+)\sin.*See top 100.*</a>\)", html)
        # 获取产品价格
        pre = tools.re_one(r'id=\"priceblock_ourprice.*?>\$([\d.]+)<', html)
        # 获取产品库存
        sto = tools.re_one(r'Only (\d+?) left in stock - order soon.', html)
        if not sto: sto = self.__stock_(sid, oid)

        return img, bsr, pre, sto

    def __stock_(self, sid, oid):
        # 请求地址
        url = "https://www.amazon.com/gp/add-to-cart/json/ref=dp_start-bbf_1_glance"
        # 构造发送数据
        data = {
            'clientName': 'SmartShelf',
            'ASIN': '%s' % self.__asin,
            'verificationSessionID': '%s' % sid,
            'offerListingID': '%s' % oid,
            'quantity': '99999'
        }
        stock = self.request(method='POST', url=url, data=data)
        stock = json.loads(stock.strip())
        # 请求完成删除代理
        self.session.proxies = {}
        if stock.get('isOK'): return stock.get('cartQuantity')
        return ''

    def __get_proxies_ip(self):
        proxies = {}
        if self.__proxy_api is None: proxies
        ip = self.request(url=self.__proxy_api)
        if ip: proxies = {'http':ip, 'https':ip}
        else: self.logger.warning('[%s]: Get Porxies Failed!' % tools.current_time())
        return proxies


if __name__ == '__main__':
    goods = Goods()
    goods.get()
