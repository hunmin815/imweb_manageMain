
# 아임웹 입출고 동기화 함수
from flask.helpers import flash
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

Domain = "https://api.imweb.me/v2/shop/products/"

def run_api(POST_pdn, POST_odn, POST_size, POST_in_quantity, POST_out_quantity, POST_in_insert_time, POST_out_insert_time, POST_sync_time, POST_user_id, POST_c_FullYear, POST_c_Month, POST_c_Day):
  import requests
  import access_token
  from time import sleep
  import pymysql
  from datetime import datetime

  sync_time = datetime.strptime(str(POST_sync_time), "%Y-%m-%d %H:%M:%S")     # 동기화 시작 시간
  # current_FullYear = datetime.today().strftime("%Y")                          # 현재 년(2021)
  # current_Month = datetime.today().strftime("%m")                             # 현재 월(08)
  # day = datetime.today().strftime("%d")                                       # 현재 일(20)

  class db_con2:
    host = config['DBSET']['HOST']
    port = config['DBSET']['PORT']
    user = config['DBSET']['USER']
    passwd = config['DBSET']['PASSWD']
    db = config['DBSET']['DB_Product']
    char = config['DBSET']['CHAR']
  
  conn2 = pymysql.connect(host=db_con2.host, port=db_con2.port, user=db_con2.user, password=db_con2.passwd, db=db_con2.db, charset=db_con2.char, autocommit=True)
  curs2 = conn2.cursor(pymysql.cursors.DictCursor)

  
  # print("imweb_api2_START")

  # 입출고 처리
  if (POST_in_quantity != 0) or (POST_out_quantity != 0):
    try:
      pdn_odn = str(POST_pdn)+"-"+str(POST_odn)
      table = "Prod_od_List"
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
            sleep(0.01)
            break
          elif int(jsonObject["code"]) == -10:
              flash("수량 입력이 잘못 되었습니다.\\nex)현재 재고보다 더 많은 출고량을 입력한건 아닌지 확인바랍니다.")
              raise
          if int(jsonObject["request_count"]) == 0:
              sleep(0.9)
        sleep(0.1)
      # 동기화 시간 맞추기 END
    except:
      print("!====Sync_ERROR====!")
    else:
      # 동기화 완료 후 Product_IN 테이블 내 동기화 당시 가장 최근 insert_time 이하는 confirm 'OK' 처리
      table = 'Product_List'
      sql = "SELECT custom_prod_code FROM "+str(table)+" WHERE prod_no = '"+str(POST_pdn)+"';"
      curs2.execute(sql)
      custom_prod_code = curs2.fetchall()
      sleep(0.01)
      db_custom_prod_code = custom_prod_code[0]['custom_prod_code']                                               # Product_List 내 custom_prod_code 호출

      if str(POST_in_insert_time) != '':
        table = 'Product_IN_'+POST_c_Day
        db = 'MALDEN_'+POST_c_FullYear+'_'+POST_c_Month
        sql = "UPDATE "+db+"."+str(table)+" SET confirm = 'OK' WHERE custom_prod_code = '"+str(db_custom_prod_code)+"' and size = '"+str(POST_size)+"' and insert_time <= '"+str(POST_in_insert_time)+"';"
        curs2.execute(sql)
        sleep(0.01)
      
      if str(POST_out_insert_time) != '':
        table = 'Product_OUT_'+POST_c_Day
        db = 'MALDEN_'+POST_c_FullYear+'_'+POST_c_Month
        sql = "UPDATE "+db+"."+str(table)+" SET confirm = 'OK' WHERE custom_prod_code = '"+str(db_custom_prod_code)+"' and size = '"+str(POST_size)+"' and insert_time <= '"+str(POST_out_insert_time)+"';"
        curs2.execute(sql)
        sleep(0.01)

      table = 'Stat_Prod_'+POST_c_Day                                                                                    # 입출고 통계 테이블 Insert
      db = 'MALDEN_'+POST_c_FullYear+'_'+POST_c_Month
      sql = "INSERT INTO "+db+"."+str(table)+" VALUES(NULL,'"+str(db_custom_prod_code)+"','"+str(POST_size)+"','"+str(POST_in_quantity)+"','"+str(POST_out_quantity)+"', NOW(),'"+str(POST_user_id)+"');"
      curs2.execute(sql)