## 시스템보안 기말 프로젝트
---

+ 파일탐색기 + 보안기능 추가
  + 파일탐색기
    + 일반적인 파일탐색기 기능 구현
    + 폴더 선택, 파일 열기, 삭제 등 기본적인 기능들 구현

  + 확장자 검사
    + 파일 탐색기에서 추가로 숨겨진 확장자 검사 기능 구현
    + python magic을 이용한 파일 시그니쳐를 분석하여 실제 확장자 확인
      + https://pypi.org/project/python-magic/
      - 한글이름이 들어간 경우 파일 분석 불가 (인코딩하고 보내려했으나 실패)

  - 바이러스 토탈을 이용한 바이러스 검사
    - 바이러스 검사 시 virustotal의 토큰을 사용하여 파일 검사 후 결과 가져오고자 하였음
    - 문제점
      - 동작이 유연하지 않음 (검사 시 다른 행동 불가)
      - 검사 결과가 제대로 반영 안됨
      - 비동기식으로 만드려했으나 실패
  
  - PyQt6로 GUI 제작
    - ```.ui```는 PyQT6로 만든 후 생성된 파일, python 코드는 해당 ui의 동작, 기능들을 구현
    - exe 파일로 변환 시 pyinstaller로 변환 

<br><br>

+ 메인화면
![image](https://github.com/ind2x/gui/assets/52172169/b27a2eb5-78a6-4bba-b644-687f2820f41d)

<br>

+ 파일탐색기
![image](https://github.com/ind2x/gui/assets/52172169/a6c50e7a-0fdb-4f92-9486-ad51e42f4719)

<br>

+ 확장자 검사
![image](https://github.com/ind2x/gui/assets/52172169/70c4ed2f-ff71-47f6-be9e-bd74f499df62)

<br>

+ 바이러스 검사
![image](https://github.com/ind2x/gui/assets/52172169/78c681f0-01c9-47ba-999c-8248524ffaf9)
