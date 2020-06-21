from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# 使用复用浏览器的方法登录企业微信
class TestLogin:
    def test_debug_login(self):
        option = Options()
        # Google\ Chrome --remote-debugging-port=9222
        # 需要和启动命令的端口号一致
        # 指定了一个调试地址
        option.debugger_address = "localhost:9222"
        driver = webdriver.Chrome(options=option)
        driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx")
