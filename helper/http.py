import logging, requests
from fake_useragent import UserAgent

class Http(object):

    logger = logging.getLogger(__name__)
    def __init__(self):
        """
        初始化
        """
        self.session = requests.session()
        self.session.headers.update({'User-Agent': UserAgent().chrome})

    def update(self, headers):
        """
        更新请求头信息
        :param headers:
        :return:
        """
        self.session.headers.update(headers)

    def request(self, method='GET', url=None, data=None, proxies=None):
        """
        发送请求
        :param method: 请求方法
        :param url: 请求地址
        :param params: url参数 dict类型
        :param data: Post数据 dict类型
        :return: Response 对象
        """

        try:
            response = self.session.request(method, url=url, data=data, proxies=proxies)
            if response.status_code in [200]: return response.text
        except Exception as e: pass  #self.logger.warning(e)
        return ''


    def dict_from_cookiejar(self, jar_cookies):
        """
        Cookie 转字典
        :param cookies:
        :return:
        """
        return requests.utils.dict_from_cookiejar(jar_cookies)


    def cookiejar_from_dict(self, dict_cookies):
        """
        字典转Cookie
        :param dict_cookies:
        :return:
        """
        return requests.utils.cookiejar_from_dict(dict_cookies)