from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class db_con2:
  host = config['DBSET']['HOST']
  port = config['DBSET']['PORT']
  user = config['DBSET']['USER']
  passwd = config['DBSET']['PASSWD']
  db = config['DBSET']['DB_Product']
  char = config['DBSET']['CHAR']

# route : /sync_now
def update_sync_now_fn():
  import pymysql
  conn = pymysql.connect(host=db_con2.host, port=db_con2.port, user=db_con2.user, password=db_con2.passwd, db=db_con2.db, charset=db_con2.char, autocommit=True)
  curs = conn.cursor(pymysql.cursors.DictCursor)

  SELECT_sql = '''SELECT SUM(CNT) FROM(
                    SELECT COUNT(*) as CNT FROM Product_List WHERE sync_now = '1'
                    UNION ALL
                    SELECT COUNT(*) as CNT FROM Product_List_SP WHERE sync_now = '1') a;'''
  curs.execute(SELECT_sql)
  sync_now = curs.fetchall()
  sync_now2 = sync_now[0]['SUM(CNT)']

  return sync_now2

# route : /Product_Rows
def update_Prod_Rows_fn():
  import pymysql
  conn = pymysql.connect(host=db_con2.host, port=db_con2.port, user=db_con2.user, password=db_con2.passwd, db=db_con2.db, charset=db_con2.char, autocommit=True)
  curs = conn.cursor(pymysql.cursors.DictCursor)
  
  table = "Prod_od_List"
  SELECT_sql = "SELECT COUNT(*) FROM "+str(table)+";"
  curs.execute(SELECT_sql)
  Prod_od_Row = curs.fetchall()

  table = "Product_List"
  SELECT_sql = "SELECT COUNT(*) FROM "+str(table)+";"
  curs.execute(SELECT_sql)
  Prod_Row = curs.fetchall()

  return Prod_od_Row+Prod_Row


def update_Prod_List_fn():
  import pymysql
  conn = pymysql.connect(host=db_con2.host, port=db_con2.port, user=db_con2.user, password=db_con2.passwd, db=db_con2.db, charset=db_con2.char, autocommit=True)
  curs2 = conn.cursor(pymysql.cursors.DictCursor)

  table2 = "Product_List"
  SELECT_sql2 = "SELECT prod_no,custom_prod_code,prod_name,prod_status,price,image_url,update_time FROM "+str(table2)+";"
  curs2.execute(SELECT_sql2)
  Product_List = curs2.fetchall()

  return Product_List


def update_Prod_od_List_fn():
  import pymysql
  conn = pymysql.connect(host=db_con2.host, port=db_con2.port, user=db_con2.user, password=db_con2.passwd, db=db_con2.db, charset=db_con2.char, autocommit=True)
  curs3 = conn.cursor(pymysql.cursors.DictCursor)

  table3 = "Prod_od_List"
  SELECT_sql3 = "SELECT pdn_odn,od_stock_sku,od_size,od_stock,od_price,od_status,update_time FROM "+str(table3)+" ORDER BY pdn,odn ASC;"
  curs3.execute(SELECT_sql3)
  Prod_od_List = curs3.fetchall()

  return Prod_od_List


def update_IN_quantity_fn():
  import pymysql
  current_Month = datetime.today().strftime("%m")
  class db_con:
    host = '10.33.111.91'
    port = 23306
    user = 'MALDEN'
    passwd = 'malden_00@'
    db = 'MALDEN_2021_'+current_Month
    char = 'utf8'
  conn = pymysql.connect(host=db_con.host, port=db_con.port, user=db_con.user, password=db_con.passwd, db=db_con.db, charset=db_con.char, autocommit=True)
  curs4 = conn.cursor(pymysql.cursors.DictCursor)
  current_Day = datetime.today().strftime("%d")

  table4 = "Product_IN_"+current_Day
  SELECT_sql4 = "SELECT custom_prod_code, size, quantity, insert_time FROM "+str(table4)+" WHERE confirm = 'NO' ORDER BY insert_time DESC;"
  curs4.execute(SELECT_sql4)
  Prod_IN = curs4.fetchall()

  SELECT_sql4 = "SELECT COUNT(*) FROM "+str(table4)+" WHERE confirm = 'NO';"
  curs4.execute(SELECT_sql4)
  Prod_IN_Row = curs4.fetchall()
  
  return Prod_IN_Row+Prod_IN


def update_OUT_quantity_fn():
  import pymysql
  current_Month = datetime.today().strftime("%m")
  class db_con:
    host = config['DBSET']['HOST']
    port = config['DBSET']['PORT']
    user = config['DBSET']['USER']
    passwd = config['DBSET']['PASSWD']
    db = 'MALDEN_2021_'+current_Month
    char = config['DBSET']['CHAR']
  conn2 = pymysql.connect(host=db_con.host, port=db_con.port, user=db_con.user, password=db_con.passwd, db=db_con.db, charset=db_con.char, autocommit=True)
  curs5 = conn2.cursor(pymysql.cursors.DictCursor)
  current_Day = datetime.today().strftime("%d")

  table5 = "Product_OUT_"+current_Day
  SELECT_sql5 = "SELECT custom_prod_code, size, quantity, insert_time FROM "+str(table5)+" WHERE confirm = 'NO' ORDER BY insert_time DESC;"
  curs5.execute(SELECT_sql5)
  Prod_OUT = curs5.fetchall()

  SELECT_sql5 = "SELECT COUNT(*) FROM "+str(table5)+" WHERE confirm = 'NO';"
  curs5.execute(SELECT_sql5)
  Prod_OUT_Row = curs5.fetchall()
  
  return Prod_OUT_Row+Prod_OUT


## SP(세트, 기획, 이벤트) 상품 START ##

# route : /Product_Rows_SP
def update_Prod_Rows_SP_fn(pdn):
  import pymysql
  conn = pymysql.connect(host=db_con2.host, port=db_con2.port, user=db_con2.user, password=db_con2.passwd, db=db_con2.db, charset=db_con2.char, autocommit=True)
  curs = conn.cursor(pymysql.cursors.DictCursor)

  if pdn != '':
    table = "Product_List_SP"
    SELECT_sql = "SELECT COUNT(*) FROM "+str(table)+" WHERE prod_no='"+str(pdn)+"';"
    curs.execute(SELECT_sql)
    Prod_Row_SP = curs.fetchall()
    
    table = "Prod_od_List_SP"
    SELECT_sql = "SELECT COUNT(*) FROM "+str(table)+" WHERE pdn='"+str(pdn)+"';"
    curs.execute(SELECT_sql)
    Prod_od_Row_SP = curs.fetchall()
  else:
    table = "Product_List_SP"
    SELECT_sql = "SELECT COUNT(*) FROM "+str(table)+";"
    curs.execute(SELECT_sql)
    Prod_Row_SP = curs.fetchall()
    
    table = "Prod_od_List_SP"
    SELECT_sql = "SELECT COUNT(*) FROM "+str(table)+";"
    curs.execute(SELECT_sql)
    Prod_od_Row_SP = curs.fetchall()

  return Prod_od_Row_SP+Prod_Row_SP


# route : /update_Prod_Total_Stock_SP
def update_Prod_Total_Stock_SP_fn():
  import pymysql
  conn = pymysql.connect(host=db_con2.host, port=db_con2.port, user=db_con2.user, password=db_con2.passwd, db=db_con2.db, charset=db_con2.char, autocommit=True)
  curs2 = conn.cursor(pymysql.cursors.DictCursor)

  table2 = "Prod_od_List_SP"
  SELECT_sql2 = "SELECT pdn,SUM(od_stock) FROM "+str(table2)+" GROUP BY pdn;"
  curs2.execute(SELECT_sql2)
  Prod_Total_Stock_SP = curs2.fetchall()

  return Prod_Total_Stock_SP


# route : /update_Prod_List_SP
def update_Prod_List_SP_fn(pdn):
  import pymysql
  conn = pymysql.connect(host=db_con2.host, port=db_con2.port, user=db_con2.user, password=db_con2.passwd, db=db_con2.db, charset=db_con2.char, autocommit=True)
  curs2 = conn.cursor(pymysql.cursors.DictCursor)

  table2 = "Product_List_SP"
  if pdn != '':
    SELECT_sql2 = "SELECT prod_no,custom_prod_code,prod_name,prod_status,price,image_url,update_time FROM "+str(table2)+" WHERE prod_no='"+str(pdn)+"';"
  else:
    SELECT_sql2 = "SELECT prod_no,custom_prod_code,prod_name,prod_status,price,image_url,update_time FROM "+str(table2)+";"
  curs2.execute(SELECT_sql2)
  Product_List_SP = curs2.fetchall()

  return Product_List_SP


# route : /update_Prod_od_List_SP
def update_Prod_od_List_SP_fn(pdn):
  import pymysql
  conn = pymysql.connect(host=db_con2.host, port=db_con2.port, user=db_con2.user, password=db_con2.passwd, db=db_con2.db, charset=db_con2.char, autocommit=True)
  curs3 = conn.cursor(pymysql.cursors.DictCursor)

  table3 = "Prod_od_List_SP"
  if pdn != '':
    SELECT_sql3 = "SELECT pdn_odn,od_stock_sku,od_size,od_stock,od_price,od_status,update_time FROM "+str(table3)+" WHERE pdn='"+str(pdn)+"' ORDER BY pdn,odn ASC;"
  else:
    SELECT_sql3 = "SELECT pdn_odn,od_stock_sku,od_size,od_stock,od_price,od_status,update_time FROM "+str(table3)+" ORDER BY pdn,odn ASC;"
  curs3.execute(SELECT_sql3)
  Prod_od_List_SP = curs3.fetchall()

  return Prod_od_List_SP


# route : /update_od_IN_quantity_SP
def update_od_IN_quantity_SP_fn(pdn):
  import pymysql
  current_Month = datetime.today().strftime("%m")
  class db_con:
    host = config['DBSET']['HOST']
    port = config['DBSET']['PORT']
    user = config['DBSET']['USER']
    passwd = config['DBSET']['PASSWD']
    db = 'MALDEN_2021_'+current_Month
    char = config['DBSET']['CHAR']

  conn = pymysql.connect(host=db_con.host, port=db_con.port, user=db_con.user, password=db_con.passwd, db=db_con.db, charset=db_con.char, autocommit=True)
  curs4 = conn.cursor(pymysql.cursors.DictCursor)
  current_Day = datetime.today().strftime("%d")

  table4 = "Product_IN_"+current_Day
  if pdn != '':
    SELECT_sql4 = "SELECT custom_prod_code, size, quantity, insert_time FROM "+str(table4)+" WHERE confirm = 'NO' ORDER BY insert_time DESC;"
    curs4.execute(SELECT_sql4)
    Prod_IN = curs4.fetchall()

    SELECT_sql4 = "SELECT COUNT(*) FROM "+str(table4)+" WHERE confirm = 'NO';"
    curs4.execute(SELECT_sql4)
    Prod_IN_Row = curs4.fetchall()
  else:
    SELECT_sql4 = "SELECT custom_prod_code, size, quantity, insert_time FROM "+str(table4)+" WHERE confirm = 'NO' ORDER BY insert_time DESC;"
    curs4.execute(SELECT_sql4)
    Prod_IN = curs4.fetchall()

    SELECT_sql4 = "SELECT COUNT(*) FROM "+str(table4)+" WHERE confirm = 'NO';"
    curs4.execute(SELECT_sql4)
    Prod_IN_Row = curs4.fetchall()
  
  return Prod_IN_Row+Prod_IN


# route : /update_od_OUT_quantity_SP
def update_od_OUT_quantity_SP_fn(pdn):
  import pymysql
  current_Month = datetime.today().strftime("%m")
  class db_con:
    host = config['DBSET']['HOST']
    port = config['DBSET']['PORT']
    user = config['DBSET']['USER']
    passwd = config['DBSET']['PASSWD']
    db = 'MALDEN_2021_'+current_Month
    char = config['DBSET']['CHAR']
  conn2 = pymysql.connect(host=db_con.host, port=db_con.port, user=db_con.user, password=db_con.passwd, db=db_con.db, charset=db_con.char, autocommit=True)
  curs5 = conn2.cursor(pymysql.cursors.DictCursor)
  current_Day = datetime.today().strftime("%d")

  if pdn != '':
    table5 = "Product_OUT_"+current_Day
    SELECT_sql5 = "SELECT custom_prod_code, size, quantity, insert_time FROM "+str(table5)+" WHERE confirm = 'NO' ORDER BY insert_time DESC;"
    curs5.execute(SELECT_sql5)
    Prod_OUT = curs5.fetchall()

    SELECT_sql5 = "SELECT COUNT(*) FROM "+str(table5)+" WHERE confirm = 'NO';"
    curs5.execute(SELECT_sql5)
    Prod_OUT_Row = curs5.fetchall()
  else:
    table5 = "Product_OUT_"+current_Day
    SELECT_sql5 = "SELECT custom_prod_code, size, quantity, insert_time FROM "+str(table5)+" WHERE confirm = 'NO' ORDER BY insert_time DESC;"
    curs5.execute(SELECT_sql5)
    Prod_OUT = curs5.fetchall()

    SELECT_sql5 = "SELECT COUNT(*) FROM "+str(table5)+" WHERE confirm = 'NO';"
    curs5.execute(SELECT_sql5)
    Prod_OUT_Row = curs5.fetchall()

  return Prod_OUT_Row+Prod_OUT

## SP(세트, 기획, 이벤트) 상품 END ##