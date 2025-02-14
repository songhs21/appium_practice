# 삼성 계산기 자동화 테스트 포트폴리오

이 프로젝트는 **삼성 갤럭시 모델 전용 계산기 앱**의 기능을 **Appium과 pytest를 활용하여 자동화 테스트**하는 코드입니다.  
자동화 테스트를 통해 기본적인 사칙연산, 예외 케이스, UI 반응을 검증합니다.

## **프로젝트 개요**
- 대상 앱: **삼성 기본 계산기 앱 (com.sec.android.app.popupcalculator)**
- 플랫폼: **Android**
- 테스트 프레임워크: **pytest**
- 자동화 도구: **Appium**
- 주요 기능:
  - **기본 연산 테스트**: 덧셈, 뺄셈, 곱셈, 나눗셈 기능 테스트
  - **공학용 연산자 테스트**: 공학용 모드 전환 및 올바른 연산자값 입력 확인 테스트
  - **입력 제약 조건 테스트**: 자리수 및 기호 제한 테스트
  - **사용자 인터페이스 테스트**: 계산 기록 확인 및 오래된 계산 기록 삭제 테스트

## **사용 기술**
- **언어**: Python
- **테스트 프레임워크**: pytest
- **모바일 자동화 도구**: Appium
- **기타**: Android SDK, adb

## **설치 방법**
### 1 **Python 설치**
- Python이 설치되어 있지 않다면 [여기](https://www.python.org/downloads/)에서 설치합니다.

### 2️ **필요한 패키지 설치**
```
pip install appium-python-client pytest
```

### 3️ **Appium 서버 설치 및 실행**
- Appium GUI 서버를 설치하지 않았다면 [여기](https://github.com/appium/appium-desktop/releases)에서 설치합니다.
- Appium 서버를 실행합니다.

### 4️ **안드로이드 디바이스 설정**
1. **갤럭시 S24 이상의 단말**: 설정 > 보안 및 개인정보 보호 > 보안 위험 자동 차단을 OFF 합니다.
2. 안드로이드 디바이스에서 개발자 옵션을 활성화하고 USB 디버깅을 켭니다.
3. 디바이스를 PC에 연결합니다.

## ▶ **테스트 실행 방법**
터미널에서 다음 명령어를 실행, 또는 IDE에서 실행하면 됩니다. 
```
pytest --html=samCalcTestReport.html --self-contained-html
```
## **테스트 항목**
### 1 **기본 사칙연산 테스트**
| 테스트 이름 | 설명 |
|------------|--------------------------------|
| `test_addition_operation` | 9 + 9 연산을 검증 |
| `test_subtraction_operation` | 9 - 7 연산을 검증 |
| `test_division_operation` | 9 ÷ 3 연산을 검증 |
| `test_multiplication_operation` | 9 × 3 연산을 검증 |

### 2️ **예외 및 제약 조건 테스트**
| 테스트 이름 | 설명 |
|------------|--------------------------------|
| `test_digit_entry_prevention_after_limit` | 15자리 이상 입력이 차단되는지 테스트 |
| `test_division_by_zero_error` | 0으로 나누는 경우 예외 처리가 되는지 검증 |
| `test_decimal_place_limit` | 소수점 10자리 제한 검증 |
| `test_invalid_character_input_error` | 사용되지 않는 기호 입력 시 오류 메시지가 표시되는지 검증 |
| `test_operator_entry_limit` | 연산자 40개 이상 입력 시 오류가 발생하는지 검증 |
| `test_zero_not_duplicated` | 0의 중복 입력 방지 검증 |
| `test_point_not_duplicated` | 소수점 중복 입력 방지 검증 |
| `test_max_input_length_limit` | 최대 입력 길이(200자) 제한 검증 |

### 3️ **고급 기능 테스트**
| 테스트 이름 | 설명 |
|------------|--------------------------------|
| `test_operator_switching_behavior` | 연산자를 변경할 때 UI가 정상적으로 업데이트되는지 검증 |
| `test_incomplete_expression_with_brackets` | 괄호만 있는 연산 입력 시 예외 처리 검증 |
| `test_unclosed_bracket_error` | 괄호를 닫지 않은 상태에서 계산 시 오류가 발생하는지 확인 |
| `test_parentheses_precedence` | 괄호 연산 우선순위 검증 |
| `test_history_deletion_when_exceeding_20` | 계산 기록이 20개를 초과할 때 오래된 계산식 삭제 여부 검증 |
| `test_scientific_calculator_functions` | 공학용 계산기의 특수 기능(제곱근, 로그 등) 입력 검증 |

## **연계 테스트 케이스**

[삼성 게산기 TC 스프레드 시트](https://docs.google.com/spreadsheets/d/1gk_v2H9F7rUT-uaLtgJ7d6tsBl2hQgLm8aObLsRxWTU/edit?gid=0#gid=0)


해당 테스트 케이스에 수동테스트/자동화테스트 구분을 주어 하나의 테스트 케이스로 관리하고있습니다.


## ⚠ **주의 사항**
- **USB 디버깅을 활성화**한 상태에서 **실제 Android 기기**를 사용해야 합니다.
- 기기의 **화면 해상도에 따라 일부 UI 요소의 위치가 다를 수 있습니다.**
- Appium 서버가 정상적으로 실행되고 있어야 테스트가 작동합니다.

### **기여 및 학습 과정**
이 프로젝트는 Appium을 활용한 자동화 테스트 및 Python 테스트 프레임워크(Pytest) 학습을 통해 개발되었습니다. 테스트 설계, 코드 작성, 리포트 작성까지 모두 직접 수행하였으며, 테스트 기법과 방법론을 활용하여 실제 QA 업무에서 발생할 수 있는 시나리오를 포괄하도록 설계했습니다.

### **테스트 결과 및 이슈 대응**
테스트 실행 후 samCalcTestReport.html 파일에서 결과를 확인할 수 있습니다. 테스트가 간헐적으로 실패하는 경우, 명시적 대기를 강화하여 해결했습니다.

## **문의**
테스트 코드 관련 문의는 songhs21@protonmail.com 통해 연락해 주세요.