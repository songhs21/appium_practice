#_-_encoding=utf8_-_
#__author__='huiseong.song'
# appium-python-client version 2.3.0
import logging
import random
import unittest
from itertools import cycle
import HtmlTestRunner
from time import sleep
import HtmlTestRunner.result
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import AppiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

class SampleTest(unittest.TestCase):
    SNACKBAR_TEXT_ID = 'com.sec.android.app.popupcalculator:id/snackbar_text'
    FORMULA_ID = 'com.sec.android.app.popupcalculator:id/calc_edt_formula'
    ACCESSBY = AppiumBy.ACCESSIBILITY_ID
    IDBY = AppiumBy.ID
    width = None
    height = None

    def tact(self, act):
        self.driver.find_element(self.ACCESSBY, value=act).click()
        sleep(0.1)

    def calculate(self, formula):
        self.tact('계산')
        value_text = self.driver.find_element(by=AppiumBy.ID, value=self.FORMULA_VALUE).text
        # formula edt에서 계산 후 텍스트를 가져올 시 문장 끝에 붙는 ' 계산 결과'의 접미사 제거
        valueA = int(value_text.replace('계산 결과', '').strip())
        valueB = None
        if formula[1] == '더하기':
            valueB = int(formula[0]) + int(formula[2])
            if valueA == valueB:
                logging.info(f'PASS: {formula[0]}와 {formula[2]}를 더하면 {valueA}입니다.')
            else:
                logging.warning(f'FAIL: {formula[0]}, {formula[1]}, {formula[2]}의 계산 결과는 {valueA}가 아닙니다.')

    
    @classmethod
    def setUpClass(cls) :
            desired_caps = {}
            desired_caps['deviceName'] = 'R3CW70RDK9F'
            desired_caps['platformName'] = 'Android'
            desired_caps['appium:appPackage'] = 'com.sec.android.app.popupcalculator'
            desired_caps['appium:appActivity'] = 'com.sec.android.app.popupcalculator.Calculator'
            cls.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                        options=AppiumOptions().load_capabilities(desired_caps))
            
            window_size = cls.driver.get_window_size()
            cls.width = window_size['width']
            cls.height = window_size['height']
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # # 빼기
    # def test_minus(self):
        
    #     value = [random.randint(0, 9), '빼기', random.randint(0,9)]
    #     # for i in value:
    #     #      print(i)
    #     num = str(value[0])+str(value[2])
    #     print(type(num))
    #     print(value[0])
    #     print(value[2])
    #     print(num)
    
        

    # 사용되지 않는 기호 및 공백에서 연산 기호 입력 실패 확인
    # def test_unUsedText(self):
    #     symbol = ['+', '-', '*', '/', '^', 'a']
    #     for symbol_item in symbol:
    #         success = False  # 성공 여부 추적
    #         retry_count = 0  # 재시도 횟수
    #         max_retries = 5  # 최대 재시도 횟수
    #         while not success and retry_count < max_retries:  # 재시도 횟수를 초과하면 종료
    #             try:
    #                 # 심볼 입력
    #                 self.driver.find_element(by=AppiumBy.ID, value='com.sec.android.app.popupcalculator:id/calc_edt_formula').send_keys(symbol_item)
    #                 # snackbar_text가 나타날 때까지 기다림 (최대 5초)
    #                 chk = WebDriverWait(self.driver, 5).until(
    #                     EC.presence_of_element_located((By.ID, self.SNACKBAR_TEXT_ID))
    #                 ).text

    #                 if chk == '완성되지 않은 수식입니다.':
    #                     print(f'공란에서 {symbol_item} 입력 불가 확인')
    #                     success = True  # 성공하면 반복 종료
    #             except NoSuchElementException as e:
    #             # try 동작으로 인해 반복적인 NoSuchElementException 처리
    #                 logging.debug(f'다음 심볼을 찾지 찾지 못함.: {symbol_item}')
    #             # 예상치 못한 에러 발생 처리
    #             except Exception as e:
    #                 logging.warning(f'발생한 예외: {e}')
                
    #             retry_count += 1  # 재시도 횟수 증가

    #             if retry_count == max_retries:
    #                 logging.error(f'{symbol_item}은 최대 반복 횟수 {max_retries}회를 초과하여 다음 연산 기호로 넘어감.')



        # 소수점 10자리 초과 체크
    # def test_dicimalDigit(self):
    #     chk = None
    #     self.tact('소수점')
    #     for num in cycle(range(10)):
    #         self.tact(str(num))
    #         try:
    #             chk = self.driver.find_element(by=AppiumBy.ID, self.TEXT_EDT_ID').text
    #             if chk:
    #                 break
            # except NoSuchElementException as e:
            # # NoSuchElementException만 DEBUG 레벨로 기록
            #     logging.debug(f'No element found: {e}')
            # except Exception as e:
            #     logging.warning(f'Exception occurred: {e}')
    #     if chk == '소수점 이하 10자리까지 입력할 수 있어요.':
    #         logging.info('소수점 자릿수 확인 ok')
    #     else:
    #         logging.error(f'소수점 자릿수 확인 fail: Received message - {chk}')

# # 공백의 필드에서 0 중복 입력 체크
#     def test_zero_not_duplicated(self, interation=5):
#         print('TEST ZERO NOT DUPLICATED START')
#         for i in range(interation):
#             self.tact('0')
#             chk = self.driver.find_element(self.IDBY, self.FORMULA_ID).text
#             assert chk == '0', f'{i+1}번째 텍스트 필들의 값은 {chk}며, 0이 중복 입력 되었거나, 다른 값이 입력되어 있습니다.'
#         print(f'{i+1}번째 텍스트 필드의 값은 {chk}며, 0이 중복으로 입력되지 않았습니다.')
#         print('TEST ZERO NOT DUPLICATED END')
        

#     # 소수점 버튼을 복수의 횟수 클릭 시 첫 입력 이후 무시하는 지 체크
#     def test_dot_not_duplicated(self, interation =5):
#         print('TEST DOT NOT DUPLICATED START')
#         print(self.width, self.height)

#         try:
#             for i in range(interation):
#                 self.tact('소수점')
#                 if i == 3:
#                     self.tact('0')
                    
#                 chk = self.driver.find_element(self.IDBY, self.FORMULA_ID).text
#                 factor = chk.count('.')
#                 assert factor == 1, f'{i+1}번째 텍스트 필드에서 소수점 개수는 {factor}개이며, 중복 입력 되었거나 입력되지 않았습니다.'
#         finally:
#             self.tact('초기화')
#             print(f'텍스트 필드의 값은 {chk}며, 소수점이 중복으로 입력되지 않았습니다.')
#             print('TEST DOT NOT DUPLICATED END')

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
                chk = self.driver.find_element(self.IDBY, self.SNACKBAR_TEXT_ID).text
                retries += 1
            except Exception as e:
                print('예외 사항이 발생하였습니다.')
                self.fail(f'발생한 예외: {e}')
            if retries >= 10:
                self.fail("Snackbar가 나타나지 않았습니다. 최대 반복 횟수를 초과하여 종료합니다.")
        
        # Snackbar가 정상적으로 나타났으면 테스트 완료
        print('15자리 초과 입력 제한 Snackbar가 정상적으로 나타났습니다.')

# 연산자를 입력한 상태에서 다른 연산자 버튼을 눌렀을 때 바뀌는지 체크
    # def test_ChangeSymbol(self):
    #     prev_symbol = None
    #     self.tact('1')
    #     symbol = ['더하기', '빼기', '곱하기', '나누기']

    #     for symbol_item in symbol:
    #         self.tact(symbol_item)
    #         formula = self.driver.find_element(self.IDBY, self.FORMULA_ID).text.replace(' ', '')
    #         # 연산자가 포함되어 있는지 체크
    #         assert symbol_item in formula, f'입력 되어야 하는 {symbol_item}가 입력되지 않았습니다.'
            
    #         current_symbol = formula.replace('1', '') # 숫자를 제거한 현재 기호
    #         if prev_symbol and current_symbol == prev_symbol:
    #             print(f'기존에 입력되어 있는 기호 {prev_symbol}에서 {symbol_item}로 변경되지 않았습니다.')
    #         else:
    #             print(f'현재 입력된 기호는 {symbol_item}이며, {formula.find(symbol_item)+1}번째 위치에 입력되어 있습니다.')
            
    #         prev_symbol = current_symbol # 현재 기호를 이전 기호로 저장

# 연산자 없이 (9(3))입력의 결과 값 체크

# 괄호를 닫지 않고 계산 버튼을 눌렀을 때 반응 체크

if __name__ == '__main__' :
    suite = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)