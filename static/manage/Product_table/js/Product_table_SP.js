// SP(세트, 기획, 이벤트) 상품 테이블 Script START //

// 상품 행수 최초 생성 및 동기화 폼 생성 START
function Create_od_Row_SP() {
$.ajax({
  url: "/Product_Rows_SP",
  type: "GET",
  // dataType : "json",
  cache: false,
  success: function (Row) {
    var Product_Row_SP = JSON.parse(Row);
    var od_Row_Count_SP = JSON.stringify(Product_Row_SP[0]['COUNT(*)']);               // 세트,기획 상품 상세 옵션 목록 행수 (Prod_od_List_SP)
    var Prod_Row_Count_SP = JSON.stringify(Product_Row_SP[1]['COUNT(*)']);             // 세트,기획 상품 목록 행수 (Product_List_SP)

    for (var i = Number(Prod_Row_Count_SP)-1; i > -1; i--){                              // 값 전달 용 hidden 생성
      var after_Value = `<input type="hidden" id="hidden_ck_pdn_`+i+`_SP" name="hidden_ck_pdn_`+i+`_SP" value="0"/>
                          <input type="hidden" id="hidden_ck_in_quantity_`+i+`_SP" name="hidden_ck_in_quantity_`+i+`_SP" value="0"/>
                          <input type="hidden" id="hidden_ck_out_quantity_`+i+`_SP" name="hidden_ck_out_quantity_`+i+`_SP" value="0"/>`
      $('#hidden_ck_count_SP').after(after_Value);
    }

    $('#hidden_od_Row_SP').val(od_Row_Count_SP);
    $('#hidden_ck_Prod_Row_SP').val(Prod_Row_Count_SP);
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
    url: "/update_Prod_List_SP",
    type: "GET",
    // dataType : "json",
    cache: false,
    success: function (data1) {
      var Prod_List_SP = JSON.parse(data1);                                                    // String 타입 -> Object 타입으로 변환
      var Prod_Row_Count_SP = $('#hidden_Prod_Row_SP').val();

      for (var a = 0; a < Number(Prod_Row_Count_SP); a++){
        var pdn = JSON.stringify(Prod_List_SP[a]['prod_no']).replace(/\"/g, "");
        var c_prod_code = JSON.stringify(Prod_List_SP[a]['custom_prod_code']).replace(/\"/g, ""); // Object 타입 -> String 타입으로 변환
        var prod_name = JSON.stringify(Prod_List_SP[a]['prod_name']).replace(/\"/g, "");                                     // 상품 이름
        var image_url = "https://cdn.imweb.me/upload/"+JSON.stringify(Prod_List_SP[a]['image_url']).replace(/\"/g, "");      // 상품 사진
        // var od_size = JSON.stringify(Prod_List_SP[a]['od_size']).replace(/\"/g, "");
        var price = JSON.stringify(Prod_List_SP[a]['price']).replace(/\"/g, "");
        // var od_stock = JSON.stringify(Prod_List_SP[a]['od_stock']).replace(/\"/g, "");
        var prod_status = JSON.stringify(Prod_List_SP[a]['prod_status']).replace(/\"/g, "").toUpperCase();
        var append_Value2 = `<tr class="alert" role="alert" style="cursor: pointer;">
                            <td style="padding:15px;" align="center" id="id_tdck_`+String(a)+`_SP">
                              <label class="checkbox-wrap checkbox-primary">
                                <input type="checkbox" id="ck_`+String(a)+`_SP" value="`+pdn+`" tabindex="-1">
                                <span class="checkmark"></span>
                              </label>
                            </td>
                            <td align="center" class=`+String(a)+`_SP style="cursor: text;">
                              <span id="id_pdn_`+String(a)+`_SP"></span>
                            </td>
                            <td width=30px; class=`+String(a)+`_SP title="상품 상세보기">
                              <div class="img" id="id_image_url_`+String(a)+`_SP"></div>
                            </td>
                            <td width=300px; class=`+String(a)+`_SP title="상품 상세보기">
                              <div class="email" id="id_c_prod_code_`+String(a)+`_SP">
                              </div>

                            </td>
                            <td align="center" id="id_price_`+String(a)+`_SP" title="상품 상세보기"></td>
                            <td width=110px; align="center" id="id_prod_status_`+String(a)+`_SP" title="상품 상세보기"></td>
                            <td width=170px; class="in_quantity_`+String(a)+`_SP" align="center" style="cursor: default;">
                              <div class="input-group">
                                <input type="text" name="quantity" id="id_in_quantity_`+String(a)+`_SP" class="quantity form-control input-number" value="0" min="0" size="3" style="font-size:11pt" autocomplete="off">
                              </div>
                            </td>
                            <td width=170px; class="out_quantity_`+String(a)+`_SP" align="center" style="cursor: default;">
                              <div class="input-group">
                                <input type="text" name="quantity" id="id_out_quantity_`+String(a)+`_SP" class="quantity form-control input-number" value="0" min="0" size="3" style="font-size:11pt" autocomplete="off">
                              </div>
                            </td>
                          </tr>
                          `;
        $('#id_tbody2').append(append_Value2);
        $('#id_pdn_'+String(a)+'_SP').append(pdn);
        $('#id_c_prod_code_'+String(a)+'_SP').append("<span id=id2_c_prod_code_"+String(a)+"_SP>"+c_prod_code+"</span>");
        // $('#id_od_size_'+String(a)+'_SP').val(od_size);
        $('#id_price_'+String(a)+'_SP').append(CurrencyCommas(price)+"원");
        $('#id_prod_status_'+String(a)+'_SP').append(prod_status);
        $('#id2_c_prod_code_'+String(a)+'_SP').after("<span>"+prod_name+"</span>");
        $('#id_image_url_'+String(a)+'_SP').css('background-image',"url("+image_url+")");
      }
      // 행 클릭 시 체크박스 체크 START //
      $("#id_tbody2").on('click', 'tr', function (e) {
        if ($(e.target).is('label')) return;
        if ($(e.target).is('input[name="quantity"]')) return;
        if ($(e.target).is('td:nth-child(2)') || $(e.target).is('td:nth-child(2) > span')) return;
        if ($(e.target).is('td:nth-child(7)')) return;
        if ($(e.target).is('td:nth-child(n+3):nth-child(-n+6)') || $(e.target).is('td:nth-child(3) > div')|| $(e.target).is('td:nth-child(4) > div > *')){
          var select_pdn = $(this).find('td:nth-child(2) > span').text();
          window.location.href = "/manage/SP_detail?pdn="+String(select_pdn);
          // window.location.href = "/manage/SP_detail";
          return;
          // return;
        } 
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


// SP 현재 재고 출력 START
function update_Prod_Total_Stock_SP() {
  update_Rows_SP();
  $.ajax({
    url: "/update_Prod_Total_Stock_SP",
    type: "GET",
    cache: false,
    success: function (data1) {
      var Prod_Total_Stock_SP = JSON.parse(data1);                                                      // String 타입 -> Object 타입으로 변환
      var Prod_Row_Count_SP = $('#hidden_Prod_Row_SP').val();
      var update_Prod_Row_Count_SP = $('#hidden_update_Prod_Row_SP').val();
      
      // $('#id_Update_time').val("최근 업데이트 시간 : "+update_time_SP);
      
      for (var a = 0; a < Number(Prod_Row_Count_SP); a++) {
        var DB_pdn = JSON.stringify(Prod_Total_Stock_SP[a]['pdn']).replace(/\"/g, "");

        //if ($('#ck_' + String(a)).is(':checked') == false) {                                          // 체크된 상품 제외
          $('#id_prod_stock_' + String(a)+'_SP').remove();
          var after_Value2 = `<td align="center" id="id_prod_stock_` + String(a) + `_SP" style="cursor: text;"></td>`;
          $('#id_prod_status_' + String(a)+'_SP').after(after_Value2);                                  // 판매 상태 뒤에 추가
        //}
      }
      for (var b = 0; b < Number(Prod_Row_Count_SP); b++) {
        var page_pdn = String($('#id_pdn_' + String(b)+'_SP').text());                                  // 이미 페이지에 호출 된 상품번호
        for (var c = 0; c < Number(update_Prod_Row_Count_SP); c++) {
          var DB_pdn = JSON.stringify(Prod_Total_Stock_SP[c]['pdn']).replace(/\"/g, "");                // DB내 호출 된 상품번호
          var Total_stock = JSON.stringify(Prod_Total_Stock_SP[c]['SUM(od_stock)']).replace(/\"/g, ""); // DB내 현재 재고

          //if (od_pdn_odn == pdn_odn && $('#ck_' + String(b)).is(':checked') == false) {               // 이미 호출된 상품번호와 DB내 상품번호와 일치 시, 체크된 상품 제외
          if (page_pdn == DB_pdn) {                                                                     // 이미 호출된 상품번호와 DB내 상품번호와 일치 시
            $('#id_prod_stock_' + String(b)+'_SP').append(CurrencyCommas(Total_stock));                 // 페이지내 호출되어 있는 상품을 찾아 현재 재고 변경
          }
        }
      }
    }
  });
  timerID5 = setTimeout("update_Prod_Total_Stock_SP()", 2000); // 2초 단위로 갱신 처리
}
// SP 현재 재고 출력 END



  // SP(세트, 기획, 이벤트) 상품 테이블 Script END //