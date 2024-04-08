import unittest
import HtmlTestRunner
from time import sleep
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy

class SampleTest(unittest.TestCase):

    # 터치 입력 함수
    def tact(self, act):
        self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value=act).click()
        sleep(0.001)
        if act == "계산":
            self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value="초기화").click()
    @classmethod
    def setUpClass(cls) :
            cls.driver = webdriver.Remote(
                command_executor= "http://127.0.0.1:4723/wd/hub",
                desired_capabilities={
                    "deviceName": "R3CW70RDK9F",
                    "platformName": "Android",
                    "appium:appPackage" : "com.sec.android.app.popupcalculator",
                    "appium:appActivity" : "com.sec.android.app.popupcalculator.Calculator"
                }
            )
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # #더하기
    def test_plus(self):
        self.tact("9")
        self.tact("더하기")
        self.tact("7")
        self.tact("계산")
    # #빼기
    def test_minus(self):
        self.tact("8")
        self.tact("5")
        self.tact("빼기")
        self.tact("4")
        self.tact("6")
        self.tact("계산")
    # #나누기
    def test_devision(self):
        self.tact("3")
        self.tact("0")
        self.tact("나누기")
        self.tact("2")
        self.tact("계산")
    # #곱하기
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
        chk = self.driver.find_element(by=MobileBy.ID, value="com.sec.android.app.popupcalculator:id/snackbar_text").text
        self.tact("초기화")
        if chk == "15자리까지 입력할 수 있어요.":
            print("digi check ok")
        else:
            print("digi check fail")

    # 계산 기록의 20개 초과시 첫 수식 삭제 확인
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
        lastveri = self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value="5 더하기 5").text
        print("마지막 계산한 식:", lastveri)
        # 처음 계산한 식이 나타날 때 까지 스크롤
        self.driver.swipe(start_x=280, start_y=1210, end_x=280, end_y=2002)
        self.driver.swipe(start_x=280, start_y=1210, end_x=280, end_y=2002)
        # 처음 계산한 식 기록 체크
        firstveri = self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value="1 더하기 1").text
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
            veri = self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value="2 더하기 2").text
            print("두번째로 계산한 식 : ",veri)
            try:
                #첫번째로 계산한 수식 잔존 여부 체크
                veri = self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value="1 더하기 1")
            except Exception as e:
                # 남아있지 않은 경우 예외 처리
                print("처음에 계산한 1+1은 목록에서 사라짐")
        self.tact("키패드 버튼")


if __name__ == "__main__" :
    suite = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

#테스트 리포트 작성용 실행 코드
# if __name__ == "__main__" :
#     suite = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
#     HtmlTestRunner.HTMLTestRunner(output="samCaclTestReport", report_name="samCaclTestReport", report_title="samCaclTestReport", combine_reports=True).run(suite)
