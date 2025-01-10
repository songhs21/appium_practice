#_-_encoding=utf8_-_
#__author__="huiseong.song"
# appium-python-client version 2.3.0

import unittest
import HtmlTestRunner
from time import sleep
import HtmlTestRunner.result
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import AppiumOptions
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By

# accessibility id or id
# 입력 창 : com.sec.android.app.popupcalculator:id/calc_edt_formula
# 계산 결과 : 결과 미리보기 / com.sec.android.app.popupcalculator:id/calc_tv_result
# 단위 계산 : 단위 계산기 버튼 / com.sec.android.app.popupcalculator:id/calc_handle_btn_converter
# 공학용 모드 : 공학용 모드 버튼 / com.sec.android.app.popupcalculator:id/calc_handle_btn_rotation
# 삭제 버튼 : 지우기 버튼 / com.sec.android.app.popupcalculator:id/calc_handle_btn_delete
# 플마 전환 : 플러스와 마이너스 간 전환 / com.sec.android.app.popupcalculator:id/calc_keypad_btn_plusminus



class SampleTest(unittest.TestCase):

    # 터치 입력 함수
    def tact(self, act):
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=act).click()
        sleep(0.1)
        if act == "계산":
            self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="초기화").click()

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
        self.tact("9")
        self.tact("더하기")
        self.tact("7")
        self.tact("계산")

    #빼기
    def test_minus(self):
        self.tact("8")
        self.tact("5")
        self.tact("빼기")
        self.tact("4")
        self.tact("6")
        self.tact("계산")

    #나누기
    def test_devision(self):
        self.tact("3")
        self.tact("0")
        self.tact("나누기")
        self.tact("2")
        self.tact("계산")

    #곱하기
    def test_multi(self):
        self.tact("1")
        self.tact("소수점")
        self.tact("1")
        self.tact("곱하기")
        self.tact("4")
        self.tact("계산")

    # 15자리 초과 체크
    def test_numover(self):
        for i in range(1,17):
            if i>=10:
                i= i-10
            self.tact(str(i))
        chk = None
        # 화면 녹화 등으로 텍스트 필드 값 취득 실패에 대비한 반복문
        while chk==None:
            self.tact("6")
            chk = self.driver.find_element(by=AppiumBy.ID, value="com.sec.android.app.popupcalculator:id/snackbar_text").text
        self.tact("초기화")
        if chk == "15자리까지 입력할 수 있어요.":
            print("sackbar: '"+ chk + "' digi check ok")
        else:
            print("digi check fail")
    
    # 사용되지 않는 기호 붙여넣기 시 스낵바 체크
            
    
    # 소수점 10자리 초과 체크
            
    
    # 200자 초과 체크
       
    # 연산 기호 40개 초과 체크
    
    # rad 모드 체크
    
    # 빈 필드에서 사칙연산, 제곱 연산 기호 입력 부락 체크
    
    # 단위 계산기 열기
    
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
                    self.fail()
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
                    self.fail()
                self.tact("초기화")
        self.tact("대체 함수")

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
    #     # 제일 마지막에 계산한 식 체크
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

    #커서이동
    # def test_cursormove(self):
        # self.driver.find_element(by=AppiumBy.ID, value="com.sec.android.app.popupcalculator:id/calc_edt_formula").send_keys(PAGE_UP)

if __name__ == "__main__" :
    suite = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

#테스트 리포트 작성용 실행 코드
# if __name__ == "__main__" :
#     suite = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
#     HtmlTestRunner.HTMLTestRunner(output="samCaclTestReport", report_name="samCaclTestReport", report_title="samCaclTestReport", combine_reports=True).run(suite)
