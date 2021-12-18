// SP(세트, 기획, 이벤트) 상품 테이블 Script START //
function getURLParams(url) {
  var result = {};
  url.replace(/[?&]{1}([^=&#]+)=([^&#]*)/g, function(s, k, v) { result[k] = decodeURIComponent(v); });
  return result;
}
var URL_pdn = getURLParams(location.search);  // URL 쿼리스트링 추출
// 상품 행수 최초 생성 및 동기화 폼 생성 START
function Create_od_Row_SP() {
  $.ajax({
    url: "/Product_Rows_SP",
    type: "GET",
    data: {"pdn":String(URL_pdn['pdn'])},
    cache: false,
    success: function (Row) {
      var Product_Row_SP = JSON.parse(Row);
      var od_Row_Count_SP = JSON.stringify(Product_Row_SP[0]['COUNT(*)']);               // 세트,기획 상품 상세 옵션 목록 행수 (Prod_od_List_SP)
      var Prod_Row_Count_SP = JSON.stringify(Product_Row_SP[1]['COUNT(*)']);             // 세트,기획 상품 목록 행수 (Product_List_SP)

      for (var i = Number(od_Row_Count_SP)-1; i > -1; i--){                              // 값 전달 용 hidden 생성
        var after_Value = `<input type="hidden" id="hidden_ck_pdn_odn_`+i+`_SP" name="hidden_ck_pdn_odn_`+i+`_SP" value="0"/>
                            <input type="hidden" id="hidden_ck_size_`+i+`_SP" name="hidden_ck_size_`+i+`_SP" value="0"/>
                            <input type="hidden" id="hidden_ck_in_quantity_`+i+`_SP" name="hidden_ck_in_quantity_`+i+`_SP" value="0"/>
                            <input type="hidden" id="hidden_ck_out_quantity_`+i+`_SP" name="hidden_ck_out_quantity_`+i+`_SP" value="0"/>`
        $('#hidden_ck_od_Row_SP').after(after_Value);
      }
      $('#hidden_ck_Prod_num').val(String(URL_pdn['pdn']));
      $('#hidden_od_Row_SP').val(od_Row_Count_SP);
      $('#hidden_ck_od_Row_SP').val(od_Row_Count_SP);
      $('#hidden_Prod_Row_SP').val(Prod_Row_Count_SP);
    }
  });
};
// 상품 행수 최초 생성 및 동기화 폼 생성 END

// 상품 행수 실시간 호출 START
function update_Rows_SP() {
  $.ajax({
    url: "/Product_Rows_SP",
    type: "GET",
    data: {"pdn":String(URL_pdn['pdn'])},
    cache: false,
    success: function (Row) {
      var Product_Row_SP = JSON.parse(Row);
      var od_Row_Count_SP = JSON.stringify(Product_Row_SP[0]['COUNT(*)']);                          // 세트,기획 상품 상세 옵션 목록 행수 (Prod_od_List_SP)
      var Prod_Row_Count_SP = JSON.stringify(Product_Row_SP[1]['COUNT(*)']);                        // 세트,기획 상품 목록 행수 (Product_List_SP)

      $('#hidden_update_Prod_Row_SP').val(Prod_Row_Count_SP);
      $('#hidden_update_od_Row_SP').val(od_Row_Count_SP);
    }
  });
  };
  // 상품 행수 실시간 호출 END


// 상품 리스트 생성 (Prod_od_List_SP) START
function updateData_SP() {
  $.ajax({
    url: "/update_Prod_od_List_SP",
    type: "GET",
    data: {"pdn":String(URL_pdn['pdn'])},
    // dataType : "json",
    cache: false,
    success: function (data1) {
      var Prod_od_List_SP = JSON.parse(data1);                                                    // String 타입 -> Object 타입으로 변환
      var od_SP_Row_Count = $('#hidden_od_Row_SP').val();

      for (var a = 0; a < Number(od_SP_Row_Count); a++){
        var pdn_odn = JSON.stringify(Prod_od_List_SP[a]['pdn_odn']).replace(/\"/g, "");
        var od_stock_sku = JSON.stringify(Prod_od_List_SP[a]['od_stock_sku']).replace(/\"/g, ""); // Object 타입 -> String 타입으로 변환
        var od_size = JSON.stringify(Prod_od_List_SP[a]['od_size']).replace(/\"/g, "");
        var od_price = JSON.stringify(Prod_od_List_SP[a]['od_price']).replace(/\"/g, "");
        var od_stock = JSON.stringify(Prod_od_List_SP[a]['od_stock']).replace(/\"/g, "");
        var od_status = JSON.stringify(Prod_od_List_SP[a]['od_status']).replace(/\"/g, "");
        var append_Value2 = `<tr class="alert" role="alert" style="cursor: pointer;">
                            <td style="padding:15px;" align="center" id="id_tdck_`+String(a)+`_SP">
                              <label class="checkbox-wrap checkbox-primary">
                                <input type="checkbox" id="ck_`+String(a)+`_SP" value="`+pdn_odn+`" tabindex="-1">
                                <span class="checkmark"></span>
                              </label>
                            </td>
                            <td align="center" class=`+String(a)+`_SP>
                              <span id="id_pdn_odn_`+String(a)+`_SP"></span>
                            </td>
                            <td width=30px; class=`+String(a)+`_SP>
                              <div class="img" id="id_image_url_`+String(a)+`_SP"></div>
                            </td>
                            <td width=300px; class=`+String(a)+`_SP>
                              <div class="email" id="id_od_stock_sku_`+String(a)+`_SP">
                              </div>
                              <input type="hidden" id="id_od_size_`+String(a)+`_SP"/>
                            </td>
                            <td align="center" id="id_od_price_`+String(a)+`_SP"></td>
                            <td width=110px; align="center" id="id_od_status_`+String(a)+`_SP"></td>
                          </tr>
                          `;
        $('#id_tbody').append(append_Value2);
        $('#id_pdn_odn_'+String(a)+'_SP').append(pdn_odn);
        $('#id_od_stock_sku_'+String(a)+'_SP').append("<span id=id2_od_stock_sku_"+String(a)+"_SP>"+od_stock_sku+"</span>");
        $('#id_od_size_'+String(a)+'_SP').val(od_size);
        $('#id_od_price_'+String(a)+'_SP').append(CurrencyCommas(od_price)+"원");
        $('#id_od_status_'+String(a)+'_SP').append(od_status);
      }
      // 행 클릭 시 체크박스 체크 START //
      $("#id_tbody").on('click', 'tr', function (e) {
        if ($(e.target).is('label')) return;
        if ($(e.target).is('input[name="quantity"]')) return;
        if ($(e.target).is('td:nth-child(n+8):nth-child(-n+9)')) return;
        var chkbox = $(this).find('td:first-child :checkbox');
        chkbox.prop('checked', !chkbox.prop('checked'));
        page_move = true;
      });
      // 행 클릭 시 체크박스 체크 END //
    }
  });
  // timerID = setTimeout("updateData()", 5000); // 2초 단위로 갱신 처리
};
// 상품 리스트 생성 (Prod_od_List_SP) END

// 상품 리스트 생성 (Product_List) START
function updateData2_SP() {
  $.ajax({
    url: "/update_Prod_List_SP",
    type: "GET",
    data: {"pdn":String(URL_pdn['pdn'])},
    cache: false,
    success: function (data2) {
      var Prod_List = JSON.parse(data2);                      // String 타입 -> Object 타입으로 변환
      var Prod_Row_Count = $('#hidden_Prod_Row_SP').val();
      var od_Row_Count = $('#hidden_od_Row_SP').val();
      
      for (var a = 0; a < Number(Prod_Row_Count); a++){
        var prod_no = JSON.stringify(Prod_List[a]['prod_no']).replace(/\"/g, "");                                         // 상품 번호
        var prod_name = JSON.stringify(Prod_List[a]['prod_name']).replace(/\"/g, "");                                     // 상품 이름
        var image_url = "https://cdn.imweb.me/upload/"+JSON.stringify(Prod_List[a]['image_url']).replace(/\"/g, "");      // 상품 사진

        for (var b = 0; b < Number(od_Row_Count); b++){
          var pdn_odn = String($('#id_pdn_odn_'+String(b)+'_SP').html()).split('-');
          if (prod_no == pdn_odn[0]){
            $('#id2_od_stock_sku_'+String(b)+'_SP').after("<span>"+prod_name+"</span>");
            $('#id_image_url_'+String(b)+'_SP').css('background-image',"url("+image_url+")");
          }
        }
      }
    }
  });
  // timerID2 = setTimeout("updateData2()", 5000); // 2초 단위로 갱신 처리
}
// 상품 리스트 생성 (Product_List) END


// SP 현재 재고 출력 START
function update_Prod_od_List_SP() {
  update_Rows_SP();
  $.ajax({
    url: "/update_Prod_od_List_SP",
    type: "GET",
    data: {"pdn":String(URL_pdn['pdn'])},
    cache: false,
    success: function (data1) {
      var Prod_od_List_SP = JSON.parse(data1);                                                                        // String 타입 -> Object 타입으로 변환
      var od_Row_Count_SP = $('#hidden_od_Row_SP').val();
      var update_od_Row_Count_SP = $('#hidden_update_od_Row_SP').val();
      var update_time_SP = JSON.stringify(Prod_od_List_SP[0]['update_time']).replace(/\"/g, "");
      $('#id_Update_time_SP').val("최근 업데이트 시간 : "+update_time_SP);
      
      for (var a = 0; a < Number(od_Row_Count_SP); a++) {
        var pdn_odn = JSON.stringify(Prod_od_List_SP[a]['pdn_odn']).replace(/\"/g, "");

        //if ($('#ck_' + String(a)).is(':checked') == false) {                                                        // 체크된 상품 제외
          $('#id_od_stock_' + String(a)+'_SP').remove();
          var after_Value2 = `<td align="center" id="id_od_stock_` + String(a) + `_SP"></td>`;
          $('#id_od_status_' + String(a)+'_SP').after(after_Value2);                                                  // 판매 상태 뒤에 추가
        //}
      }
      for (var b = 0; b < Number(od_Row_Count_SP); b++) {
        var od_pdn_odn = String($('#id_pdn_odn_' + String(b)+'_SP').text());                                          // 이미 페이지에 호출 된 상품번호
        for (var c = 0; c < Number(update_od_Row_Count_SP); c++) {
          var pdn_odn = JSON.stringify(Prod_od_List_SP[c]['pdn_odn']).replace(/\"/g, "");                             // DB내 호출 된 상품번호
          var od_stock = JSON.stringify(Prod_od_List_SP[c]['od_stock']).replace(/\"/g, "");                           // DB내 현재 재고

          //if (od_pdn_odn == pdn_odn && $('#ck_' + String(b)).is(':checked') == false) {                             // 이미 호출된 상품번호와 DB내 상품번호와 일치 시, 체크된 상품 제외
          if (od_pdn_odn == pdn_odn) {                                                                                // 이미 호출된 상품번호와 DB내 상품번호와 일치 시
            $('#id_od_stock_' + String(b)+'_SP').append(CurrencyCommas(od_stock));                                    // 페이지내 호출되어 있는 상품을 찾아 현재 재고 변경
          }
        }
      }
    }
  });
  timerID5 = setTimeout("update_Prod_od_List_SP()", 5000); // 2초 단위로 갱신 처리
}
// SP 현재 재고 출력 END


// SP 입고 출고 업데이트 START //
function update_od_IN_quantity_SP() {
  $.ajax({
    url: "/update_od_IN_quantity_SP",
    type: "GET",
    data: {"pdn":String(URL_pdn['pdn'])},
    cache: false,
    success: function (data3) {
      var Prod_IN_and_Row = JSON.parse(data3);                              // String 타입 -> Object 타입으로 변환
      var IN_Row_Count = JSON.stringify(Prod_IN_and_Row[0]['COUNT(*)']);    // Product_IN 테이블 행수
      // console.log("IN_Row_Count : "+IN_Row_Count);
      var od_Row_Count = $('#hidden_od_Row_SP').val();

      for (var c = 0; c < Number(od_Row_Count); c++){
        if($('#ck_' + String(c)+'_SP').is(':checked') == false){
          $('.in_quantity_'+String(c)+'_SP').remove();
          $('#in_insert_time_'+String(c)+'_SP').remove();
          // $('#id_in_quantity_'+String(c)).remove();
          var afterValue = `<td width=170px; class="in_quantity_`+String(c)+`_SP" align="center" style="cursor: default;">
                              <div class="input-group">
                                <input type="text" name="quantity" id="id_in_quantity_`+String(c)+`_SP" class="quantity form-control input-number" value="?" min="0" size="3" style="font-size:11pt" autocomplete="off">
                              </div>
                            </td>`;
          // var afterValue2 = `<input type="hidden" name="in_insert_time_`+String(c)+`_SP" id="in_insert_time_`+String(c)+`_SP"/>`;
          $('#id_od_stock_'+String(c)+'_SP').after(afterValue);
          // $('#hidden_ck_od_Row_SP').after(afterValue2);
        }                                    
      }

      if (IN_Row_Count != "0") {
        for (var a = 0; a < Number(od_Row_Count); a++) {
          if($('#ck_' + String(a)+'_SP').is(':checked') == false){
            var od_stock_sku = String($('#id2_od_stock_sku_' + String(a)+'_SP').text());    // 페이지내 stock_sku 호출
            var in_quantity = 0;

            for (var b = 0; b < Number(IN_Row_Count); b++) {
              var prod_code_size = JSON.stringify(Prod_IN_and_Row[b + 1]['custom_prod_code']).replace(/\"/g, "") + "-" + JSON.stringify(Prod_IN_and_Row[b + 1]['size']).replace(/\"/g, "");
              var prod_in_quantity = JSON.stringify(Prod_IN_and_Row[b + 1]['quantity']).replace(/\"/g, "");   // QR 입고 별 수량
              // var prod_in_insert_time = JSON.stringify(Prod_IN_and_Row[1]['insert_time']).replace(/\"/g, ""); // 가장 최신 QR 입고 날짜
              if (od_stock_sku == prod_code_size) {
                in_quantity += Number(prod_in_quantity);
                // $('#in_insert_time_' + String(a)+'_SP').val(prod_in_insert_time);
              }
            }
              $('#id_in_quantity_' + String(a)+'_SP').val(in_quantity);
          }
        }
      }
      else{
        for (var a = 0; a < Number(od_Row_Count); a++) {
          if($('#ck_' + String(a)+'_SP').is(':checked') == false){
            in_quantity = 0;
            // prod_in_insert_time = '';
            $('#id_in_quantity_' + String(a)+'_SP').val(in_quantity);                      // count가 0이면 0
            // $('#in_insert_time_' + String(a)+'_SP').val(prod_in_insert_time);
          }
        }
      }
    }
  });
  // timerID6 = setTimeout("update_od_IN_quantity_SP()", 3000); // 3초 단위로 갱신 처리
}

function update_od_OUT_quantity_SP() {
  $.ajax({
    url: "/update_od_OUT_quantity_SP",
    type: "GET",
    data: {"pdn":String(URL_pdn['pdn'])},
    cache: false,
    success: function (data4) {
      var Prod_OUT_and_Row = JSON.parse(data4);                      // String 타입 -> Object 타입으로 변환
      var OUT_Row_Count = JSON.stringify(Prod_OUT_and_Row[0]['COUNT(*)']);
      // console.log("OUT_Row_Count : "+OUT_Row_Count);
      var od_Row_Count = $('#hidden_od_Row_SP').val();

      for (var c = 0; c < Number(od_Row_Count); c++){
        if($('#ck_' + String(c)+'_SP').is(':checked') == false){
          $('.out_quantity_'+String(c)+'_SP').remove();
          $('#out_insert_time_'+String(c)+'_SP').remove();
          // $('#id_out_quantity_'+String(c)).remove();
          var afterValue = `<td width=170px; class="out_quantity_`+String(c)+`_SP" align="center" style="cursor: default;">
                              <div class="input-group">
                                <input type="text" name="quantity" id="id_out_quantity_`+String(c)+`_SP" class="quantity form-control input-number" value="?" min="0" size="3" style="font-size:11pt" autocomplete="off">
                              </div>
                            </td>`;
          // var afterValue2 = `<input type="hidden" name="out_insert_time_`+String(c)+`_SP" id="out_insert_time_`+String(c)+`_SP"/>`;
          $('.in_quantity_'+String(c)+'_SP').after(afterValue);
          // $('#sync_btn').before(afterValue2);      
        }                                 
      }

      if (OUT_Row_Count != "0") {
        for (var a = 0; a < Number(od_Row_Count); a++) {
          if($('#ck_' + String(a)+'_SP').is(':checked') == false){
            var od_stock_sku = String($('#id2_od_stock_sku_' + String(a)+'_SP').text());
            var out_quantity = 0;

            for (var b = 0; b < Number(OUT_Row_Count); b++) {
              var prod_code_size = JSON.stringify(Prod_OUT_and_Row[b + 1]['custom_prod_code']).replace(/\"/g, "") + "-" + JSON.stringify(Prod_OUT_and_Row[b + 1]['size']).replace(/\"/g, "");
              var prod_out_quantity = JSON.stringify(Prod_OUT_and_Row[b + 1]['quantity']).replace(/\"/g, "");   // QR 출고 별 수량
              // var prod_out_insert_time = JSON.stringify(Prod_OUT_and_Row[1]['insert_time']).replace(/\"/g, ""); // 가장 최신 QR 출고 날짜
              if (od_stock_sku == prod_code_size) {
                out_quantity += Number(prod_out_quantity);
                // $('#out_insert_time_' + String(a)+'_SP').val(prod_out_insert_time);
              }
            }
              $('#id_out_quantity_' + String(a)+'_SP').val(out_quantity);
          }
        }
      }
      else{
        for (var a = 0; a < Number(od_Row_Count); a++) {
          if($('#ck_' + String(a)+'_SP').is(':checked') == false){
            out_quantity = 0;
            // prod_out_insert_time = '';
            $('#id_out_quantity_' + String(a)+'_SP').val(out_quantity);                         // count가 0이면 0
            // $('#out_insert_time_' + String(a)+'_SP').val(prod_out_insert_time);
          }
        }
      }
    }
  });
  // timerID7 = setTimeout("update_od_OUT_quantity_SP()", 3000); // 3초 단위로 갱신 처리
}

  // SP(세트, 기획, 이벤트) 상품 테이블 Script END //