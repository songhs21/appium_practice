import unittest
from time import sleep
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy

class SampleTest(unittest.TestCase):

    # 터치 입력 함수
    def tact(self, act):
        self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value=act).click()
        sleep(0.1)
        if act == "계산":
            self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value="초기화").click()

    def setUp(self) :
            self.driver = webdriver.Remote(
                command_executor= "http://127.0.0.1:4723/wd/hub",
                desired_capabilities={
                    "deviceName": "R3CW70RDK9F",
                    "platformName": "Android",
                    "appium:appPackage" : "com.sec.android.app.popupcalculator",
                    "appium:appActivity" : "com.sec.android.app.popupcalculator.Calculator"
                }
            )

    def tearDown(self):
        self.driver.quit()

    #더하기
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
        self.tact("1")
        self.tact("2")
        self.tact("3")
        self.tact("4")
        self.tact("5")
        self.tact("6")
        self.tact("7")
        self.tact("8")
        self.tact("9")
        self.tact("0")
        self.tact("1")
        self.tact("2")
        self.tact("3")
        self.tact("4")
        self.tact("5")
        self.tact("6")
        chk = self.driver.find_element(by=MobileBy.ID, value="com.sec.android.app.popupcalculator:id/snackbar_text").text
        if chk == "15자리까지 입력할 수 있어요.":
            print("자리수 제한 체크 ok")
        else:
            print("실패")



if __name__ == "__main__" :
    suite = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
