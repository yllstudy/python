from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import imaplib
import email
import re
from email import message_from_bytes

# ------ Heygen 注册部分 ------

# 设置WebDriver路径（修改为你的WebDriver路径）css-mjwkym
# driver_path = r"D:\software\edgdriver\msedgedriver.exe"

# 创建一个WebDriver实例
driver = webdriver.Edge()

# 打开Heygen注册页面
driver.get("https://app.heygen.com/login?cid=aaba7365")

# 等待页面加载
time.sleep(2)

# 定位到“注册”按钮并点击（请根据实际页面元素进行调整）
register_button = driver.find_element(By.LINK_TEXT, "Sign Up with Email")  # 或者使用其他适当的定位方法
register_button.click()

# 等待注册页面加载
time.sleep(2)


# 查找邮箱输入框并填写（替换为你的邮箱地址）
email_input = driver.find_element(By.ID, "email")
email_input.send_keys("yll708854084@163.com")

# 点击获取验证码的按钮
get_code_button = driver.find_element(By.CLASS_NAME, "css-o9bvpj")
get_code_button.click()

# ------ 163 邮箱部分 ------

# 163邮箱设置
username = "yll708854084@163.com"  # 替换为你的邮箱用户名
password = "NSJYHILIOURLMBDR"        # 替换为你的密码
imap_url = "imap.163.com"         # 163邮箱的IMAP服务器地址


# 连接到IMAP服务器
imaplib.Commands['ID'] = ('AUTH')

mail = imaplib.IMAP4_SSL(host = imap_url, port='993')
mail.login(username, password)

# 准备IMAP ID信息并格式化为合适的字符串形式
imap_id_info = '("name" "myname" "version" "1.0.0" "vendor" "MyVendor" "support-email" "support@example.com")'
# 发送IMAP ID命令
mail._simple_command('ID', imap_id_info)

result, data = mail.select("inbox")

# 搜索未读邮件
status, messages = mail.search(None, 'UNSEEN')

# 获取最新的邮件
messages = messages[0].split(b' ')
latest_email_id = messages[-1]

# 获取邮件内容
_, msg = mail.fetch(latest_email_id, '(RFC822)')
msg = email.message_from_bytes(msg[0][1])

# 遍历邮件内容以提取验证码
verification_code = ""

if msg.is_multipart():
    for part in msg.walk():
        msg = message_from_bytes(part)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    html_content = part.get_payload(decode=True).decode('utf-8')
                    # 使用正则表达式匹配验证码
                    match = re.search(r'\b\d{6}\b', html_content)
                    if match:
                        verification_code = match.group(0)
                        print("Verification Code:", verification_code)
        else:
            # 如果邮件不是多部分，直接处理
            html_content = msg.get_payload(decode=True).decode('utf-8')
            match = re.search(r'\b\d{6}\b', html_content)
            if match:
                verification_code = match.group(0)
                print("Verification Code:", verification_code)

# 关闭邮箱连接
mail.close()
mail.logout()

# ------ 完成 Heygen 注册 ------

# 如果验证码提取成功
if verification_code:
    # 查找验证码输入框并填写验证码
    verification_code_input = driver.find_element(By.ID, "code")
    verification_code_input.send_keys(verification_code)

    # 查找提交按钮并点击
    submit_button = driver.find_element(By.CLASS_NAME, "css-7spms1")
    submit_button.click()

    # 提交验证码后，等待新页面加载
    time.sleep(5)  # 根据需要调整等待时间

    # 找到设置密码的输入框，并输入密码
    password_input = driver.find_element(By.ID, "password")  # 假设密码输入框的ID是'password'
    password_input.send_keys("1qaz2wsx#")

    # 找到确认密码的输入框，并再次输入密码
    confirm_password_input = driver.find_element(By.ID, "pwdconfirm")  # 假设确认密码输入框的ID是'confirm_password'
    confirm_password_input.send_keys("1qaz2wsx#")

    # 点击“Done”按钮完成注册
    done_button = driver.find_element(By.CLASS_NAME, "css-8bykl")  # 假设“Done”按钮的ID是'done_button'
    done_button.click()




# 关闭浏览器
# driver.quit()
