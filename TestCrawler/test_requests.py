import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree

"""
https://medium.com/@yanweiliu/python%E7%88%AC%E8%9F%B2%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%B8%80-beautifulsoup-1ee011df8768
"""


def test1():
    url = "https://jwlin.github.io/py-scraping-analysis-book/ch1/connect.html"
    rsp = requests.get(url)
    print('rsp.text:{}'.format(rsp.text))

    # 網頁抓取後編碼錯誤?
    rsp.encoding = 'utf-8'  # 轉換編碼至UTF-8
    # rsp.encoding = 'big5'  # 設定成該網頁的編碼，例如big5編碼或簡體的gbk編碼
    # 顯示網頁狀態
    print('rsp.status_code:{}'.format(rsp.status_code))
    # 顯示200即為正常
    # 通常2開頭為正常
    # 開頭為4或5表示錯誤

    soup = BeautifulSoup(rsp.text, 'lxml')
    print(soup)


def test2():
    payload = {'key1': 'value1', 'key2': 'value2'}
    # 將查詢參數加入 GET 請求中
    html = requests.get("http://httpbin.org/get", params=payload)
    print(html.url)  # http://httpbin.org/get?key1=value1&key2=value2
    print('html.text:{}'.format(html.text))  # 以json格式呈現
    # 將查詢參數加入 POST 請求中
    html = requests.post("http://httpbin.org/post", data=payload)
    print('html.text:{}'.format(html.text))  # 以json格式呈現

    soup = BeautifulSoup(html.text, 'lxml')
    print(soup)


def test3():
    """
    https://medium.com/%E9%B3%A5-crl/python%E9%9A%A8%E7%AD%86-requests-lxml%E5%9F%BA%E6%9C%AC%E7%88%AC%E8%9F%B2-%E4%BB%A5%E5%8D%9A%E5%AE%A2%E4%BE%86%E5%8D%B3%E6%99%82%E6%8E%92%E8%A1%8C%E6%A6%9C%E7%82%BA%E4%BE%8B-f9c67de0644e
    """

    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

    # res = requests.get("http://www.books.com.tw/web/sys_hourstop/home?loc=P_003_001", headers=headers)
    # content = res.content.decode()
    # html = etree.HTML(content)
    # title = html.xpath('//body/div[4]/div/div[2]/div[1]/div/div[1]/ul/li/div[2]/h4/a/text()')
    # price = html.xpath('//body/div[4]/div/div[2]/div[1]/div/div[1]/ul/li/div[2]/ul/li/strong[last()]/b/text()')

    ua = UserAgent(verify_ssl=False)
    headers = {"User-Agent": ua.chrome}
    res = requests.get("https://www.books.com.tw/web/sys_hourstop/home?loc=act_menu_0_001", headers=headers)
    content = res.content.decode()
    html = etree.HTML(content)
    title = html.xpath('//body/div[4]/div/div[2]/div[1]/div/div[1]/ul/li/div[2]/h4/a/text()')
    price = html.xpath('//body/div[4]/div/div[2]/div[1]/div/div[1]/ul/li/div[2]/ul/li/strong[last()]/b/text()')
    for i, j in zip(title, price):
        print(i, j)


if __name__ == "__main__":
    # test1()
    # test2()
    test3()
