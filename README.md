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
    1. Python 설치
      Python을 설치하지 않았다면 [여기](https://www.python.org/downloads/) 에서 설치할 수 있습니다.

    2. 패키지지 설치
      터미널에서 다음 명령어를 실행하여 appium python 클라이언트 패키지를 설치합니다:
      pip install appium-python-client html-testRunner


    3. Appium 서버 설치 및 실행 
      - Appium gui server를 설치하지 않았다면 [여기](https://github.com/appium/appium-desktop/releases) 에서 설치합니다.
      - Appium 서버를 실행합니다.
      appium


    4. 안드로이드 디바이스 설정
      1. 갤럭시 S24 이상의 단말의 경우, 설정 > 보안 및 개인정보 보호 > 보안 위험 자동 차단을 OFF 합니다.
      2. 안드로이드 디바이스에서 개발자 옵션을 활성화하고 USB 디버깅을 켭니다.
      3. 디바이스를 PC에 연결합니다.
    
    
  ## 테스트 실행하기기
    터미널에서 python SamCalcTest.py, 또는 IDE에서 Run을 실행합니다.
    리포트는 samCaclTestReport 폴더에 생성됩니다.

  ## 테스트 설명
    ### 주요 테스트 케이스
      기본 연산
      test_plus
      test_minus
      test_devision
      test_multi
      각 함수는 사칙 연산 기호의 동작을 테스트합니다.

    ### 예외 및 제약 조건
      test_numover: 연산자 기호 없이 15자리의 연속된 숫자 입력 시 15자리 초과 입력 시 입력 무시와 스낵바 알림 팝업에 대한 테스트
      test_history: 계산 버튼을 통해 계산한 식이 20개를 초과하였을 경우 가장 먼저 계산된 식의 삭제와 가장 마지막에 계산된 식의 추가에 대한 테스트
    고급 기능
      test_sciencalc: 공학용 모드의 연산자가 올바르게 입력되는지에 대한 테스트