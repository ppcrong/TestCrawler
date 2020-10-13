import os
import shutil
from pprint import pprint
from urllib.parse import urlparse
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree


def test1():
    """
    https://medium.com/@yanweiliu/python%E7%88%AC%E8%9F%B2%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%B8%80-beautifulsoup-1ee011df8768
    """

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
    """
    https://medium.com/@yanweiliu/python%E7%88%AC%E8%9F%B2%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%B8%80-beautifulsoup-1ee011df8768
    """

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


def test4():
    """
    https://ithelp.ithome.com.tw/articles/10203744
    """

    # r = requests.get('https://www.google.com/search?q=python3')

    payload = {
        'q': 'python3'
    }
    r = requests.get('https://www.google.com/search?', params=payload)

    # save result to html for analysis
    save_text('test4.html', r.text)

    r = requests.post('https://httpbin.org/post', data={'key': 'value'})
    # r = requests.put('https://httpbin.org/put', data = {'key':'value'})
    # r = requests.delete('https://httpbin.org/delete')
    # r = requests.head('https://httpbin.org/get')
    # r = requests.options('https://httpbin.org/get')
    pprint(r.text)


def test5():
    """
    https://ithelp.ithome.com.tw/articles/10204390
    """

    ua = UserAgent(verify_ssl=False)
    headers = {"User-Agent": ua.chrome}
    r = requests.get('https://www.google.com/search?q=python3', headers=headers)

    # save result to html for analysis
    save_text('test5.html', r.text)

    soup = BeautifulSoup(r.text, 'lxml')
    a_title = soup.select('a h3')
    for t in a_title:
        print(t.text)
    print('-----------------')

    # ugly code here++++++++++++++++
    a_list = soup.select('div#rso div.g div.rc div.r a')
    new_list = []
    """
    remove some useless tags

    tag we need is as below:
        <a href="https://www.python.org/download/releases/3.0/" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://www.python.org/download/releases/3.0/&amp;ved=2ahUKEwj2kvLaz43qAhV5ITQIHetZAlwQFjAAegQIAxAB">

    tag we don't need has attr "class" as below:
        <a class="GHDvEf" href="#" id="am-b0" aria-label="結果選項" aria-expanded="false" aria-haspopup="true" role="button" jsaction="m.tdd;keydown:m.hbke;keypress:m.mskpe" data-ved="2ahUKEwj2kvLaz43qAhV5ITQIHetZAlwQ7B0wAHoECAMQBA">
        <a class="fl" href="https://translate.google.com/translate?hl=zh-TW&amp;sl=en&amp;u=https://www.python.org/download/releases/3.0/&amp;prev=search" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://translate.google.com/translate%3Fhl%3Dzh-TW%26sl%3Den%26u%3Dhttps://www.python.org/download/releases/3.0/%26prev%3Dsearch&amp;ved=2ahUKEwj2kvLaz43qAhV5ITQIHetZAlwQ7gEwAHoECAMQCQ">翻譯這個網頁</a>
    """
    for a in a_list:
        if not a.has_attr('class'):
            new_list.append(a)
    # ugly code here----------------

    print('len(new_list):{}'.format(len(new_list)))
    for a in new_list:
        print('title', a.text)
        print('href', a['href'])
        r = requests.get(a['href'])
        with open("".join(x for x in a.text if (x.isalnum() or x in "._- ")) + '.html', 'w+', encoding="utf-8") as f:
            f.write(r.text)
            print('saved')


def test6():
    """
    my own practice
    """

    ua = UserAgent(verify_ssl=False)
    headers = {"User-Agent": ua.chrome}
    res = requests.get("https://weekly.manong.io/issues/", headers=headers)

    # save result to html for analysis
    save_text('test6.html', res.text)

    content = res.content.decode()
    html = etree.HTML(content)

    # get the newest title and link
    new_title = html.xpath('/html/body/div[2]/h4/a/text()')
    new_href = html.xpath('/html/body/div[2]/h4/a/@href')
    if len(new_title) > 0 and len(new_href) > 0:
        print('最新一期：{}'.format(new_title[0]))
        print('最新連結：{}'.format(new_href[0]))
        res = requests.get(new_href[0], headers=headers)
        with open("".join(x for x in new_title[0] if (x.isalnum() or x in "._- ")) + '.html', 'w+',
                  encoding="utf-8") as f:
            f.write(res.text)
            print('({}) 已存檔'.format(f.name))


def save_text(filename: str, text: str):
    with open(filename, 'w+', encoding="utf-8") as f:
        f.write(text)
    print('{} saved'.format(filename))


def get_all_title_href(url):
    """
    https://ithelp.ithome.com.tw/articles/10204709
    """

    ua = UserAgent(verify_ssl=False)
    headers = {"User-Agent": ua.chrome}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # get title href
    results = soup.select("div.title")
    urlp = urlparse(url)

    # save result to html for analysis
    save_text(os.path.basename(urlp.path), r.text)

    print('++++++++++++++++++++{}++++++++++++++++++++'.format(os.path.basename(urlp.path)))
    for item in results:
        a_item = item.select_one("a")
        title = item.text
        if a_item:
            print('https://www.ptt.cc' + a_item.get('href'))
            get_article_content('https://www.ptt.cc' + a_item.get('href'))
    print('--------------------{}--------------------\n\n'.format(os.path.basename(urlp.path)))

    # get up btn href and return
    btn = soup.select('div.btn-group > a')
    up_page_href = btn[3]['href']
    return 'https://www.ptt.cc' + up_page_href


def get_article_content(article_url):
    ua = UserAgent(verify_ssl=False)
    headers = {"User-Agent": ua.chrome}
    r = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    results = soup.select('span.article-meta-value')
    if results:
        print('作者:', results[0].text)
        print('看板:', results[1].text)
        print('標題:', results[2].text)
        print('時間:', results[3].text)


def test7(loop=1):
    """
    https://ithelp.ithome.com.tw/articles/10204709
    """

    url = "https://www.ptt.cc/bbs/Food/index.html"

    for page in range(1, loop + 1):
        url = get_all_title_href(url=url)


def test8():
    img_url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
    img_name = 'google'
    download_img(img_url=img_url, img_name=img_name, ext_name='png')
    download_img2(img_url=img_url, img_name=img_name + '2', ext_name='png')


def download_img(img_url: str, img_name: str, ext_name: str):
    # create image folder if not exist
    folder = './image/'
    if not os.path.isdir(folder):
        os.mkdir(folder)

    ua = UserAgent(verify_ssl=False)
    headers = {"User-Agent": ua.chrome}
    r = requests.get(img_url, stream=True, headers=headers)
    print('save img to ./image/' + img_name + '.' + ext_name)
    try:
        with open('./image/' + img_name + '.' + ext_name, 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)
    except:
        print('can not save img', img_url)


def download_img2(img_url: str, img_name: str, ext_name: str):
    # create image folder if not exist
    folder = './image2/'
    if not os.path.isdir(folder):
        os.mkdir(folder)

    print('save img to ./image2/' + img_name + '.' + ext_name)
    try:
        urlretrieve(url=img_url, filename='./image2/' + img_name + '.' + ext_name)
    except:
        print('can not save img', img_url)


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    test6()
    # test7(2)
    #test8()
