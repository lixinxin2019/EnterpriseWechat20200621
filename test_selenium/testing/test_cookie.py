import json
import time
from time import sleep

from selenium import webdriver

# 使用cookie登录企业微信
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestCookie():
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    # def test_get_cookie(self): #该方法用于获取cookies并存储到cookies.json文件中
    #     time.sleep(15)
    #     # 一定要在扫码，登录成功之后执行
    #     cookies = self.driver.get_cookies()
    #     # 将cookies存放到cookies.json文件
    #     with open("cookies.json", "w") as f:
    #         json.dump(cookies, f)
    #     print("cookies show", cookies)

    def test_cookie_login(self, expect_conditions=None):
        cookies = json.load(open("cookies.json"))
        # for cookie in cookies:
        # 添加一个dict的cookie信息，把cookie键值对一个一个的塞入浏览器中
        # 处理每个cookie里面是否包含expiry属性
        for cookie in cookies:
            # 处理每个cookie里面是否包含expiry属性
            if 'expiry' in cookie.keys():
                cookie.pop('expiry')
            self.driver.add_cookie(cookie)

        # 等待10秒，等待程序将cookies塞入浏览器中
        # time.sleep(10)
        # 刷新页面，可见已登录状态
        # self.driver.refresh()

        # 将time.sleep(10)死等待替换成显示等待，
        while True:
            self.driver.refresh()
            res = WebDriverWait(self.driver, 10).until(
                expected_conditions.element_to_be_clickable((By.ID, "menu_index")))
            if res is not None:
                break

        # 将死等待替换成显示等待,当【导入通讯录】可点击时，再去进行后边的点击操作，
        # 注意：expected_conditions.XXX,后一定传元组
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".index_service_cnt_itemWrap:nth-child(2)")))

        # 使用CSS定位找到【导入通讯录】页面元素，并点击
        self.driver.find_element(By.CSS_SELECTOR, ".index_service_cnt_itemWrap:nth-child(2)").click()

        # time.sleep(2)
        # 将死等待替换成显示等待，当【上传文件】按钮可见时，再去进行后边的上传文件

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "js_upload_file_input")))

        # 使用id定位到【上传文件】页面元素，并上传文件，注意：send_keys必须是一个绝对路径
        self.driver.find_element(By.ID, "js_upload_file_input").send_keys(
            "/Users/edz/PycharmProjects/EnterpriseWechat/test_selenium/data/workbook.xlsx")

        time.sleep(2)
        # 断言文件上传成功
        assert_ele = self.driver.find_element(By.ID, "upload_file_name").text
        assert assert_ele == "workbook.xlsx"
        time.sleep(2)
        # 死等待比较长的时间，方便代码调试
        time.sleep(100000000)

    def teardown(self):
        self.driver.quit()
