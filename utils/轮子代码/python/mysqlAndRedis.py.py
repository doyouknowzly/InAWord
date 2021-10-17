import pymysql
import openpyxl


# 1.准备数据库数据

def functionGetReviewFromMysql():
	
	dbconn = pymysql.connect(
  	host = "119.29.11.72",
  	database = "global_community",
  	user = "root",
  	password = "root",
  	port = 3306,
  	charset = 'utf8'
 	)


	sql = "SELECT rid, pkg_name, content, create_time FROM review_0 where disabled = 0 and ischeck = 1"



	sql_test = "SELECT rid, pkg_name, content, create_time FROM review_"


	for i in range(9): 
		cur = dbconn.cursor()
		cur.execute("use global_community")
		cur.execute(sql_test + str(i))
		reviews = cur.fetchall()
		print(reviews)


functionGetReviewFromMysql()

# 2.查询redis数据

# 3.存储进excel
wb = openpyxl.Workbook()
wb.create_sheet('test_case')
wb.save('cases.xls')
