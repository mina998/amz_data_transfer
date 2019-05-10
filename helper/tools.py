import re, time, datetime
from lxml import etree

class Tools(object):

    @staticmethod
    def xpath_one(xpath, docment, i=0):
        element = etree.HTML(docment)
        list = element.xpath(xpath)
        if len(list) > i: return list[i]
        return ''


    @staticmethod
    def re_one(ptn, html, i=0):
        list = re.findall(ptn, html, re.I)
        if len(list) > i: return list[i].replace(',', '')
        return ''

    @staticmethod
    def sleep(s):
        """
        休眠时间
        :param s:
        :return:
        """
        time.sleep(s)

    @staticmethod
    def current_time(str='%Y-%m-%d %H:%M:%S'):
        """
        获取当日期时间
        :param str: 日期时间格式
        :return: 日期时间
        """
        return datetime.datetime.now().strftime(str)

    @staticmethod
    def time_stamp_now(t=False):
        """
        获取当前时间戳
        :return:
        """
        if t: return int(time.time())
        return time.time()

    @staticmethod
    def next_time_stamp():
        """
        明天时间戳
        :return:
        """
        # 当天日期
        today    = datetime.date.today()
        # 明天日期
        tomorrow = today + datetime.timedelta(days=1)
        # 转为时间数组
        timeArray = time.strptime(str(tomorrow), "%Y-%m-%d")
        # 转为时间戳
        return int(time.mktime(timeArray))
