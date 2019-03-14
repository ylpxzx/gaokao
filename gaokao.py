import requests
import time
import re
from lxml import etree
import save
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Referer':'http://college.gaokao.com/schlist/a14/p2/',
            'Host':'college.gaokao.com'
        }

x={}
y_wen={}
y_li={}
tab = 'school_data'
json_name='school_data.json'
json1_name='school_data_li1.json'
json2_name='school_data_wen1.json'


def gain_html(url):
    response = requests.get(url, headers=headers)
    html = response.text
    return html

def parse_html(url):
    '''正则表达式爬取'''
    #爬取首页学校基本信息
    html=gain_html(url)
    pattern = re.compile(
        '<dt>.*?<img src="(.*?)".*?onerror.*?alt="(.*?)".*?<strong title=.*?<a href="(.*?)".*?<li>高校类型：(.*?)</li>.*?<li>高校隶属：(.*?)</li>.*?<li>高校性质：(.*?)</li>.*?<li>学校网址：(.*?)</li>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        x['id'] = item[1]
        x['school_img'] = item[0]
        x['school_type'] = item[3]
        x['school_subjection'] = item[4]
        x['school_nature'] = item[5]
        x['school_url'] = item[6]
        x['next_url'] = item[2]

        # 爬取学校页的地址信息
        next_url = x['next_url']
        school_html=gain_html(next_url)
        pattern = re.compile('<div class="college_msg bk">.*?<dl>.*?(通讯地址|学校地址)：(.*?)"*?<br.*?联系电话：', re.S)
        items1 = re.findall(pattern, school_html)
        for item1 in items1:
            x['local_name'] = item1[1]
        time.sleep(2)
        #存入数据库或者json文件
        save.to_mysql(tab, x)
        save.to_json(json_name, x)



        #爬取分数线
        school_html = etree.HTML(school_html)
        result = school_html.xpath('//div[@class="tabCon5"]//tr//td[position()<7]/text()')

        # result1是平均分数的数据列表
        result1 = school_html.xpath('//div[@class="tabCon5"]//tr//td[@id="pjf"]//a/text()')

        # 处理id=’pif_hs‘的异常标签
        result2 = school_html.xpath('//div[@class="tabCon5"]//tr//td[@id="pjf_hs"]//a/text()')

        school_name = school_html.xpath('//p[@class="btnFsxBox"]//font/text()')
        # 单个获取id=’pif_hs‘标签中的数据存入result1
        for res in result2:
            result1.append(res)
        p = len(result)
        #q是文科平均分数线的总数据
        q = len(result1)
        j = 0
        w = 0
        r = 0
        # t列表用于处理“首行缺少学历类型的分数线”
        t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

        try:
            # 首个if语句用于处理学校没有分数线数据的情况
            if result:
                # while用于分离文理科
                while result[0] != result[j + 6]:
                    j += 1
                a = j + 6

                # p是获取到的数据总数，a=j+6之前的数据是理科数据，后面是文科分数线的总数，l是文科分数线的总数
                l = p - a

                # u是文科平均分数总数的起始点
                u = int(a / 5)
                # if 判断是否为5的倍数（因为首行缺少录取批次的分数线总和数据不是5的倍数）
                if l / 5 not in t:
                    #处理一些首行录取批次为None的数据，将空的地方替换为’------‘
                    result.insert(int(a) + 4, '------')
                #爬取理科分数线
                for i in range(0, a + 1):
                    #按照获取的数据逻辑将数据存入json
                    if w <= a - 5 and r <= a / 5:
                        #根据获取到的数据的规律解析数据
                        y_li['id'] = school_name[0]
                        y_li['year'] = result[w]
                        y_li['low'] = result[w + 1]
                        y_li['high'] = result[w + 2]
                        y_li['ave'] = result1[r]
                        y_li['num'] = result[w + 3]
                        y_li['type'] = result[w + 4]
                        time.sleep(1)
                        print(y_li)
                        save.to_json(json1_name,y_li)
                        print("存入理科成功！")
                    #w是总分数线（除了平均数）的逻辑数
                    w += 5
                    #r是平均数的逻辑数
                    r += 1
                '''# 爬取文科分数线
                for i in range(0, l + 1):
                    # 按照获取的数据逻辑将数据存入json
                    if a <= p - 4 and u <= q:
                        y_wen['id'] = school_name[0]
                        y_wen['year'] = result[a]
                        y_wen['low'] = result[a + 1]
                        y_wen['high'] = result[a + 2]
                        y_wen['ave'] = result1[u]
                        y_wen['num'] = result[a + 3]
                        y_wen['type'] = result[a + 4]
                        time.sleep(1)
                        print(y_wen)
                        save.to_json(json2_name, y_wen)
                        print("存入文科成功！")
                    # a是总分数线（除了平均数）的逻辑数
                    a += 5
                    # u是平均数的逻辑数
                    u += 1'''
        except:
            pass

def main():
    for i in range(1, 4):
        url = 'http://college.gaokao.com/schlist/a14/p' + str(i) + '/'
        print("爬取第" + str(i) + "页")
        parse_html(url=url)
main()
