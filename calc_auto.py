import unittest
from time import sleep
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy

def touchAction(act):
	driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value=act)
	sleep(0.1)
	if act == "계산"
        	driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value="초기화").click()

class SampleTest(unittest.TestCase):
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

    def test_sum(self):
    	touchAction("9")
    	touchAction("더하기")
    	touchAction("9")
    	touchAction("계산")
        if fom != num1+num2:
            rst = False
            if rst == False:
                print("더하기 테스트 실패")

    
    def test_min(self):
        print("곧 작성할 코드")
    

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__" :
    suite = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
