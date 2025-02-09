#_-_encoding=utf8_-_
#__author__="huiseong.song"

import pytest
import logging
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope='function')
def test_setup_android(request):
    options = AppiumOptions()
    options.set_capability('deviceName', '')
    options.set_capability('platformName', 'Android')
    options.set_capability('appium:appPackage', 'com.sec.android.app.popupcalculator')
    options.set_capability('appium:appActivity', 'com.sec.android.app.popupcalculator.Calculator')

    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
    request.cls.driver = driver

    # 연결된 디바이스 이름 가져오기
    device_name = driver.capabilities.get('deviceName')

    def fin():
        logging.info(f'연결된 디바이스 이름: {device_name}')
        driver.quit()

    request.addfinalizer(fin)
    yield driver

@pytest.mark.usefixtures("test_setup_android")
class TestCalculator:

    SNACKBAR_TEXT_ID = 'com.sec.android.app.popupcalculator:id/snackbar_text'
    FORMULA_ID = 'com.sec.android.app.popupcalculator:id/calc_edt_formula'
    HISTORY = 'com.sec.android.app.popupcalculator:id/calc_history_view_group'
    ACCESSBY = AppiumBy.ACCESSIBILITY_ID
    IDBY = AppiumBy.ID
    width = None
    height = None
    
    # 터치 입력 함수
    def tact(self, act):
        self.driver.find_element(self.ACCESSBY, value=act).click()
        sleep(0.1)

    # 계산식 검증
    def calculate(self, formula):
        self.tact('계산')
        value_text = self.driver.find_element(self.IDBY, value=self.FORMULA_ID).text
        # 공백 제거, 음수의 경우 기호로 교체, 접미사인 계산결과 제거 순으로 문자열 수정 후 결과 값 저장
        value_text = value_text.replace(' ', '')
        if '빼기' in value_text:
            value_text = value_text.replace('빼기', '-')
        value_text = value_text.replace('빼기', '-')
        valueA = int(value_text.replace('계산결과', ''))

        # 괄호를 먼저 처리하는 로직
        while '괄호' in formula:  # 괄호가 있을 때 반복
            # 괄호의 시작과 끝 인덱스 찾기
            start_idx = formula.index('괄호')
            end_idx = formula.index('괄호', start_idx + 1)
            # 괄호 안의 부분 수식 추출
            sub_formula = formula[start_idx + 1:end_idx]  # 괄호 안의 수식
            # 괄호 안의 수식 계산
            sub_value = self.evaluate(sub_formula)
            # 괄호를 계산한 후 수식에 다시 삽입
            formula = formula[:start_idx] + [str(sub_value)] + formula[end_idx + 1:]

        # 괄호를 처리한 후 남은 수식 계산
        valueB = self.evaluate(formula)
        assert valueA == valueB, f'FAIL: 계산 결과는 {valueA}가 아닙니다.'

    # 계산식 계산 후 결과 반환
    def evaluate(self, formula):
        # 먼저 곱셈과 나누기를 처리하기 위해 수식에서 "*"와 "/"를 먼저 처리
        while '곱하기' in formula or '나누기' in formula:
            for i, item in enumerate(formula):
                if item == '곱하기':
                    left = int(formula[i - 1])
                    right = int(formula[i + 1])
                    result = left * right
                    formula = formula[:i - 1] + [str(result)] + formula[i + 2:]
                    break  # 계산한 후에는 다시 반복해서 확인
                elif item == '나누기':
                    left = int(formula[i - 1])
                    right = int(formula[i + 1])
                    result = left / right
                    formula = formula[:i - 1] + [str(result)] + formula[i + 2:]
                    break
        # 그 후에 덧셈과 뺄셈 처리
        while '더하기' in formula or '빼기' in formula:
            for i, item in enumerate(formula):
                if item == '더하기':
                    left = int(formula[i - 1])
                    right = int(formula[i + 1])
                    result = left + right
                    formula = formula[:i - 1] + [str(result)] + formula[i + 2:]
                    break
                elif item == '빼기':
                    left = int(formula[i - 1])
                    right = int(formula[i + 1])
                    result = left - right
                    formula = formula[:i - 1] + [str(result)] + formula[i + 2:]
                    break

        result = float(formula[0])
        return int(result) if result.is_integer() else result

    # 더하기
    def test_addition_operation(self):
        formula = ['9', '더하기', '9']
        for formula_item in formula:
           self.tact(formula_item)
        self.calculate(formula)

    #빼기
    def test_subtraction_operation(self):
        formula = ['9', '빼기', '7']
        for formula_item in formula:
            self.tact(formula_item)
        self.calculate(formula)
        
    #나누기
    def test_division_operation(self):
        formula = ['9', '나누기', '3']
        for formula_item in formula:
           self.tact(formula_item)
        self.calculate(formula)

    #곱하기
    def test_multiplication_operation(self): # asdf
        formula = ['9', '곱하기', '3']
        for formula_item in formula:
           self.tact(formula_item)
        self.calculate(formula)

    # 0으로 나누기
    def test_division_by_zero_error(self):
        expression = ['3', '나누기', '0']
        for item in expression:
            self.tact(item)
        chk = None
        retry_count = 0  # 재시도 횟수
        while chk != '0으로 나눌 수 없어요.':
            self.tact('계산')
            try:
                chk = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((self.IDBY, self.SNACKBAR_TEXT_ID))
            ).text
            except Exception as e:
                pytest.fail(f'발생한 예외: {e}')
            retry_count += 1
            if retry_count >= 10:
                pytest.fail("Snackbar가 나타나지 않았습니다. 최대 반복 횟수를 초과하여 종료합니다.")
        # Snackbar가 정상적으로 나타났으면 테스트 완료
        assert chk == '0으로 나눌 수 없어요.', f'[Faild] Snack Bar가 나타나지 않았거나 지정한 값과 다릅니다. chk{chk}'

    # 괄호가 있는 식에서 괄호 우선 순위 체크
    def test_parentheses_precedence(self):
        formula = ['1', '더하기', '괄호', '2', '빼기', '3', '괄호', '곱하기', '4']
        for item in formula:
            self.tact(item)
        self.calculate(formula)
            
    # 사용되지 않는 기호 및 공백에서 연산 기호 입력 실패 확인
    def test_invalid_character_input_error(self):
        symbol = ['+', '-', '*', '/', '^', 'a', ' ']
        for symbol_item in symbol:
            success = False
            chk = None
            retry_count = 0  # 재시도 횟수
            while chk != '완성되지 않은 수식입니다.' and not success:  # 재시도 횟수를 초과하면 종료
                try:
                    self.driver.find_element(self.IDBY, value=self.FORMULA_ID).send_keys(symbol_item)
                    chk = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((self.IDBY, self.SNACKBAR_TEXT_ID))
            ).text
                    assert chk == '완성되지 않은 수식입니다.', f"[Failed] 입력되지 말아야할 {symbol_item}이 입력 됐거나, chk 값이 다릅니다. chk: {chk}"
                except NoSuchElementException as e:
                # try 동작으로 인해 반복적인 NoSuchElementException 처리
                    pytest.fail(f'[Failed: {symbol_item} 입력 중 스낵바 확인 불가.')
                # 예상치 못한 에러 발생 처리
                except Exception as e:
                    print(f'Failed: 예외 상황이 발생하였습니다. {e}')
                success = True
                retry_count += 1  # 재시도 횟수 증가

                if retry_count >= 5:
                    print(f'{symbol_item}은 최대 반복 횟수 5회를 초과하여 다음 연산 기호로 넘어감.')

    # 연산 기호 40개 초과 체크
    def test_operator_entry_limit(self):
        chk = None
        total_chars = 0
        while total_chars>=40:
           self.tact("2")
           self.tact("나누기")
           total_chars += 1
        
        while chk is None:
            self.tact("2")
            self.tact("나누기")
            try:
                chk = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((self.IDBY, self.SNACKBAR_TEXT_ID))
            ).text
            except Exception as e:
                logging.warning(f"예외 상황이 발생하였습니다. {e}")
        assert chk == "연산기호는 40개까지 입력할 수 있어요.", f'[FAILED] 연산기호는 40개까지 입력할 수 있어요. 스낵바가 나타나지 않았거나 다른 값이 입력되어 있습니다. chk" {chk}'

    # 소수점 10자리 초과 체크
    def test_decimal_place_limit(self):
        # 소수점 입력 후 스낵 바 팝업 확인 루프
        chk = None
        self.tact('소수점')
        retry_count = 0
        max_retries = 15
        while chk != '소수점 이하 10자리까지 입력할 수 있어요.':
            self.tact('2')
            if retry_count >= 10:
                try:
                    chk = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((self.IDBY, self.SNACKBAR_TEXT_ID))
                ).text
                    if retry_count >= max_retries:
                        pytest.fail(f"소수점 스낵 바 확인 최대 반복 횟수가 초과하였습니다. 최대 반복 횟수: {max_retries}")
                # 예외 발생 시 처리
                except Exception as e:
                    pytest.fail(f'Failed: 예외 상황이 발생하였습니다. {e}')
            
            retry_count += 1
                
        assert chk == '소수점 이하 10자리까지 입력할 수 있어요.', f'소수점 스낵 바 확인에 실패했습니다. chk 값: {chk}'

    # 공백의 필드에서 0 중복 입력 체크
    def test_zero_not_duplicated(self, interation=5):
        # 0 반복 입력
        for i in range(interation):
            self.tact('0')
            chk = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((self.IDBY, self.FORMULA_ID))
            ).text
        
        # 입력된 0의 갯수 체크
        assert chk == '0', f'{i+1}번째 텍스트 필드의 값은 {chk}며, 0이 중복 입력 되었거나, 다른 값이 입력되어 있습니다.'

    # 소수점 버튼을 복수의 횟수 클릭 시 첫 입력 이후 무시하는 지 체크
    def test_point_not_duplicated(self, interation =5):
        # 소수점 반복 입력
        try:
            for i in range(interation):
                self.tact('소수점')
                if i == 3:
                    self.tact('0')
                # 텍스드 필드의 값 가져와 소수점 갯수 체크 후 검증
                chk = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((self.IDBY, self.FORMULA_ID))
            ).text
                factor = chk.count('.')
                assert factor == 1, f'{i+1}번째 텍스트 필드에서 소수점 개수는 {factor}개이며, 중복 입력 되었거나 전혀 입력되지 않았습니다.'
        finally:
            self.tact('초기화')

    # 15자리와 연산자 입력 후 필드의 15자리 사이에 숫자를 입력했을 때 입력 불가 체크
    def test_digit_entry_prevention_after_limit(self, iteration = 15):
        window_size = self.driver.get_window_size()
        width = int(window_size['width']*0.5)
        height = int(window_size['height']*0.15)

        # 15 자리 숫자와 연산자 입력 후 커서 이동
        for i in range(iteration):
            self.tact('2')
        self.tact('더하기')
        self.driver.tap([(width, height)])
        # 스낵바의 텍스트와 비교할 함수와 스낵바가 나타날 때 까지의 반복
        chk = None
        retry_count = 0
        while chk != '15자리까지 입력할 수 있어요.':
            self.tact('2')
            retry_count += 1
            try:
                chk = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((self.IDBY, self.SNACKBAR_TEXT_ID))
            ).text
            except Exception as e:
                pytest.fail(f'발생한 예외: {e}')
            if retry_count >= 10:
                pytest.fail(f"[FAILED] 15자리까지 입력할 수 있어요 스택바가 나타나지 않았습니다. 최대 반복 횟수를 초과하여 종료합니다. chk: {chk}")

    # 연산자를 입력한 상태에서 다른 연산자 버튼을 눌렀을 때 바뀌는지 체크
    def test_operator_switching_behavior(self):
        prev_symbol = None
        self.tact('1')
        symbol = ['더하기', '더하기', '빼기', '빼기', '곱하기', '곱하기', '나누기', '나누기']

        for symbol_item in symbol:
            self.tact(symbol_item)
            formula = self.driver.find_element(self.IDBY, self.FORMULA_ID).text.replace(' ', '')
            # 연산자가 포함되어 있는지 체크
            assert symbol_item in formula, f'[FAILED] 입력 되어야 하는 {symbol_item}가 입력되지 않았거나, {prev_symbol}에서 변경되지 않았습니다.'

            # 숫자를 제거한 현재 기호
            current_symbol = formula.replace('1', '')
            # 현재 기호를 이전 기호로 저장
            prev_symbol = current_symbol

    # 연산자가 없는 괄호식 테스트
    def test_incomplete_expression_with_brackets(self):
        expression = ('괄호', '괄호', '3', '괄호', '괄호')
        for item in expression:
            self.tact(item)
        i=0
        while i != 4:
            self.driver.press_keycode(21)
            i += 1
        self.tact('9')
        formula = self.driver.find_element(self.IDBY, self.FORMULA_ID).text
        
        chk = None
        retry_count = 0  # 재시도 횟수
        max_retries = 5  # 최대 재시도 횟수
        while chk != '완성되지 않은 수식입니다.':
            self.tact('계산')
            try:
                chk = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((self.IDBY, self.SNACKBAR_TEXT_ID))
                ).text
                retry_count += 1
                if retry_count >= max_retries:
                    pytest.fail(f"[FAIL] 재시도 횟수가 {max_retries}회를 초과하여 실패하였습니다.")
            except Exception as e:
                pytest.fail(f'발생한 예외: {e}')
        assert chk == '완성되지 않은 수식입니다.', f'[Failed] SnackBar를 찾지 못했거나 값을 가져오지 못했습니다. chk: {chk}'

    # 괄호를 닫지 않은 계산식 테스트
    def test_unclosed_bracket_error(self):
        # 계산식 입력
        expression = ('괄호', '3')
        for item in expression:
            self.tact(item)
        self.tact('계산')

        # 결과 값 저장 후 필요 없는 부분 정리
        value = self.driver.find_element(self.IDBY, self.FORMULA_ID).text
        result = value.replace('계산 결과', '').replace(' ', '').strip()

        # 케이스 성패 여부 확인
        assert result == expression[1], f'[Failed] 입력한 값과 결과 값이 다릅니다. 입력 값: {expression[1]} 결과 값: {result}'

    # 계산 기록 20개 초과 시 삭체 처리 체크
    def test_history_deletion_when_exceeding_20(self):
        # 계산 기록 20개 입력
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2]
        for value in values:
            self.tact(str(value))
            self.tact("더하기")
            self.tact(str(value))
            self.tact("계산")
        self.tact('계산기록')
        
        
        # 20개에 대한 후반부 계산 기록 가져오기
        parent_element = self.driver.find_element(self.IDBY, self.HISTORY)
        child_elements = parent_element.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        expressions = [child.text for child in child_elements]
                
        # 마지막 계산한 식 2+2 위치 저장
        lastindex_old = expressions.index('2+2')

        # 계산 기록 처음으로 스크롤
        for _ in range(2):
            self.driver.swipe(start_x=300, start_y=1400, end_x=300, end_y=2002)
        sleep(0.3)

        # 스크롤 후 20개에 대한 전반부 계산 기록 가져오기
        parent_element = self.driver.find_element(self.IDBY, self.HISTORY)
        child_elements = parent_element.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        expressions = [child.text for child in child_elements]

        # 첫번째 계산한 1+1 위치 저장
        firstindex = expressions.index('1+1')

        # 21번째 계산식 기록
        self.tact("키패드")
        self.tact("3")
        self.tact("더하기")
        self.tact("3")
        self.tact("계산")
        self.tact("계산기록")
        
        
        # 계산 기록 추가한 후반부 계산 기록 가져오기
        parent_element = self.driver.find_element(self.IDBY, self.HISTORY)
        child_elements = parent_element.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        expressions = [child.text for child in child_elements]
        
        # 2+2 계산식의 변경된 위치 저장
        lastindex_new = expressions.index('2+2')

        # 계산 기록 추가 후의 계산 기록 처음으로 스크롤
        self.driver.swipe(start_x=300, start_y=1400, end_x=300, end_y=2002)
        self.driver.swipe(start_x=300, start_y=1400, end_x=300, end_y=2002)

        # 계산 기록 추가 후의 전반부 계산 기록 가져오기
        parent_element = self.driver.find_element(self.IDBY, self.HISTORY)
        child_elements = parent_element.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        expressions = [child.text for child in child_elements]

        # 검증: 첫 번째 기록(1+1)이 삭제되었는지 확인
        assert '1+1' not in expressions, "처음 계산한 식이 삭제되지 않았음"
        
        # 검증: 마지막 계산 기록(2+2)의 위치가 변경되었는지 확인
        assert lastindex_new < lastindex_old, "마지막 계산식의 위치가 줄어들지 않았음"

    # 공학용 계산기 함수 버튼 작동 확인
    def test_scientific_calculator_functions(self):
        try:
            self.tact("공학용 모드")
        except Exception as e:
            print(f'예외 사항이 발생했습니다. : {e}')
            pytest.fail('공학용 모드 버튼을 찾지 못하였습니다.')
        
        # 입력할 버튼과 포뮬러에 표시되는 값
        standard_funcs = {
            '제곱근': '제곱근 여는 소괄호 ',
            '사인': '사인 여는 소괄호 ',
            '코사인': '코사인 여는 소괄호 ',
            '탄젠트': '탄젠트 여는 소괄호 ',
            '자연 로그': '자연 로그 여는 소괄호 ',
            '대수': '대수 여는 소괄호 ',
            '역수': '1 나누기 ',
            '오일러의 수의 거듭제곱': '오일러의 수  제곱 여는 소괄호 ',
            'x의 제곱': '9 제곱 여는 소괄호 2닫는 소괄호 ',
            '엑스의 와이제곱': '9 제곱 여는 소괄호 ',
            '절대값': '절대값 여는 소괄호 ',
            'Pi': 'Pi ',
            '오일러의 수': '오일러의 수 '
        }

        # 함수 버튼 클릭과 입력된 값과 지정된 값의 비교
        for func, excepted_output in standard_funcs.items():
            if '9' in excepted_output:
                self.tact('9')
            # NoSuchElementException의 간헐적 발생으로 인한 click() 방식 변경
            element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((self.ACCESSBY, func))
            )
            element.click()
            actual_text = self.driver.find_element(self.IDBY, self.FORMULA_ID).text
            assert actual_text.replace(' ', '') == excepted_output.replace(' ', ''), f'[FAILED] 입력된 값이 지정한 값과 다릅니다. 클릭한 버튼: {func}, 비교해야할 값: {excepted_output}, 입력 필드에 입력된 값: {actual_text}'
            self.tact('초기화')
        
        # 일반 함수 입력 후 대체 함수 버튼 확인을 위한 버튼 전환
        self.tact('대체 함수')

        # 입력할 버튼과 포뮬러에 표시되는 값
        alternate_funcs = {
            '세제곱근': '세제곱근 여는 소괄호 ',
            '역 사인': '역 사인 여는 소괄호 ',
            '역 코사인': '역 코사인 여는 소괄호 ',
            '역 탄젠트': '역 탄젠트 여는 소괄호 ',
            '쌍곡 사인': '사인 h여는 소괄호 ',
            '쌍곡 코사인': '코사인 h여는 소괄호 ',
            '쌍곡 탄젠트': '탄젠트 h여는 소괄호 ',
            '역 쌍곡 사인': '역 사인 h여는 소괄호 ',
            '역 쌍곡 코사인': '역 코사인 h여는 소괄호 ',
            '역 쌍곡 탄젠트': '역 탄젠트 h여는 소괄호 ',
            '2의 엑스제곱': '2 제곱 여는 소괄호 ',
            '세제곱': '9 제곱 여는 소괄호 3닫는 소괄호 ',
            '계승': '9계승 '
        }

        # 함수 버튼 클릭과 입력된 값과 지정된 값의 비교
        for func, excepted_output in alternate_funcs.items():
            if '9' in excepted_output:
                self.tact('9')
            element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((self.ACCESSBY, func))
            )
            element.click()
            actual_text = self.driver.find_element(self.IDBY, self.FORMULA_ID).text
            assert actual_text.replace(' ', '') == excepted_output.replace(' ', ''), f'[FAILED] 입력된 값이 지정한 값과 다릅니다. 클릭한 버튼: {func}, 비교해야할 값: {excepted_output}, 입력 필드에 입력된 값: {actual_text}'
            self.tact('초기화')

    # 200자 초과의 스낵바 확인
    def test_max_input_length_limit(self):
    # 15자리 숫자와 연산자 입력
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5']
        operator = '더하기'
        cycle_length = len(numbers) + 1

        # 반복 횟수와 
        repeat_count = 200 // cycle_length
        remainder = 200 % cycle_length

        # 반복 입력
        for _ in range(repeat_count):
            for num in numbers:
                self.tact(num)
            self.tact(operator)

        # 나머지 입력
        for i in range(remainder):
            if i < len(numbers):
                self.tact(numbers[i])
            else:
                self.tact(operator)
        
        chk = None
        while chk is None:
            self.tact("0")
            try:
                chk = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((self.IDBY, self.SNACKBAR_TEXT_ID))
            ).text
            except Exception as e:
                logging.warning(f'예외 사항이 발생하였습니다. 에러 {e}')
        assert chk == '200자까지 입력할 수 있어요.', f'[FAILED] "200자까지 입력할 수 있어요" 스낵바가 나타나지 않았거나 다른 값이 입력되었습니다. chk: {chk}'


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(self, item, call):
    if call.when == 'call': # 테스트 실행 후
        # 실패 처리
        if call.excinfo is not None:
            self.driver.execute_script(f'Failed : {item.nodeid}')
        else:
            self.driver.execute_script(f'Succese : {item.nodeid}')

# if __name__ == "__main__":
#     pytest.main()

if __name__ == "__main__":
    pytest.main(['--html=samCalcTestReport.html', '--self-contained-html', '--capture=tee-sys'])