import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
# 创建函数，获取页面数据
def get_urls(ui, n):  # ui:地址，n：页码数
    urllst = []
    for i in range(1, n + 1):
        urllst.append(ui + str(i))
    return urllst

# 获得每个页面信息
def get_onepage_data(u):  # u:网址
    r = requests.get(u)
    soup = BeautifulSoup(r.text, 'lxml')
    infor = soup.find('ul', class_="list_item clrfix").find_all('li')
    data_jd = []
    data_link = []
    for i in infor:
        dic = {}
        dic_link = {}

        dic['景点名称'] = i.find('span', class_="cn_tit").text
        dic['攻略提到数量'] = i.find('div', class_="strategy_sum").text
        dic['点评数量'] = i.find('div', class_="comment_sum").text
        dic['景点排名'] = i.find('span', class_="ranking_sum").text
        dic['驴友去过'] = i.find('span', class_="sum").text.split('%')[0]
        dic['星级'] = i.find('span', class_="cur_star")['style'].split(':')[1].split('%')[0]
        data_jd.append(dic)
    return data_jd


# 获得所有网页信息
def get_all_data(urls):  # urls 网址列表
    data_list = []

    for i in urls:
        data_list.extend(get_onepage_data(i))
    df = pd.DataFrame(data_list)  # 导入pandas的DataFrame
    df.index = df['景点名称']
    del df['景点名称']
    return df


# 数据字符转数字，以计算处理
def data_collation(df):
    df['点评数量'] = df['点评数量'].astype(np.int)
    df['攻略提到数量'] = df['攻略提到数量'].astype(np.int)
    df['驴友去过'] = df['驴友去过'].astype(np.int)
    df['星级'] = df['星级'].astype(np.int)
    df.fillna(value=0, inplace=True)
    return df


# 筛选综合得分前n名的数据
def data_top(urls, n):  # 前n个数据
    df = get_all_data(urls)
    df = data_collation(df)
    # 构建函数实现字段标准化，标准分
    cols = ['攻略提到数量', '星级', '点评数量']
    for col in cols:
        df[col + '_b'] = round((df[col] - df[col].min()) / (df[col].max() - df[col].min()) * 100, 2)
        # 由驴友去过比例得分+攻略提到数量得分+星级得分+点评数得分，每项均为0-100分
    df['综合得分'] = df['驴友去过'] + df['攻略提到数量_b'] + df['星级_b'] + df['点评数量_b']
    top_n = df.sort_values(by='综合得分', ascending=False).iloc[:n]
    return top_n


if __name__ == "__main__":
    start_time = time.time()
    urls = get_urls('https://travel.qunar.com/p-cs299861-nanjing-jingdian-1-', 5)  # 链接及页数
    top30_data = data_top(urls, 30)  # 前30的数据

    end_time1 = time.time()
    print("爬取基本数据，耗时:", end_time1 - start_time)

