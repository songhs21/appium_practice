from configuration import configuration
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction


wd = configuration.cal()
TouchAction = TouchAction(wd)
TouchAction.wait(ms=5000)

#설정 조작


#메시지 발신
#wd.find_element(By.ID, 'com.samsung.android.messaging:id/blackbird_first_launch_appbar_start_button').click()
#TouchAction.wait(ms=10000)
#TouchAction.tap(x=500, y=1120)
#새메시지
#wd.find_element(By.XPATH, '//android.widget.ImageButton[@content-desc="새 메시지 작성"]').click()
#wd.find_element(By.XPATH, '//android.widget.ImageButton[@content-desc="1:1 대화"]').click()




#플레이스토어
#TouchAction.tap(x=530, y=2050).perform()
#wd.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[3]/android.view.View/android.view.View[2]/android.widget.TextView').click()
#TouchAction.wait(ms=6000)
#TouchAction.tap(x=500, y=700).perform()
#TouchAction.tap(x=500, y=900).perform()
#TouchAction.tap(x=500, y=1200).perform()
#TouchAction.tap(x=500, y=1400).perform()
#TouchAction.tap(x=500, y=1700).perform()
#TouchAction.tap(x=500, y=1900).perform()
#wd.find_element(By.XPATH, '').click()
#wd.find_element(By.XPATH, '').click()
#wd.find_element_by_xpath('//android.widget.Button[@content-desc="1"]').click()
#wd.execute({'id' : 00000000-0000-02d8-ffff-ffff00000001})
#wd.find_element(By.XPATH, '//android.widget.Button[@text="1"]').click()
