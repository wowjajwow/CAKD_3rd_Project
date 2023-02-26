모델 데이터를 다운 받아주세요
주소 링크 : https://drive.google.com/file/d/1H4DoSKDtsv_yp-2hkPDAfsMJoqJlcZOT/view?usp=sharing
다운받은 모델 데이터를 model_data 폴더에 넣어주세요


1. 시스템 환경변수에서 venv 폴더를 환경변수로 설정
2. setup으로 필요한 패키지 설치
3. set flask_app=server
4. 기본 포트 5000 방화벽에서 인바운드 규칙 설정 포트 5000번연결 허용
5. flask run --host=0.0.0.0 --with-threads

주의: 아이템이 많은 데이터는 시간이 오래걸리므로 sentnece20과 같은 작은 사이즈의 json파일을 업로드 해주세요.

-유사도-
코사인 유사도를 사용하였고
제목의 유사도와 내용의 유사도 합으로 계산했습니다.
내용은 문단을 모델에 넣어서 임베딩하였습니다.