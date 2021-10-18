import pymysql
import xlwt
import xlrd
import redis
from rediscluster import StrictRedisCluster
import json
import time


class RedisCluster(object):  # 连接redis集群
    def __init__(self,conn_list):
        self.conn_list = conn_list  # 连接列表

    def connect(self):
        """
        连接redis集群
        :return: object
        """
        try:
            # 非密码连接redis集群, 配置Decode，否则数据中会多出字符'b'
            redisconn = StrictRedisCluster(startup_nodes=self.conn_list, decode_responses=True)
            return redisconn
        except Exception as e:
            print(e)
            print("错误,连接redis 集群失败")
            return False

    def get_state(self):
        """
        获取状态
        :return:
        """
        res = RedisCluster(self.conn_list).connect()
        # print("连接集群对象",res,type(res),res.__dict__)
        if not res:
            return False

        dic = res.cluster_info()  # 查看info信息, 返回dict

        for i in dic:  # 遍历dict
            ip = i.split(":")[0]
            if dic[i].get('cluster_state'):  # 获取状态
                print("节点状态, ip: ", ip, "value: ", dic[i].get('cluster_state'))





# 1.准备数据库数据

dbconn = pymysql.connect(host = "teststore-01.ctgmop49hwif.ap-southeast-1.rds.amazonaws.com", database = "global_community", user = "awstestuser", password = "97303af4f0be7e0551111ec78f78a880", port = 33066, charset = 'utf8')


sql = "SELECT rid, pkg_name, content, region, create_time FROM review_"
sql_tail = " where disabled = 0 and ischeck = 1"


sql_test = "SELECT rid, pkg_name, region, content, create_time FROM review_"





# 2.查询redis数据
redis_basis_conn = [
        {'host':'10.177.235.210','port':6379},
        {'host':'10.177.235.209','port': 6379},
        {'host':'10.177.118.22','port': 6379},
        {'host':'10.177.118.23','port': 6379},
        {'host':'10.177.235.213','port': 6379},
    ]
redis_conn = RedisCluster(redis_basis_conn).connect()

# 3.存储进excel
wb = xlwt.Workbook()
reviewExcel = wb.add_sheet('review.2021.10.18')

line = 0;
reviewExcel.write(line , 0, "rid")
reviewExcel.col(0).width = 7000
reviewExcel.write(line , 1, "pkg_name")
reviewExcel.col(1).width = 10000
reviewExcel.write(line , 2, "score")
reviewExcel.col(4).width = 5000
reviewExcel.write(line , 3, "content")
reviewExcel.col(3).width = 10000
reviewExcel.write(line , 4, "Date")
reviewExcel.col(4).width = 5000


for i in range(9): 
	cur = dbconn.cursor()
	cur.execute("use global_community")
	cur.execute(sql + str(i) + sql_tail)
	reviews = cur.fetchall()

	if(len(reviews)) > 0:
		for j in range(len(reviews)) : 

			one = reviews[j]
			rid = one[0]
			pkg_name = one[1]
			content = one[2]
			region = one[3]
			create_time = one[4]
			time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(create_time/1000)))
			jsonData = {}
			jsonData["pkgName"] = pkg_name
			if pkg_name is None:
				continue
			jsonData["region"] = region
			jsonData["rid"] = rid
			# separators用来避免json中出现空格
			jsonDataStr = json.dumps(jsonData, ensure_ascii=False, separators=(',',':'))
			print("forEach loop")
			print(jsonDataStr)
			#defaultKey = "GS_R_D_L::" + pkg_name
			key = "GS_R_D_L::" + pkg_name
			print("key: " + key)
			score = redis_conn.zscore(key, jsonDataStr)
			print(score)
			# iine行 x列
			line = line + 1
			reviewExcel.write(line , 0, str(rid))
			reviewExcel.write(line , 1, pkg_name)
			reviewExcel.write(line , 2, str(score))
			reviewExcel.write(line , 3, content)
			reviewExcel.write(line , 4, time_str)



wb.save('D:\\Users\\Desktop\\reviews.xls')

print("after excel")



