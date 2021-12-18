
# SP 아임웹 입출고 동기화 함수
from flask.helpers import flash
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

Domain = "https://api.imweb.me/v2/shop/products/"
class db_con2_SP:
  host = config['DBSET']['HOST']
  port = config['DBSET']['PORT']
  user = config['DBSET']['USER']
  passwd = config['DBSET']['PASSWD']
  db = config['DBSET']['DB_Product']
  char = config['DBSET']['CHAR']

# SP 테이블 동기화 START #
def run_api_SP(POST_pdn, db_C_prod_code_SP, POST_in_quantity, POST_out_quantity, POST_sync_time, POST_user_id, POST_c_FullYear, POST_c_Month, POST_c_Day):
  import requests
  import access_token
  from time import sleep
  import pymysql
  from datetime import datetime

  # sync_time = datetime.strptime(str(POST_sync_time), "%Y-%m-%d %H:%M:%S")     # 동기화 시작 시간
  # current_FullYear = datetime.today().strftime("%Y")                          # 현재 년(2021)
  # current_Month = datetime.today().strftime("%m")                             # 현재 월(08)
  # day = datetime.today().strftime("%d")                                       # 현재 일(20)


  
  conn2 = pymysql.connect(host=db_con2_SP.host, port=db_con2_SP.port, user=db_con2_SP.user, password=db_con2_SP.passwd, db=db_con2_SP.db, charset=db_con2_SP.char, autocommit=True)
  curs2 = conn2.cursor(pymysql.cursors.DictCursor)



  # SP 입출고 처리 #
  if (POST_in_quantity != 0) or (POST_out_quantity != 0):
    try:
      table = "Prod_od_List_SP"
      SELECT_sql = "SELECT COUNT(*) FROM "+str(table)+" WHERE pdn='"+str(POST_pdn)+"';"
      curs2.execute(SELECT_sql)
      db_od_Rows_SP = curs2.fetchall()
      db_od_Rows_SP = db_od_Rows_SP[0]['COUNT(*)']
      sleep(0.01)
      for i in range(int(db_od_Rows_SP)):
        create_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        sync_time = datetime.strptime(str(create_time), "%Y-%m-%d %H:%M:%S")
        # 동기화 시간 맞추기 START
        while 1:    
          SELECT_sql = "SELECT odn,od_size,od_stock,update_time FROM "+str(table)+" WHERE pdn='"+str(POST_pdn)+"' ORDER BY pdn,odn ASC;"
          curs2.execute(SELECT_sql)
          db_result_SP = curs2.fetchall()
          sleep(0.001)
          db_update_time_SP = db_result_SP[i]['update_time']
          # print("sync_time         : "+str(sync_time))
          # print("db_update_time_SP : "+str(db_update_time_SP))
          time1 = datetime.strptime(str(db_update_time_SP), "%Y-%m-%d %H:%M:%S")                     # 상품 update_time 호출
          diff = sync_time <= time1
          if diff == True:
            db_od_stock_SP = db_result_SP[i]['od_stock']
            od_stock = (int(db_od_stock_SP) + int(POST_in_quantity)) - int(POST_out_quantity)               # (DB내 현재 재고 + 입고) - 출고
            db_odn = db_result_SP[i]['odn']
            try:
              payload = ""
              headers = {"access-token": str(access_token.create_token())}
              sleep(0.01)
              url = str(Domain)+str(POST_pdn)+"/options-details/"+str(db_odn)
              querystring = {"stock":str(od_stock)}
              option_response = requests.request("PATCH", url, data=payload, headers=headers, params=querystring)
              jsonObject = option_response.json()
              sleep(0.01)
            except:
              print("Re-request..")
              sleep(0.5)
              pass
            if int(jsonObject["code"]) == 200:
              print("======Sync_OK(imweb)======"+str(POST_pdn)+"-"+str(db_odn)+" : "+str(od_stock))
              table2 = 'Stat_Prod_'+POST_c_Day                                                                                    # 입출고 통계 테이블 Insert
              db = 'MALDEN_'+POST_c_FullYear+'_'+POST_c_Month
              db_od_size_SP = db_result_SP[i]['od_size']
              sql = "INSERT INTO "+db+"."+str(table2)+" VALUES(NULL,'"+str(db_C_prod_code_SP)+"','"+str(db_od_size_SP)+"','"+str(POST_in_quantity)+"','"+str(POST_out_quantity)+"', NOW(),'"+str(POST_user_id)+"');"
              curs2.execute(sql)
              sleep(0.05)
              break
            elif int(jsonObject["code"]) == -10:
              flash("수량 입력이 잘못 되었습니다.\\nex)현재 재고보다 더 많은 출고량을 입력한건 아닌지 확인바랍니다.")
              raise
            if int(jsonObject["request_count"]) == 0:
              sleep(0.9)
          sleep(0.1)
    except:
      print("!====Sync_ERROR_SP====!")
# SP 테이블 동기화 END #


# SP_detail 페이지 동기화 START #
def run_api_SP_detail(POST_pdn, POST_odn, POST_ck_size_SP, POST_in_quantity, POST_out_quantity, POST_sync_time, POST_user_id, POST_c_FullYear, POST_c_Month, POST_c_Day):
  import requests
  import access_token
  from time import sleep
  import pymysql
  from datetime import datetime

  sync_time = datetime.strptime(str(POST_sync_time), "%Y-%m-%d %H:%M:%S")     # 동기화 시작 시간
  
  conn2 = pymysql.connect(host=db_con2_SP.host, port=db_con2_SP.port, user=db_con2_SP.user, password=db_con2_SP.passwd, db=db_con2_SP.db, charset=db_con2_SP.char, autocommit=True)
  curs2 = conn2.cursor(pymysql.cursors.DictCursor)

  # 입출고 처리
  if (POST_in_quantity != 0) or (POST_out_quantity != 0):
    try:
      pdn_odn = str(POST_pdn)+"-"+str(POST_odn)
      table = "Prod_od_List_SP"
      # 동기화 시간 맞추기 START
      while 1:
        sql = "SELECT update_time FROM "+str(table)+" WHERE pdn_odn = '"+str(pdn_odn)+"';"
        curs2.execute(sql)
        db_update_time = curs2.fetchall()     
        sleep(0.001)                      
        time1 = datetime.strptime(str(db_update_time[0]['update_time']), "%Y-%m-%d %H:%M:%S")                     # 상품 update_time 호출
        diff = sync_time <= time1
        if diff == True:
          sql = "SELECT od_stock FROM "+str(table)+" WHERE pdn_odn = '"+str(pdn_odn)+"';"
          curs2.execute(sql)
          db_od_stock = curs2.fetchall()
          sleep(0.01)
          od_stock = (int(db_od_stock[0]['od_stock']) + int(POST_in_quantity)) - int(POST_out_quantity)               # (DB내 현재 재고 + 입고) - 출고
          try:
            payload = ""
            headers = {"access-token": str(access_token.create_token())}
            sleep(0.01)
            url = str(Domain)+str(POST_pdn)+"/options-details/"+str(POST_odn)
            querystring = {"stock":str(od_stock)}
            option_response = requests.request("PATCH", url, data=payload, headers=headers, params=querystring)
            jsonObject = option_response.json()
            sleep(0.01)
          except:
            print("Re-request..")
            sleep(0.5)
            pass
          if int(jsonObject["code"]) == 200:
            print("======Sync_OK(imweb)======"+str(pdn_odn)+" : "+str(od_stock))
            table3 = 'Product_List_SP'
            sql = "SELECT custom_prod_code FROM "+str(table3)+" WHERE prod_no = '"+str(POST_pdn)+"';"
            curs2.execute(sql)
            custom_prod_code = curs2.fetchall()
            sleep(0.01)
            db_custom_prod_code = custom_prod_code[0]['custom_prod_code']

            table2 = 'Stat_Prod_'+POST_c_Day                                                                                    # 입출고 통계 테이블 Insert
            db = 'MALDEN_'+POST_c_FullYear+'_'+POST_c_Month
            sql = "INSERT INTO "+db+"."+str(table2)+" VALUES(NULL,'"+str(db_custom_prod_code)+"','"+str(POST_ck_size_SP)+"','"+str(POST_in_quantity)+"','"+str(POST_out_quantity)+"', NOW(),'"+str(POST_user_id)+"');"
            curs2.execute(sql)
            sleep(0.05)
            break
          elif int(jsonObject["code"]) == -10:
              flash("수량 입력이 잘못 되었습니다.\\nex)현재 재고보다 더 많은 출고량을 입력한건 아닌지 확인 바랍니다.")
              raise
          if int(jsonObject["request_count"]) == 0:
              sleep(0.9)
        sleep(0.1)
      # 동기화 시간 맞추기 END
    except:
      print("!====Sync_ERROR_SPdetail====!")

# SP_detail 페이지 동기화 END #