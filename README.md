# 재고 관리 페이지

### 로그인 화면 (GIF)
![manage_로그인 화면](https://user-images.githubusercontent.com/15862848/146658003-a2ec2dde-a953-41d0-9da8-e56e6f0ae56c.gif)
- 패스워드는 SHA512 + Salt 방식입니다.
<br><br><br><br><br>

### 메인 페이지 (GIF)
![manage화면](https://user-images.githubusercontent.com/15862848/146658463-f90940f0-425f-4dd5-baa1-a2e0fc02b417.gif)
<br><br><br><br><br>

### 일반 상품 재고 아임웹 동기화 (GIF)
![일반상품동기화](https://user-images.githubusercontent.com/15862848/146658139-42de7a4f-4e1e-49e9-835a-c31901ab3c8e.gif)
- 아임웹과 Open API 통신으로 동기화를 진행합니다.
<br><br><br><br><br>

### 세트 상품 재고 아임웹 동기화 (GIF)
![세트 상품 동기화](https://user-images.githubusercontent.com/15862848/146658182-fbdcf577-8e92-45e5-98b5-d33e0b61bb3a.gif)
- 세트 상품은 옵션 재고가 많아 별도의 페이지를 만들어 관리합니다.
- 상품명 클릭시 상품 상세 페이지로 이동
<br><br><br><br><br>

### 구현된 기능 ✔
- 상품 재고관리 페이지 (상품번호, 상품명, 상품사진, 판매가, 현재 재고, 입고, 출고)
- 아임웹과 연동하여 **상품정보 수집** 프로그램 개발<br>(상품번호, 자체상품코드, 상품명, 판매상태, 판매가, 상품사진, 옵션 상세번호, 옵션 재고번호(SKU), 옵션 재고, 옵션 상태)
- 관리 페이지내 재고표시 (Ajax)
- 항목 체크시 입고, 출고 부분 업데이트가 멈추며 수량 수정 가능 (왼쪽 상단 첫번째 체크박스는 전체 체크 버튼)
- 로그인 페이지 구축 및 연동 (관리자 인증 사용자만 접속 가능)
- QR코드 생성 페이지 구축 및 연동
- 동기화할 상품 체크 -> 동기화 버튼 클릭 -> 아임웹 상품목록에 존재하는 해당 상품 재고 변경됨
- 동기화된 상품 **입출고 이력 별도 저장** 구축
- 동기화하지 않은 상품 -> 매일 23:59에 자동 동기화 처리
- 동기화시 상품수집 당시 정보와 현재 아임웹 재고가 다를 수 있음 -> 동기화시 상품 업데이트 시간을 실시간 체크하여 **싱크**를 맞춤
- 동기화 상태 표시
