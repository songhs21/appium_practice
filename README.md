# 삼성 계산기 테스트 자동화 포트폴리오


  ## 개요
  calc_auto.py는 삼성의 갤럭시 모델 전용 계산기 어플리케이션의 기능을 자동으로 테스트하기 위해 작성된 Python 스크립트입니다. 이 프로젝트는 Appium과 unittest 프레임워크를 사용하여 다양한 계산 기능과 예외 상황을 검증합니다.


  ## 주요 기능
   - **기본 연산 테스트**: 덧셈, 뺄셈, 곱셈, 나눗셈 기능 테스트
   - **공학용 연산자 테스트**: 공학용 모드 전환과 올바른 연산자값 입력 확인 테스트
   - **입력 제약 조건 테스트**: 자리수 및 기호 제한 테스트
   - **사용자 인터페이스 테스트**: 계산 기록 확인과 오래된 계산 기록 삭제 테스트


  ## 기술 스택
   - **언어**: Python
   - **테스트 프레임워크**: unittest, HtmlTestRunner
   - **모바일 자동화 도구**: Appium
   - **기타**: Android SDK, adb
  
  ## 설치 방법
    Python 설치
      Python을 설치하지 않았다면 여기에서 설치하십시오.

    의존성 설치
      다음 명령어를 실행하여 필요한 Python 패키지를 설치합니다:
      pip install appium-python-client html-testRunner
    
    Appium 서버 설치 및 실행
      Appium Desktop 또는 npm을 통해 Appium을 설치합니다.
      npm install -g appium
    Appium 서버를 실행합니다.
      appium
    안드로이드 디바이스 설정
      1. 안드로이드 디바이스에서 개발자 옵션을 활성화하고 USB 디버깅을 켭니다.
      2. 디바이스를 PC에 연결합니다.
    테스트 실행 방법
      3. 리포트 없이 실행
    아래 명령어를 사용하여 테스트를 실행합니다:
      python SamCalcTest.py
    HTML 리포트 생성하며 실행
  아래 명령어를 사용하여 HTML 형식의 테스트 리포트를 생성합니다:
    python SamCalcTest.py
    리포트는 samCaclTestReport 폴더에 생성됩니다.

  ## 테스트 설명
    주요 테스트 케이스
      기본 연산
      test_plus: 9 + 7 테스트
      test_minus: 85 - 46 테스트
      test_devision: 30 / 2 테스트
      test_multi: 1.1 * 4 테스트
    예외 및 제약 조건
      test_numover: 15자리 초과 입력 시 알림 확인
      test_history: 계산 기록 20개 초과 시 처리 확인
    고급 기능
      test_sciencalc: 공학용 계산기 모드의 다양한 함수 테스트