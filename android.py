import unittest
from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy

class SampleTest(unittest.TestCase):

    def setUp(self) :
        self.driver = webdriver.Remote(
            command_executor= "http://127.0.0.1:4723/wd/hub",
            desired_capabilities={
                "deviceName": "MAAIKN003089AB9",
                "platformName": "Android"
            }
        )

    # 테스트 할 app 실행
    def test_method(self):
        element = self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value='File Manager')
        element.click()
        sleep(3)
         

    # 테스트 케이스
    def test_case(self):
        driver = self.driver
        driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.TableLayout/android.widget.TableRow[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.LinearLayout").click()
        sleep(1)
        element = self.driver.find_element(by=MobileBy.ACCESSIBILITY_ID, value="Navigate up")
        element.click()
        sleep(1)
        driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/androidx.appcompat.widget.LinearLayoutCompat[1]/android.widget.CheckedTextView").click()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__" :
    suite = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)