#_-_encoding=utf8_-_
#__author__="huiseong.song"
# appium-python-client version 2.3.0

import logging
import pytest
from itertools import cycle
from time import sleep
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import AppiumOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# accessibility id or id
# 입력 창 : com.sec.android.app.popupcalculator:id/calc_edt_formula
# 계산 결과 : 결과 미리보기 / com.sec.android.app.popupcalculator:id/calc_tv_result
# 단위 계산 : 단위 계산기 버튼 / com.sec.android.app.popupcalculator:id/calc_handle_btn_converter
# 공학용 모드 : 공학용 모드 버튼 / com.sec.android.app.popupcalculator:id/calc_handle_btn_rotation
# 삭제 버튼 : 지우기 버튼 / com.sec.android.app.popupcalculator:id/calc_handle_btn_delete
# 플마 전환 : 플러스와 마이너스 간 전환 / com.sec.android.app.popupcalculator:id/calc_keypad_btn_plusminus

@pytest.fixture(scope='function')
def test_setup_android(request):
    options = AppiumOptions()
    options.set_capability('deviceName', '')
    options.set_capability('platformName', 'Android')
    options.set_capability('appium:appPackage', 'com.sec.android.app.popupcalculator')
    options.set_capability('appium:appActivity', 'com.sec.android.app.popupcalculator.Calculator')

    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
    request.cls.driver = driver

    def fin():
        driver.quit()

    request.addfinalizer(fin)
    yield driver

@pytest.mark.usefixtures("test_setup_android")
class TestCalculator:
    SNACKBAR_TEXT_ID = 'com.sec.android.app.popupcalculator:id/snackbar_text'
    FORMULA_ID = 'com.sec.android.app.popupcalculator:id/calc_edt_formula'
    ACCESSBY = AppiumBy.ACCESSIBILITY_ID
    IDBY = AppiumBy.ID
    width = None
    height = None

    SNACKBAR_TEXT_ID = 'com.sec.android.app.popupcalculator:id/snackbar_text'

    # 터치 입력 함수
    def tact(self, act):
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=act).click()
        sleep(0.1)

    # 계산식 계산과 결과값 검증
    def calculate(self, formula):
        self.tact('계산')
        value_text = self.driver.find_element(by=AppiumBy.ID, value=self.FORMULA_ID).text

        # formula edt에서 계산 후 텍스트를 가져올 시 문장 끝에 붙는 ' 계산 결과'의 접미사 제거
        valueA = int(value_text.replace('계산 결과', '').strip())
        valueB = None
        # 더하기 값 확인
        if formula[1] == '더하기':
            valueB = int(formula[0]) + int(formula[2])
            if valueA == valueB:
                print(f'PASS: {formula[0]}와 {formula[2]}를 더하면 {valueA}입니다.')
            else:
                print(f'FAIL: {formula[0]}, {formula[1]}, {formula[2]}의 계산 결과는 {valueA}가 아닙니다.')
        # 빼기 값 확인
        elif format[1] == '빼기':
            valueB = int(formula[0]) - int(formula[2])
            if valueA == valueB:
                print(f'PASS: {formula[0]}와 {formula[2]}를 빼면 {valueA}입니다.')
            else:
                print(f'FAIL: {formula[0]}, {formula[1]}, {formula[2]}의 계산 결과는 {valueA}가 아닙니다.')
        #나누기 값 확인
        elif format[1] == '나누기':
            valueB = int(formula[0]) / int(formula[2])
            if valueA == valueB:
                print(f'PASS: {formula[0]}와 {formula[2]}를 나누면 {valueA}입니다.')
            else:
                print(f'FAIL: {formula[0]}, {formula[1]}, {formula[2]}의 계산 결과는 {valueA}가 아닙니다.')
        #곱하기 값 확인
        elif format[1] == '곱하기':
            valueB = int(formula[0]) * int(formula[2])
            if valueA == valueB:
                print(f'PASS: {formula[0]}와 {formula[2]}를 곱하면 {valueA}입니다.')
            else:
                print(f'FAIL: {formula[0]}, {formula[1]}, {formula[2]}의 계산 결과는 {valueA}가 아닙니다.')


    @classmethod
    def setUpClass(cls) :
            desired_caps = {}
            desired_caps["deviceName"] = "R3CW70RDK9F"
            desired_caps["platformName"] = "Android"
            desired_caps["appium:appPackage"] = "com.sec.android.app.popupcalculator"
            desired_caps["appium:appActivity"] = "com.sec.android.app.popupcalculator.Calculator"
            cls.driver = webdriver.Remote("http://localhost:4723/wd/hub",
                                          options=AppiumOptions().load_capabilities(desired_caps))
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # 더하기
    def test_plus(self):
        formula = ['9', '더하기', '9']
        for formula_item in formula:
           self.tact(formula_item)
        self.calculate(formula)

    #빼기
    def test_minus(self):
        formula = ['9', '빼기', '7']
        for formula_item in formula:
            self.tact(formula_item)
        self.calculate(formula)

    #나누기
    def test_devision(self):
        formula = ['9', '나누기', '3']
        for formula_item in formula:
           self.tact(formula_item)
        self.calculate(formula)

    #곱하기
    def test_multi(self):
        formula = ['9', '곱하기', '3']
        for formula_item in formula:
           self.tact(formula_item)
        self.calculate(formula)

    # 15자리 초과 체크
    def test_digitOver(self):
        for i in range(1,17):
            if i>=10:
                i= i-10
            self.tact(str(i))
        chk = None
        # 화면 녹화 등으로 텍스트 필드 값 취득 실패에 대비한 반복문
        while chk is None:
            self.tact("6")
            chk = self.driver.find_element(by=AppiumBy.ID, value="com.sec.android.app.popupcalculator:id/snackbar_text").text
        self.tact("초기화")
        if chk == "15자리까지 입력할 수 있어요.":
            logging.info("자릿수 체크 Ok")
        else:
            print(f"자릿수 체크 Fail: {chk}")

    # 소수점 10자리 초과 체크
    def test_dicimalDigit(self):
        chk = None
        self.tact("소수점")
        for num in cycle(range(10)):
            self.tact(str(num))
            try:
                chk = self.driver.find_element(by=AppiumBy.ID, value="com.sec.android.app.popupcalculator:id/snackbar_text").text
                if chk:
                    break
            except NoSuchElementException as e:
                logging.debug(f"No element found: {e}")
            except Exception as e:
                logging.warning(f"Exception occurred: {e}")
        if chk == "소수점 이하 10자리까지 입력할 수 있어요.":
            logging.info("소수점 자릿수 확인 ok")
        else:
            logging.error(f"소수점 자릿수 확인 fail: {chk}")

    # 계산 기록 20개 초과 시 삭체 처리 체크
    def test_history(self):
        # 기록 20개 쌓기
        for i in range(1,21):
            if i==10:
                i= i-8
            elif 20>i>10:
                i= i-10
            elif i==20:
                i= i-15
            # print(i)
            self.tact(str(i))
            self.tact("더하기")
            self.tact(str(i))
            self.tact("계산")
        self.tact("계산기록")
        # 제일 마지막에 계산한 식 체크
        lastveri = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="5 더하기 5").text
        print("last fomula:", lastveri)
        # 처음 계산한 식이 나타날 때 까지 스크롤
        self.driver.swipe(start_x=280, start_y=1210, end_x=280, end_y=2002)
        self.driver.swipe(start_x=280, start_y=1210, end_x=280, end_y=2002)
        # 처음 계산한 식 기록 체크
        firstveri = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="1 더하기 1").text
        print(firstveri)
        # 처음 계산한 식이 남아있는 경우 21번재 수식 기록
        if "1+1" == firstveri:
            self.tact("키패드 버튼")
            self.tact("2")
            self.tact("더하기")
            self.tact("1")
            self.tact("계산")
            self.tact("계산기록 버튼")
            self.driver.swipe(start_x=280, start_y=1210, end_x=280, end_y=2002)
            self.driver.swipe(start_x=280, start_y=1210, end_x=280, end_y=2002)
            # 두번째로 계산한 수식 잔존 여부 체크
            veri = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="2 더하기 2").text
            print("두번째로 계산한 식 : ",veri)
            try:
                #첫번째로 계산한 수식 잔존 여부 체크
                veri = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="1 더하기 1")
            except Exception as e:
                # 남아있지 않은 경우 예외 처리
                print("removed first fomula")
        self.tact("키패드 버튼")

    # 연산 기호 40개 초과 체크
    def test_operationSymbolPcs(self):
         while True:
            self.tact("2")
            self.tact("나누기")
            try:
                chk = self.driver.find_element(by=AppiumBy.ID, value="com.sec.android.app.popupcalculator:id/snackbar_text").text
                if chk == "연산기호는 40개까지 입력할 수 있어요.":
                    print("chk=" + chk)
                    break
            except NoSuchElementException as e:
                logging.debug(f"No element found: {e}")
            except Exception as e:
                logging.warning(f"Exception occurred: {e}")
    
    # 공학용 계산기 함수 버튼 작동 확인
    def test_sciencalc(self):
        sleep(1)
        try:
            self.tact("공학용 모드")
        except:
            self.tact("대체 함수")
        funcchk = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="제곱근").text
        if funcchk == "√":
            funcs = ['제곱근', '사인', '코사인', '탄젠트', '자연 로그', '대수', '역수', '오일러의 수의 거듭제곱', 'x의 제곱', '엑스의 와이제곱', '절대값', 'Pi', '오일러의 수']
            txtchk = ['√(', 'sin(', 'cos(', 'tan(', 'ln(', 'log(', '1÷', 'e^(', '9^(2)', '9^(', 'abs(', 'π', 'e']
            fomuvalue = ['제곱근 여는 소괄호 ', '사인 여는 소괄호 ', '코사인 여는 소괄호 ', '탄젠트 여는 소괄호 ', '자연 로그 여는 소괄호 ', '대수 여는 소괄호 ', '1 나누기 ', '오일러의 수  제곱 여는 소괄호 ', '9 제곱 여는 소괄호 2닫는 소괄호 ', '9 제곱 여는 소괄호 ', '절대값 여는 소괄호 ', 'Pi ', '오일러의 수 ']
            for i in range(0,13):
                if i == 8 or i == 9:
                    self.tact("9")
                self.tact(funcs[i])
                txt = self.driver.find_element(by=AppiumBy.ID, value="com.sec.android.app.popupcalculator:id/calc_edt_formula").text
                if txt == fomuvalue[i]:
                    print(funcs[i], txtchk[i],"Checked <br>")
                else:
                    pytest.fail()
                self.tact("초기화")
        self.tact("대체 함수")
        funcchk = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="세제곱근").text
        print(funcchk)
        if funcchk == "3√":
            funcs = ['세제곱근', '역 사인', '역 코사인', '역 탄젠트', '쌍곡 사인', '쌍곡 코사인', '쌍곡 탄젠트', '역 쌍곡 사인', '역 쌍곡 코사인', '역 쌍곡 탄젠트', '2의 엑스제곱', '세제곱', '계승']
            txtchk = ['cbrt(', 'asin(', 'acos(', 'atan(', 'sinh(', 'cosh(', 'tanh(', 'asinh(', 'acosh(', 'atanh(', '2^(', '9^(3)', '9!']
            fomuvalue = ['세제곱근 여는 소괄호 ', '역 사인  여는 소괄호 ', '역 코사인  여는 소괄호 ', '역 탄젠트  여는 소괄호 ', '사인 h여는 소괄호 ', '코사인 h여는 소괄호 ', '탄젠트 h여는 소괄호 ', '역 사인  h여는 소괄호 ', '역 코사인  h여는 소괄호 ', '역 탄젠트  h여는 소괄호 ', '2 제곱 여는 소괄호 ', '9 제곱 여는 소괄호 3닫는 소괄호 ', '9계승 ']
            for i in range(0,13):
                if i == 11 or i == 12:
                    self.tact("9")
                self.tact(funcs[i])
                txt = self.driver.find_element(by=AppiumBy.ID, value="com.sec.android.app.popupcalculator:id/calc_edt_formula").text
                if txt == fomuvalue[i]:
                    print(funcs[i], txtchk[i],"Checked <br>")
                else:
                    pytest.fail()
                self.tact("초기화")
        self.tact("대체 함수")

    # 사용되지 않는 기호 및 공백에서 연산 기호 입력 실패 확인
    def test_unUsedText(self):
        symbol = ["+", "-", "*", "/", "^", "a"]
        for symbol_item in symbol:
            success = False  # 성공 여부 추적
            retry_count = 0  # 재시도 횟수
            max_retries = 5  # 최대 재시도 횟수
            while not success and retry_count < max_retries:  # 재시도 횟수를 초과하면 종료
                try:
                    # 심볼 입력
                    self.driver.find_element(by=AppiumBy.ID, value="com.sec.android.app.popupcalculator:id/calc_edt_formula").send_keys(symbol_item)
                    # snackbar_text가 나타날 때까지 기다림 (최대 5초)
                    chk = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.ID, self.SNACKBAR_TEXT_ID))
                    ).text

                    if chk == "완성되지 않은 수식입니다.":
                        print(f"공란에서 {symbol_item} 입력 불가 확인")
                        success = True  # 성공하면 반복 종료
                except NoSuchElementException as e:
                # try 동작으로 인해 반복적인 NoSuchElementException 처리
                    logging.debug(f"다음 심볼을 찾지 찾지 못함.: {symbol_item}")
                # 예상치 못한 에러 발생 처리
                except Exception as e:
                    logging.warning(f"발생한 예외: {e}")
                
                retry_count += 1  # 재시도 횟수 증가

                if retry_count == max_retries:
                    logging.error(f"{symbol_item}은 최대 반복 횟수 {max_retries}회를 초과하여 다음 연산 기호로 넘어감.")

    # 사용되지 않는 기호 및 공백에서 연산 기호 입력 실패 확인
    def test_unUsedText(self):
        symbol = ['+', '-', '*', '/', '^', 'a']
        for symbol_item in symbol:
            success = False  # 성공 여부 추적
            retry_count = 0  # 재시도 횟수
            max_retries = 5  # 최대 재시도 횟수
            while not success and retry_count < max_retries:  # 재시도 횟수를 초과하면 종료
                try:
                    # 심볼 입력
                    self.driver.find_element(by=AppiumBy.ID, value='com.sec.android.app.popupcalculator:id/calc_edt_formula').send_keys(symbol_item)
                    # snackbar_text가 나타날 때까지 기다림 (최대 5초)
                    chk = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.ID, self.SNACKBAR_TEXT_ID))
                    ).text

                    if chk == '완성되지 않은 수식입니다.':
                        print(f'공란에서 {symbol_item} 입력 불가 확인')
                        success = True  # 성공하면 반복 종료
                except NoSuchElementException as e:
                # try 동작으로 인해 반복적인 NoSuchElementException 처리
                    logging.debug(f'다음 심볼을 찾지 찾지 못함.: {symbol_item}')
                # 예상치 못한 에러 발생 처리
                except Exception as e:
                    logging.warning(f'발생한 예외: {e}')
                
                retry_count += 1  # 재시도 횟수 증가

                if retry_count == max_retries:
                    logging.error(f'{symbol_item}은 최대 반복 횟수 {max_retries}회를 초과하여 다음 연산 기호로 넘어감.')

    # 소수점 10자리 초과 체크
    def test_dicimalDigit(self):
        chk = None
        self.tact('소수점')
        for num in cycle(range(10)):
            self.tact(str(num))
            try:
                chk = self.driver.find_element(by=AppiumBy.ID, value=self.FORMULA_ID).text
                if chk:
                    break
            except NoSuchElementException as e:
            # NoSuchElementException만 DEBUG 레벨로 기록
                logging.debug(f'No element found: {e}')
            except Exception as e:
                logging.warning(f'Exception occurred: {e}')
        if chk == '소수점 이하 10자리까지 입력할 수 있어요.':
            logging.info('소수점 자릿수 확인 ok')
        else:
            logging.error(f'소수점 자릿수 확인 fail: Received message - {chk}')

    # 공백의 필드에서 0 중복 입력 체크
    def test_zero_not_duplicated(self, interation=5):
        print('TEST ZERO NOT DUPLICATED START')
        for i in range(interation):
            self.tact('0')
            chk = self.driver.find_element(self.IDBY, self.FORMULA_ID).text
            assert chk == '0', f'{i+1}번째 텍스트 필들의 값은 {chk}며, 0이 중복 입력 되었거나, 다른 값이 입력되어 있습니다.'
        print(f'{i+1}번째 텍스트 필드의 값은 {chk}며, 0이 중복으로 입력되지 않았습니다.')
        print('TEST ZERO NOT DUPLICATED END')  

    # 소수점 버튼을 복수의 횟수 클릭 시 첫 입력 이후 무시하는 지 체크
    def test_dot_not_duplicated(self, interation =5):
        print('TEST DOT NOT DUPLICATED START')
        print(self.width, self.height)

        try:
            for i in range(interation):
                self.tact('소수점')
                if i == 3:
                    self.tact('0')
                    
                chk = self.driver.find_element(self.IDBY, self.FORMULA_ID).text
                factor = chk.count('.')
                assert factor == 1, f'{i+1}번째 텍스트 필드에서 소수점 개수는 {factor}개이며, 중복 입력 되었거나 입력되지 않았습니다.'
        finally:
            self.tact('초기화')
            print(f'텍스트 필드의 값은 {chk}며, 소수점이 중복으로 입력되지 않았습니다.')
            print('TEST DOT NOT DUPLICATED END')

# 15자리와 연산자 입력 후 필드의 15자리 사이를 클릭하고 숫자를 입력했을 때 입력 불가 체크
    def test_15DigitLimitEnforced(self, iteration = 15):
        # 15 자리 숫자와 연산자 입력 후 커서 이동
        for i in range(iteration):
            self.tact('2')
        self.tact('더하기')
        self.driver.press_keycode(21)

        # 스낵바의 텍스트와 비교할 함수와 스낵바가 나타날 때 까지의 반복
        chk = None
        retries = 0
        while chk != '15자리까지 입력할 수 있어요':
            self.tact('2')
            try:
                chk = self.driver.find_element(by=AppiumBy.ID, value= "com.sec.android.app.popupcalculator:id/calc_edt_formula").text
                retries += 1
            except Exception as e:
                print('예외 사항이 발생하였습니다.')
                pytest.fail(f'발생한 예외: {e}')
            if retries >= 10:
                pytest.fail("Snackbar가 나타나지 않았습니다. 최대 반복 횟수를 초과하여 종료합니다.")
        
        # Snackbar가 정상적으로 나타났으면 테스트 완료
        print('15자리 초과 입력 제한 Snackbar가 정상적으로 나타났습니다.')

    # 연산자를 입력한 상태에서 다른 연산자 버튼을 눌렀을 때 바뀌는지 체크
    def test_ChangeSymbol(self):
        prev_symbol = None
        self.tact('1')
        symbol = ['더하기', '빼기', '곱하기', '나누기']

        for symbol_item in symbol:
            self.tact(symbol_item)
            formula = self.driver.find_element(self.IDBY, self.FORMULA_ID).text.replace(' ', '')
            # 연산자가 포함되어 있는지 체크
            assert symbol_item in formula, f'입력 되어야 하는 {symbol_item}가 입력되지 않았습니다.'
            
            current_symbol = formula.replace('1', '') # 숫자를 제거한 현재 기호
            if prev_symbol and current_symbol == prev_symbol:
                print(f'기존에 입력되어 있는 기호 {prev_symbol}에서 {symbol_item}로 변경되지 않았습니다.')
            else:
                print(f'현재 입력된 기호는 {symbol_item}이며, {formula.find(symbol_item)+1}번째 위치에 입력되어 있습니다.')
            
            prev_symbol = current_symbol # 현재 기호를 이전 기호로 저장

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(self, item, call):
    if call.when == 'call': # 테스트 실행 후
        # 실패 처리
        if call.excinfo is not None:
            self.driver.execute_script(f'Failed : {item.nodeid}')
        else:
            self.driver.execute_script(f'Succese : {item.nodeid}')

# 리포트 미 생성 테스트
if __name__ == "__main__":
    pytest.main()

# 리포트 생성 테스트
# if __name__ == "__main__":
#     pytest.main(['--html=report.html', '--self-contained-html'])
