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
    sql_str = "select province_id,city_id from hft_admindb..fun_city order by city_id"
    citys = cursor.execute(sql_str)
    citys = citys.fetchall()

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
        cursor.execute(sql_str.format(p_id, c_id, (page-1)*row, row))
        page += 1

        for r in cursor:
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
    table = 'lease_in'
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
    index = "index_ss_sale_in"

    body = {
        "query": {
            "bool": {
                "must": [
                    # {"term": {"id": 1346798279}},  # 精确查找
                    {"match": {"city_id": 1}},
                    {"match": {"build_name": "广场"}},
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


def start():
    init_data()
    # search()


if __name__ == '__main__':
    start()
