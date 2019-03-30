#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: start.py
@time: 2019/3/5 14:27:30
@desc:

"""
import time
from os import walk

import datetime

import pyodbc
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk


class ElasticObj:
    def __init__(self, index_name, index_type, ip="127.0.0.1"):
        '''

        :param index_name: 索引名称
        :param index_type: 索引类型
        '''
        self.index_name = index_name
        self.index_type = index_type
        # 无用户名密码状态
        # self.es = Elasticsearch([ip])
        # 用户名密码状态
        self.es = Elasticsearch([ip], http_auth=('elastic', 'password'), port=9200)

    def create_index(self, index_name="ott", index_type="ott_type"):
        '''
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param ex: Elasticsearch对象
        :return:
        '''
        # 创建映射
        _index_mappings = {
            "mappings": {
                self.index_type: {
                    "properties": {
                        "title": {
                            "type": "text",
                            "index": True,
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "date": {
                            "type": "text",
                            "index": True
                        },
                        "keyword": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "source": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "link": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                }

            }
        }
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=_index_mappings)
            print res

    def IndexData(self):
        es = Elasticsearch()
        csvdir = 'D:/work/ElasticSearch/exportExcels'
        filenamelist = []
        for (dirpath, dirnames, filenames) in walk(csvdir):
            filenamelist.extend(filenames)
            break
        total = 0
        for file in filenamelist:
            csvfile = csvdir + '/' + file
            self.Index_Data_FromCSV(csvfile, es)
            total += 1
            print total
            time.sleep(10)

    def Index_Data_FromCSV(self, csvfile):
        '''
        从CSV文件中读取数据，并存储到es中
        :param csvfile: csv文件，包括完整路径
        :return:
        '''
        list = CSVOP.ReadCSV(csvfile)
        index = 0
        doc = {}
        for item in list:
            if index > 1:  # 第一行是标题
                doc['title'] = item[0]
                doc['link'] = item[1]
                doc['date'] = item[2]
                doc['source'] = item[3]
                doc['keyword'] = item[4]
                res = self.es.index(index=self.index_name, doc_type=self.index_type, body=doc)
                print(res['created'])
            index += 1
            print index

    def Index_Data(self):
        '''
        数据存储到es
        :return:
        '''
        list = [
            {"date": "2017-09-13",
             "source": "慧聪网",
             "link": "http://info.broadcast.hc360.com/2017/09/130859749974.shtml",
             "keyword": "电视",
             "title": "付费 电视 行业面临的转型和挑战"
             },
            {"date": "2017-09-13",
             "source": "中国文明网",
             "link": "http://www.wenming.cn/xj_pd/yw/201709/t20170913_4421323.shtml",
             "keyword": "电视",
             "title": "电视 专题片《巡视利剑》广获好评：铁腕反腐凝聚党心民心"
             }
        ]
        for item in list:
            res = self.es.index(index=self.index_name, doc_type=self.index_type, body=item)
            print(res['created'])

    def bulk_Index_Data(self):
        '''
        用bulk将批量数据存储到es
        :return:
        '''
        list = [
            {"date": "2017-09-13",
             "source": "慧聪网",
             "link": "http://info.broadcast.hc360.com/2017/09/130859749974.shtml",
             "keyword": "电视",
             "title": "付费 电视 行业面临的转型和挑战"
             },
            {"date": "2017-09-13",
             "source": "中国文明网",
             "link": "http://www.wenming.cn/xj_pd/yw/201709/t20170913_4421323.shtml",
             "keyword": "电视",
             "title": "电视 专题片《巡视利剑》广获好评：铁腕反腐凝聚党心民心"
             },
            {"date": "2017-09-13",
             "source": "人民电视",
             "link": "http://tv.people.com.cn/BIG5/n1/2017/0913/c67816-29533981.html",
             "keyword": "电视",
             "title": "中国第21批赴刚果（金）维和部隊启程--人民 电视 --人民网"
             },
            {"date": "2017-09-13",
             "source": "站长之家",
             "link": "http://www.chinaz.com/news/2017/0913/804263.shtml",
             "keyword": "电视",
             "title": "电视 盒子 哪个牌子好？ 吐血奉献三大选购秘笈"
             }
        ]
        ACTIONS = []
        i = 1
        for line in list:
            action = {
                "_index": self.index_name,
                "_type": self.index_type,
                "_id": i,  # _id 也可以默认生成，不赋值
                "_source": {
                    "date": line['date'],
                    "source": line['source'].decode('utf8'),
                    "link": line['link'],
                    "keyword": line['keyword'].decode('utf8'),
                    "title": line['title'].decode('utf8')}
            }
            i += 1
            ACTIONS.append(action)
            # 批量处理
        success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
        print('Performed %d actions' % success)

    def Delete_Index_Data(self, id):
        '''
        删除索引中的一条
        :param id:
        :return:
        '''
        res = self.es.delete(index=self.index_name, doc_type=self.index_type, id=id)
        print res

    def Get_Data_Id(self, id):

        res = self.es.get(index=self.index_name, doc_type=self.index_type, id=id)
        print(res['_source'])

        print '------------------------------------------------------------------'
        #
        # # 输出查询到的结果
        for hit in res['hits']['hits']:
            # print hit['_source']
            print hit['_source']['date'], hit['_source']['source'], hit['_source']['link'], hit['_source']['keyword'], \
                hit['_source']['title']

    def Get_Data_By_Body(self):
        # doc = {'query': {'match_all': {}}}
        doc = {
            "query": {
                "match": {
                    "keyword": "电视"
                }
            }
        }
        _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=doc)

        for hit in _searched['hits']['hits']:
            # print hit['_source']
            print hit['_source']['date'], hit['_source']['source'], hit['_source']['link'], hit['_source']['keyword'], \
                hit['_source']['title']


class ElasticSearchClass(object):

    def __init__(self, host, port, user, passwrod):
        self.host = host
        self.port = port
        self.user = user
        self.password = passwrod
        self.es = None
        self.connect()

    def connect(self):
        self.es = Elasticsearch(hosts=[{'host': self.host, 'port': self.port}],
                                http_auth=(self.user, self.password))

    def insert(self, index, doc_type, body, id=None):
        """
        插入一条数据body到指定的index、指定的type下;可指定Id,若不指定,ES会自动生成
        :param index: 待插入的index值
        :param doc_type: 待插入的type值
        :param body: 待插入的数据 -> dict型
        :param id: 自定义Id值
        :return:
        """
        return self.es.index(index=index, doc_type=doc_type, body=body, id=id)

    def count(self, index_name):
        """
        :param index_name:
        :return: 统计index总数
        """
        return self.es.count(index=index_name)

    def delete(self, indexname, doc_type, id):
        """
        :param indexname:
        :param doc_type:
        :param id:
        :return: 删除index中具体的一条
        """
        self.es.delete(index=indexname, doc_type=doc_type, id=id)

    def get(self, indexname, doc_type, id):
        return self.es.get(index=indexname, doc_type=doc_type, id=id)

    def search_index(self, index):
        """
        查找所有index数据
        """
        try:
            return self.es.search(index=index)
        except Exception as err:
            print(err)

    def search_doc(self, index=None, doc_type=None, body=None):
        """
        查找index下所有符合条件的数据
        :param index:
        :param doc_type:
        :param body: 筛选语句,符合DSL语法格式
        :return:
        """
        return self.es.search(index=index, doc_type=doc_type, body=body)

    def search(self, index, doc_type, body, size=10, from_=0, scroll='10s'):
        """
        根据index，type查找数据，
        其中size默认为十条数据，可以修改为其他数字，但是不能大于10000
        """
        return self.es.search(index=index, doc_type=doc_type, body=body, size=size, from_=from_, scroll=scroll)

    def scroll(self, scroll_id, scroll):
        """
        根据上一个查询方法，查询出来剩下所有相关数据
        """
        return self.es.scroll(scroll_id=scroll_id, scroll=scroll)


def get_db_conn():
    """
    初始化数据库
    :return: 数据库连接
    """
    config = {
        'db_host': '192.168.11.106',
        'db_port': '33434',
        'db_user': 'user_fafa',
        'db_pwd': 'user_fafa123456',
        'db_db': 'hft_searchdb'
    }
    conn_info_str = 'DRIVER={SQL Server};SERVER=%s,%s;UID=%s;PWD=%s;DATABASE=%s' % (
        config['db_host'], config['db_port'], config['db_user'], config['db_pwd'], config['db_db'])
    conn = pyodbc.connect(conn_info_str, unicode_results=True, autocommit=True)

    return conn


def query_datas(table):
    db_conn = get_db_conn()
    cursor = db_conn.cursor()

    total = 0
    page = 1
    row = 10000
    # sql_str = "select province_id,city_id from hft_admindb..fun_city order by city_id"
    # citys = cursor.execute(sql_str)
    # citys = citys.fetchall()

    citys = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (15, 6), (23, 7), (9, 8), (22, 9), (11, 10), (19, 11),
             (19, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 19), (3, 20), (3, 21), (3, 22),
             (3, 23), (4, 24), (4, 25), (4, 26), (4, 27), (4, 28), (4, 29), (4, 30), (4, 31), (4, 32), (4, 33), (4, 34),
             (5, 35), (5, 36), (5, 37), (5, 38), (5, 39), (5, 40), (5, 41), (5, 42), (5, 43), (5, 44), (5, 45), (5, 46),
             (6, 47), (6, 48), (6, 49), (6, 50), (6, 51), (6, 52), (6, 53), (6, 54), (6, 55), (6, 56), (6, 57), (6, 58),
             (6, 59), (6, 60), (7, 61), (7, 62), (7, 63), (7, 64), (7, 65), (7, 66), (7, 67), (7, 68), (7, 69), (8, 70),
             (8, 71), (8, 72), (8, 73), (8, 74), (8, 75), (8, 76), (8, 77), (8, 78), (8, 79), (8, 80), (8, 81), (8, 82),
             (10, 83), (10, 84), (10, 85), (10, 86), (10, 87), (10, 88), (10, 89), (10, 90), (10, 91), (10, 92),
             (10, 93), (10, 94), (10, 95), (11, 96), (11, 97), (11, 98), (11, 99), (11, 100), (11, 101), (11, 102),
             (11, 103), (11, 104), (11, 105), (12, 106), (12, 107), (12, 108), (12, 109), (12, 110), (12, 111),
             (12, 112), (12, 113), (12, 114), (12, 115), (12, 116), (12, 117), (12, 118), (12, 119), (12, 120),
             (12, 121), (12, 122), (13, 123), (13, 124), (13, 125), (13, 126), (13, 127), (13, 128), (13, 129),
             (13, 130), (13, 131), (14, 132), (14, 133), (14, 134), (14, 135), (14, 136), (14, 137), (14, 138),
             (14, 139), (14, 140), (14, 141), (14, 142), (15, 143), (15, 144), (15, 145), (15, 146), (15, 147),
             (15, 148), (15, 149), (15, 150), (15, 151), (15, 152), (15, 153), (15, 154), (15, 155), (15, 156),
             (15, 157), (15, 158), (16, 159), (16, 160), (16, 161), (16, 162), (16, 163), (16, 164), (16, 165),
             (16, 166), (16, 167), (16, 168), (16, 169), (16, 170), (16, 171), (16, 172), (16, 173), (16, 174),
             (16, 175), (17, 176), (17, 177), (17, 178), (17, 179), (17, 180), (17, 181), (17, 182), (17, 183),
             (17, 184), (17, 185), (17, 186), (17, 187), (17, 188), (17, 189), (17, 190), (17, 191), (17, 192),
             (18, 193), (18, 194), (18, 195), (18, 196), (18, 197), (18, 198), (18, 199), (18, 200), (18, 201),
             (18, 202), (18, 203), (18, 204), (18, 205), (18, 206), (19, 207), (19, 208), (19, 209), (19, 210),
             (19, 211), (19, 212), (19, 213), (19, 214), (19, 215), (19, 216), (19, 217), (19, 218), (19, 219),
             (19, 220), (19, 221), (19, 222), (19, 223), (19, 224), (19, 225), (20, 226), (20, 227), (20, 228),
             (20, 229), (20, 230), (20, 231), (20, 232), (20, 233), (20, 234), (20, 235), (20, 236), (20, 237),
             (20, 238), (20, 239), (21, 240), (21, 241), (21, 242), (21, 243), (21, 244), (21, 245), (21, 246),
             (21, 247), (21, 248), (21, 249), (21, 250), (21, 251), (21, 252), (21, 253), (21, 254), (21, 255),
             (21, 256), (21, 257), (21, 258), (21, 259), (21, 260), (1, 261), (1, 262), (1, 263), (1, 264), (1, 265),
             (1, 266), (1, 267), (1, 268), (1, 269), (1, 270), (1, 271), (1, 272), (1, 273), (1, 274), (24, 275),
             (24, 276), (24, 277), (24, 278), (24, 279), (24, 280), (24, 281), (24, 282), (24, 283), (25, 284),
             (25, 285), (25, 286), (25, 287), (25, 288), (25, 289), (25, 290), (25, 291), (25, 292), (25, 293),
             (25, 294), (25, 295), (25, 296), (25, 297), (25, 298), (25, 299), (26, 300), (26, 301), (26, 302),
             (26, 303), (26, 304), (26, 305), (26, 306), (27, 307), (27, 308), (27, 309), (27, 310), (27, 311),
             (27, 312), (27, 313), (27, 314), (27, 315), (27, 316), (28, 317), (28, 318), (28, 319), (28, 320),
             (28, 321), (28, 322), (28, 323), (28, 324), (28, 325), (28, 326), (28, 327), (28, 328), (28, 329),
             (28, 330), (29, 331), (29, 332), (29, 333), (29, 334), (29, 335), (29, 336), (29, 337), (29, 338),
             (30, 339), (30, 340), (30, 341), (30, 342), (30, 343), (31, 344), (31, 345), (31, 346), (31, 347),
             (31, 348), (31, 349), (31, 350), (31, 351), (31, 352), (31, 353), (31, 354), (31, 355), (31, 356),
             (31, 357), (31, 358), (31, 359), (31, 360), (31, 361), (34, 362), (34, 363), (34, 364), (34, 365),
             (34, 366), (34, 367), (34, 368), (2, 369), (1, 370), (1, 371), (16, 372), (33, 381), (32, 382)]

    if table == "sale_in":
        sql_str = "select province_id,city_id,id,status_flag, in_time, title, build_name, region, region_id, " \
                  "section, section_id, sectors, owner, mobile_phone, total_price, unit_price, useage, area, room, " \
                  "hall, wei, yang, fitment, direct, page_sours, repeat_id, charact from sale_in " \
                  "where province_id={0} and city_id={1} order by id " \
                  "OFFSET {2} ROW FETCH NEXT {3} rows only"
    else:
        sql_str = "select province_id,city_id,id,status_flag, in_time, title, build_name, region, region_id, " \
                  "section, section_id, sectors, owner, mobile_phone, total_price, price_unit, useage, area, room, " \
                  "hall, wei, yang, fitment, direct, page_sours, repeat_id, charact from lease_in " \
                  "where province_id={0} and city_id={1} order by id " \
                  "OFFSET {2} ROW FETCH NEXT {3} rows only"
    for c in citys:
        p_id, c_id = c[0], c[1]
        while True:
            cursor.execute(sql_str.format(p_id, c_id, (page - 1) * row, row))
            rows = cursor.fetchall()
            print('load datas:{0}-{1}, pages:{2}, rows:{3}'.format(p_id, c_id, page, len(rows)))
            page += 1
            if not rows:
                page = 1
                break

            for r in rows:
                total += 1
                data = {
                    "province_id": r[0],
                    "city_id": r[1],
                    "id": r[2],
                    "status_flag": r[3],
                    "in_time": r[4],
                    "title": r[5],
                    "build_name": r[6],
                    "region": r[7],
                    "region_id": r[8],
                    "section": r[9],
                    "section_id": r[10],
                    "sectors": r[11],
                    "owner": r[12],
                    "mobile_phone": r[13],
                    "total_price": r[14],
                    "unit_price": r[15],
                    "useage": r[16],
                    "area": r[17],
                    "room": r[18],
                    "hall": r[19],
                    "wei": r[20],
                    "yang": r[21],
                    "fitment": r[22],
                    "direct": r[23],
                    "page_sours": r[24],
                    "repeat_id": r[25],
                    "charact": r[26],
                }
                yield data


def init_data():
    # es 地址：172.16.13.22:9200
    # http://172.16.13.22:9800/

    hosts = [
        {"host": "172.16.13.22", "port": 9200}
    ]

    es = Elasticsearch(hosts=hosts)

    lst_datas = []
    table = 'sale_in'
    # table = 'lease_in'
    index = "index_ss_{0}".format(table)
    for data in query_datas(table):
        lst_datas.append({
            '_op_type': 'index',  # create 创建，index 创建更新，delete 删除， update  更新
            "_index": index,
            "_type": "text",
            "_id": data["id"],
            "_source": data,
        })
        if len(lst_datas) >= 10000:
            helpers.bulk(es, lst_datas)
            print("insert data size:{0}".format(len(lst_datas)))
            lst_datas = []

    if lst_datas:
        helpers.bulk(es, lst_datas)


def search():
    hosts = [
        {"host": "172.16.13.22", "port": 9200}
    ]

    es = Elasticsearch(hosts=hosts)
    index = "index_ss_gr_sale_c1"

    body = {
        "query": {
            "bool": {
                "must": [
                    # {"term": {"id": 1346798279}},  # 精确查找
                    {"match": {"city_id": 1}},
                    {"match": {"build_name": "公寓"}},
                ]
            }

            # "match": {
            #     "build_name": "成都"
            # }
        },
        "sort": [{"in_time": "desc"}]
    }
    params = {
        "from": 0,  # 分页
        "size": 1000,  # 分页
    }
    results = es.search(index=index, body=body, params=params)

    datas = results.get('hits', {}).get('hits', {})
    for d in datas:
        source = d.get('_source', {})
        ss = [unicode(x) for x in source.values()]
        print(u'|'.join(ss))

    took = results.get('took')
    timed_out = results.get('timed_out')
    total = results.get('hits', {}).get('total')
    print(u"总数据：{0}, 花费：{1}ms".format(total, took))


def query(es, index, body, params):
    results = es.search(index=index, body=body, params=params)

    took = results.get('took')
    timed_out = results.get('timed_out')
    total = results.get('hits', {}).get('total', 0)
    print(u"total：{0}, cost：{1}ms, time_out:{2}".format(total, took, timed_out))

    datas = results.get('hits', {}).get('hits', {})
    return datas


def search_test():
    hosts = [
        {"host": "172.16.13.22", "port": 9200}
    ]
    es = Elasticsearch(hosts=hosts)

    # 分页查询
    index = "index_ss_sale_in"
    body = {
        "query": {"bool": {"must": [{"match": {"city_id": 1}}]}},
        "from": 0,
        "size": 0,
        "sort": [{"in_time": "desc"}],
        # "aggs": {"avg_price": {"avg": {"field": "total_price"}}}
    }
    params = {
        "from": 0,  # 分页
        "size": 100,  # 分页
    }

    datas = query(es, index, body, params)
    for d in datas:
        source = d.get('_source', {})
        ss = [unicode(x) for x in source.values()]
        print(u'|'.join(ss))


def start():
    # init_data()
    search()
    # search_test()


if __name__ == '__main__':
    start()
