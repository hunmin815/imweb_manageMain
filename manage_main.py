from flask import Flask, app, render_template, request, url_for, flash, session
from datetime import datetime
from time import sleep
from pymysql import NUMBER, STRING
from werkzeug.utils import escape, redirect
import imweb_api2
import imweb_api_SP
import db_conn
import update_Prod_List
import json
import hashlib
import importlib
import configparser
# from json import JSONEncoder

config = configparser.ConfigParser()
config.read('config.ini')

application = Flask(__name__)
application.secret_key = 'ABCDEFGHIJKL_Malden'

@application.route("/")
def index():
  importlib.reload(db_conn)
  db_admin = ''                                                                                 # admin 여부
  if ('userid' in session) and ('user_key' in session):
    session_user_id = '%s' % escape(session['userid'])
    session_user_key = '%s' % escape(session['user_key'])
    db_conn.conn3
    db_conn.curs3

    table = "user_account"
    SELECT_sql = "select user_num, admin from " + table + " where id = '"+session_user_id+"';"
    try:
      db_conn.curs3.execute(SELECT_sql)
      user_num_rows = db_conn.curs3.fetchall()
      sleep(0.1)
      db_user_num = user_num_rows[0]['user_num']
      db_admin = str(user_num_rows[0]['admin'])
      user_num = db_user_num  
    except:
      return render_template("Login.html")
  else:
    return render_template("Login.html")
  
  if db_admin == '1':
    return render_template("manage.html", user_id = session_user_id, user_key = session_user_key, url = "https://manage.lnksdev.com")
  else:
    flash("허가되지 않은 사용자입니다.\\n지속적인 로그인 시도 시 차단될 수 있습니다.")
    return redirect('/logout')


# 로그인 체크 START
@application.route("/login" , methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    str = ""
    salt = config['LOGIN']['SALT']
    user_id = request.form['user_id']
    user_pw = request.form['user_pw']
    str = user_pw
    user_crypt = hashlib.sha512((str+salt).encode('utf8')).hexdigest()
    user_crypt2 = hashlib.sha512((user_crypt).encode('utf8')).hexdigest()

    db_conn.conn3
    db_conn.curs3

    table = "user_account"
    SELECT_sql = "select * from " + table + " where id = '"+user_id+"';"
    try:
      if db_conn.curs3.execute(SELECT_sql) != "0":
        user_account_rows = db_conn.curs3.fetchall()
        sleep(0.1)
        db_user_pw = user_account_rows[0]['password']
        db_admin = user_account_rows[0]['admin']

        if int(db_admin) != 1: # 관리자 여부
          flash("허가되지 않은 사용자입니다.\\n지속적인 로그인 시도 시 차단될 수 있습니다.")
          return redirect('/')
        elif (user_crypt2 == db_user_pw) and int(db_admin) == 1:
          session['userid'] = user_id
          session['user_key'] = user_crypt2
          return redirect('/manage')
        else:
          flash("아이디가 존재하지 않거나 비밀번호가 잘못되었습니다")
          return redirect('/')
      else:
        flash("아이디가 존재하지 않거나 비밀번호가 잘못되었습니다")
        return redirect('/')
    except:
      flash("아이디가 존재하지 않거나 비밀번호가 잘못되었습니다")
      return redirect('/')
  else:
    flash("잘못된 접근입니다.")
    return redirect('/')
# 로그인 체크 END

# 로그아웃 START
@application.route("/logout")
def logout():
  try:
    session.pop('userid', None)
    session.pop('user_key', None)
    return redirect('/')
  except:
    session.pop('userid', None)
    session.pop('user_key', None)
    return redirect('/')
# 로그아웃 END

# 재고 관리(manage) 페이지 구성 START #
@application.route("/manage")
def manage():
  db_admin = ''                                                                                 # admin 여부
  if ('userid' in session) and ('user_key' in session):
    session_user_id = '%s' % escape(session['userid'])
    session_user_key = '%s' % escape(session['user_key'])
    db_conn.conn3
    db_conn.curs3

    table = "user_account"
    SELECT_sql = "select user_num, admin from " + table + " where id = '"+session_user_id+"';"
    try:
      db_conn.curs3.execute(SELECT_sql)
      user_num_rows = db_conn.curs3.fetchall()
      sleep(0.1)
      db_user_num = user_num_rows[0]['user_num']
      db_admin = str(user_num_rows[0]['admin'])
      user_num = db_user_num  
    except:
      flash("로그인 후 이용가능합니다.")
      return redirect('/logout')
  else:
    flash("로그인 후 이용가능합니다.")
    return redirect('/logout')
  
  if db_admin == '1':
    return render_template("manage.html", user_id = session_user_id, user_key = session_user_key, url = "https://manage.lnksdev.com")
  else:
    flash("허가되지 않은 사용자입니다.\\n지속적인 로그인 시도 시 차단될 수 있습니다.")
    return redirect('/logout')


@application.route("/manage/SP_detail", methods=['POST', 'GET'])
def SP_detail():
  if request.method == 'GET':
    db_admin = ''                                                                                 # admin 여부
    if ('userid' in session) and ('user_key' in session):
      session_user_id = '%s' % escape(session['userid'])
      session_user_key = '%s' % escape(session['user_key'])
      db_conn.conn3
      db_conn.curs3

      table = "user_account"
      SELECT_sql = "select user_num, admin from " + table + " where id = '"+session_user_id+"';"
      try:
        db_conn.curs3.execute(SELECT_sql)
        user_num_rows = db_conn.curs3.fetchall()
        sleep(0.1)
        db_user_num = user_num_rows[0]['user_num']
        db_admin = str(user_num_rows[0]['admin'])
        user_num = db_user_num  
      except:
        flash("로그인 후 이용가능합니다.")
        return redirect('/logout')
    else:
      flash("로그인 후 이용가능합니다.")
      return redirect('/logout')

    if db_admin == '1':
      select_pdn = request.args.get('pdn')
      try:
        table = "Product_List_SP"
        SELECT_sql = "select prod_name from " + table + " where prod_no = '"+str(select_pdn)+"';"
        db_conn.conn2
        db_conn.curs2.execute(SELECT_sql)
        result_row = db_conn.curs2.fetchall()
        DB_prod_name = result_row[0]['prod_name']

        return render_template("manage_detail.html" , user_id = session_user_id, user_key = session_user_key, url = "https://manage.lnksdev.com", prod_name = DB_prod_name)
      except:
        flash("잠시 후 다시 시도해주세요.")
        return redirect('/manage')
    else:
      flash("허가되지 않은 사용자입니다.\\n지속적인 로그인 시도 시 차단될 수 있습니다.")
      return redirect('/logout')

# 동기화 표시
@application.route("/sync_now", methods=['POST', 'GET'])
def sync_update():
  if request.method == 'GET':
    sync_now = json.dumps(update_Prod_List.update_sync_now_fn(), ensure_ascii=False, default=str).encode('utf8')
    
    return sync_now

# 상품 전체 행 수
@application.route("/Product_Rows", methods=['POST', 'GET'])
def Row():
  if request.method == 'GET':
    Product_Rows = json.dumps(update_Prod_List.update_Prod_Rows_fn(), ensure_ascii=False, default=str).encode('utf8')
    
    return Product_Rows

# 상품 리스트 조회
@application.route("/update_Prod_List", methods=['POST', 'GET'])
def update():
  if request.method == 'GET':
    Product_List = json.dumps(update_Prod_List.update_Prod_List_fn(), ensure_ascii=False, default=str).encode('utf8')
    
    return Product_List

# 상품 상세옵션 조회
@application.route("/update_Prod_od_List", methods=['POST', 'GET'])
def update2():
  if request.method == 'GET':
    Prod_od_List = json.dumps(update_Prod_List.update_Prod_od_List_fn(), ensure_ascii=False, default=str).encode('utf8')
    
    return Prod_od_List

# 상품 입고 수량 조회
@application.route("/update_IN_quantity", methods=['POST', 'GET'])
def update3():
  if request.method == 'GET':
    try:
      Prod_IN_and_Row = json.dumps(update_Prod_List.update_IN_quantity_fn(), ensure_ascii=False, default=str).encode('utf8')
    except Exception as e:
      # print(e)
      Prod_IN_and_Row = """[{"COUNT(*)": 0}]"""
      return str(Prod_IN_and_Row)
    return Prod_IN_and_Row

# 상품 출고 수량 조회
@application.route("/update_OUT_quantity", methods=['POST', 'GET'])
def update4():
  if request.method == 'GET':
    try:
      Prod_OUT_and_Row = json.dumps(update_Prod_List.update_OUT_quantity_fn(), ensure_ascii=False, default=str).encode('utf8')
    except Exception as e:
      # print(e)
      Prod_OUT_and_Row = """[{"COUNT(*)": 0}]"""
      return str(Prod_OUT_and_Row)
    return Prod_OUT_and_Row


## SP(세트, 기획, 이벤트) 상품 START ##
# SP 상품 전체 행 수
@application.route("/Product_Rows_SP", methods=['POST', 'GET'])
def SP_Row():
  if request.method == 'GET':
    pdn = str(request.args.get('pdn'))
    if pdn != "None":
      Product_Rows_SP = json.dumps(update_Prod_List.update_Prod_Rows_SP_fn(pdn), ensure_ascii=False, default=str).encode('utf8')
    else:
      Product_Rows_SP = json.dumps(update_Prod_List.update_Prod_Rows_SP_fn(''), ensure_ascii=False, default=str).encode('utf8')
    
    return Product_Rows_SP

# SP 상품 전체 재고 조회
@application.route("/update_Prod_Total_Stock_SP", methods=['POST', 'GET'])
def SP_update0():
  if request.method == 'GET':
    Prod_Total_Stock_SP = json.dumps(update_Prod_List.update_Prod_Total_Stock_SP_fn(), ensure_ascii=False, default=str).encode('utf8')
    
    return Prod_Total_Stock_SP

# SP 상품 리스트 조회
@application.route("/update_Prod_List_SP", methods=['POST', 'GET'])
def SP_update1():
  if request.method == 'GET':
    pdn = str(request.args.get('pdn'))
    if pdn != "None":
      Product_List_SP = json.dumps(update_Prod_List.update_Prod_List_SP_fn(pdn), ensure_ascii=False, default=str).encode('utf8')
    else:
      Product_List_SP = json.dumps(update_Prod_List.update_Prod_List_SP_fn(''), ensure_ascii=False, default=str).encode('utf8')
    return Product_List_SP

# SP 상품 상세옵션 조회
@application.route("/update_Prod_od_List_SP", methods=['POST', 'GET'])
def SP_update2():
  if request.method == 'GET':
    pdn = str(request.args.get('pdn'))
    if pdn != "None":
      Prod_od_List_SP = json.dumps(update_Prod_List.update_Prod_od_List_SP_fn(pdn), ensure_ascii=False, default=str).encode('utf8')
    else:
      Prod_od_List_SP = json.dumps(update_Prod_List.update_Prod_od_List_SP_fn(''), ensure_ascii=False, default=str).encode('utf8')
    
    return Prod_od_List_SP

# SP 상품 상세옵션 입고 조회
@application.route("/update_od_IN_quantity_SP", methods=['POST', 'GET'])
def SP_update3():
  if request.method == 'GET':
    pdn = str(request.args.get('pdn'))
    try:
      if pdn != "None":
        Prod_IN_and_Row_SP = json.dumps(update_Prod_List.update_od_IN_quantity_SP_fn(pdn), ensure_ascii=False, default=str).encode('utf8')
      else:
        Prod_IN_and_Row_SP = json.dumps(update_Prod_List.update_od_IN_quantity_SP_fn(''), ensure_ascii=False, default=str).encode('utf8')
    except Exception as e:
      # print(e)
      Prod_IN_and_Row_SP = """[{"COUNT(*)": 0}]"""
      return str(Prod_IN_and_Row_SP)
    return Prod_IN_and_Row_SP

# SP 상품 상세옵션 출고 조회
@application.route("/update_od_OUT_quantity_SP", methods=['POST', 'GET'])
def SP_update4():
  if request.method == 'GET':
    pdn = str(request.args.get('pdn'))
    try:
      if pdn != "None":
        Prod_OUT_and_Row_SP = json.dumps(update_Prod_List.update_od_OUT_quantity_SP_fn(pdn), ensure_ascii=False, default=str).encode('utf8')
      else:
        Prod_OUT_and_Row_SP = json.dumps(update_Prod_List.update_od_OUT_quantity_SP_fn(''), ensure_ascii=False, default=str).encode('utf8')
    except Exception as e:
      # print(e)
      Prod_OUT_and_Row_SP = """[{"COUNT(*)": 0}]"""
      return str(Prod_OUT_and_Row_SP)
    return Prod_OUT_and_Row_SP
## SP(세트, 기획, 이벤트) 상품 END ##

# 아임웹 동기화 START
@application.route("/imweb_sync", methods=['POST', 'GET'])
def sync():
  if request.method == 'POST':
    db_admin = ''                                                                                 # admin 여부
    if 'userid' in session:
      session_user_id = '%s' % escape(session['userid'])
      session_user_key = '%s' % escape(session['user_key'])
      db_conn.conn3
      db_conn.curs3

      table = "user_account"
      SELECT_sql = "select user_num, admin from " + table + " where id = '"+session_user_id+"';"
      db_conn.curs3.execute(SELECT_sql)
      user_num_rows = db_conn.curs3.fetchall()
      sleep(0.05)  
      db_user_num = user_num_rows[0]['user_num']
      db_admin = str(user_num_rows[0]['admin'])
      user_num = db_user_num
    else:
      flash("로그인 후 이용가능합니다.")
      return redirect('/logout')
    
    if db_admin == '1':
      sleep(0.1)
      # POST_ck_count = request.form['hidden_ck_count']
      POST_ck_od_Row = request.form['hidden_ck_od_Row']
      current_FullYear = datetime.today().strftime("%Y")                                                      # 현재 년(2021)
      current_Month = datetime.today().strftime("%m")                                                         # 현재 월(08)
      Day = datetime.today().strftime("%d")                                                                   # 현재 일(20)

      for i in range(int(POST_ck_od_Row)):
        if (request.form['hidden_ck_pdn_odn_'+str(i)] != "0" and request.form['hidden_ck_in_quantity_'+str(i)] != "0") or (request.form['hidden_ck_pdn_odn_'+str(i)] != "0" and request.form['hidden_ck_out_quantity_'+str(i)] != "0"):
          POST_ck_pdn_odn = request.form['hidden_ck_pdn_odn_'+str(i)].split('-')
          # POST_ck_od_stock_sku = request.form['hidden_ck_od_stock_sku_'+str(i)]
          POST_ck_size = request.form['hidden_ck_size_'+str(i)]
          POST_ck_in_quantity = request.form['hidden_ck_in_quantity_'+str(i)]
          POST_ck_out_quantity = request.form['hidden_ck_out_quantity_'+str(i)]
          POST_ck_in_insert_time = request.form['in_insert_time_'+str(i)]
          POST_ck_out_insert_time = request.form['out_insert_time_'+str(i)]
          
          UPDATE_sql = "UPDATE Product_List SET sync_now='1' WHERE prod_no='"+str(POST_ck_pdn_odn[0])+"';"
          db_conn.curs2.execute(UPDATE_sql)

          sync_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")                                              # 동기화 시작 시간
          imweb_api2.run_api(str(POST_ck_pdn_odn[0]), str(POST_ck_pdn_odn[1]), str(POST_ck_size), int(POST_ck_in_quantity), int(POST_ck_out_quantity), str(POST_ck_in_insert_time), str(POST_ck_out_insert_time), str(sync_time), str(session_user_id), str(current_FullYear), str(current_Month), str(Day))
   
      UPDATE_sql = "UPDATE Product_List SET sync_now='0';"
      db_conn.curs2.execute(UPDATE_sql)

      ## SP 상품 동기화 START ##        
      POST_ck_Prod_Row = request.form['hidden_ck_Prod_Row_SP']
      for i in range(int(POST_ck_Prod_Row)):
        if (request.form['hidden_ck_pdn_'+str(i)+'_SP'] != "0" and request.form['hidden_ck_in_quantity_'+str(i)+'_SP'] != "0") or (request.form['hidden_ck_pdn_'+str(i)+'_SP'] != "0" and request.form['hidden_ck_out_quantity_'+str(i)+'_SP'] != "0"):
          POST_ck_pdn_SP = request.form['hidden_ck_pdn_'+str(i)+'_SP']
          POST_ck_in_quantity_SP = request.form['hidden_ck_in_quantity_'+str(i)+'_SP']
          POST_ck_out_quantity_SP = request.form['hidden_ck_out_quantity_'+str(i)+'_SP']
          try:
            table = "Product_List_SP"
            SELECT_sql = "select custom_prod_code from " + table + " where prod_no = '"+str(POST_ck_pdn_SP)+"';"
            db_conn.conn2
            db_conn.curs2.execute(SELECT_sql)
            db_C_prod_code_SP = db_conn.curs2.fetchall()
          except:
            flash("등록되지 않은 상품입니다.\\n확인 후 다시 시도해 주세요")
            return render_template("manage.html", user_id = session_user_id, user_key = session_user_key, url = "https://manage.lnksdev.com")
          else:
            UPDATE_sql = "UPDATE Product_List_SP SET sync_now='1' WHERE prod_no='"+str(POST_ck_pdn_SP)+"';"
            db_conn.curs2.execute(UPDATE_sql)
              
            sync_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")                                              # 동기화 시작 시간
            imweb_api_SP.run_api_SP(str(POST_ck_pdn_SP), str(db_C_prod_code_SP[0]['custom_prod_code']),int(POST_ck_in_quantity_SP), int(POST_ck_out_quantity_SP), str(sync_time), str(session_user_id), str(current_FullYear), str(current_Month), str(Day))
        ## SP 상품 동기화 END ##

      UPDATE_sql = "UPDATE Product_List_SP SET sync_now='0';"
      db_conn.curs2.execute(UPDATE_sql)

      return render_template("manage.html", user_id = session_user_id, user_key = session_user_key, url = "https://manage.lnksdev.com")
    else:
      flash("허가되지 않은 사용자입니다.")
      return redirect('/logout')
  else:
      flash("잘못된 접근입니다.")
      return redirect('/logout')


## SP_detail 동기화 ##
@application.route("/imweb_sync_SP_detail", methods=['POST', 'GET'])
def sync_SP_detail():
  if request.method == 'POST':
    db_admin = ''                                                                                 # admin 여부
    if 'userid' in session:
      session_user_id = '%s' % escape(session['userid'])
      session_user_key = '%s' % escape(session['user_key'])
      db_conn.conn3
      db_conn.curs3

      table = "user_account"
      SELECT_sql = "select user_num, admin from " + table + " where id = '"+session_user_id+"';"
      db_conn.curs3.execute(SELECT_sql)
      user_num_rows = db_conn.curs3.fetchall()
      sleep(0.05)  
      db_user_num = user_num_rows[0]['user_num']
      db_admin = str(user_num_rows[0]['admin'])
      user_num = db_user_num
    else:
      flash("로그인 후 이용가능합니다.")
      return redirect('/logout')
    
    if db_admin == '1':
      sleep(0.1)
      # POST_ck_count = request.form['hidden_ck_count']
      POST_ck_od_Row_SP = request.form['hidden_ck_od_Row_SP']                                                 # 상품 행 수
      current_FullYear = datetime.today().strftime("%Y")                                                      # 현재 년(2021)
      current_Month = datetime.today().strftime("%m")                                                         # 현재 월(08)
      Day = datetime.today().strftime("%d")                                                                   # 현재 일(20)

      for i in range(int(POST_ck_od_Row_SP)):
        if (request.form['hidden_ck_pdn_odn_'+str(i)+'_SP'] != "0" and request.form['hidden_ck_in_quantity_'+str(i)+'_SP'] != "0") or (request.form['hidden_ck_pdn_odn_'+str(i)+'_SP'] != "0" and request.form['hidden_ck_out_quantity_'+str(i)+'_SP'] != "0"):
          POST_ck_pdn_odn_SP = request.form['hidden_ck_pdn_odn_'+str(i)+'_SP'].split('-') # pdn : 상품 번호, odn : 상세 옵션번호
          POST_ck_size_SP = request.form['hidden_ck_size_'+str(i)+'_SP']
          POST_ck_in_quantity_SP = request.form['hidden_ck_in_quantity_'+str(i)+'_SP']
          POST_ck_out_quantity_SP = request.form['hidden_ck_out_quantity_'+str(i)+'_SP']
          sync_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")                                              # 동기화 시작 시간
          imweb_api_SP.run_api_SP_detail(str(POST_ck_pdn_odn_SP[0]), str(POST_ck_pdn_odn_SP[1]), str(POST_ck_size_SP), int(POST_ck_in_quantity_SP), int(POST_ck_out_quantity_SP), str(sync_time), str(session_user_id), str(current_FullYear), str(current_Month), str(Day))
      
      return redirect(url_for('SP_detail', pdn=str(request.form['hidden_ck_Prod_num'])))
      # return render_template("manage_detail.html", user_id = session_user_id, user_key = session_user_key, url = "https://manage.lnksdev.com")
    else:
      flash("허가되지 않은 사용자입니다.")
      return redirect('/logout')
  else:
      flash("잘못된 접근입니다.")
      return redirect('/logout')
# 아임웹 동기화 END
# 재고 관리(manage) 페이지 구성 END #


if __name__ == "__main__":
    application.run(host='0.0.0.0')
    # application.run(debug=True)
    
